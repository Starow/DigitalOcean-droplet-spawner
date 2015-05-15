#!/usr/bin/env python2
# -*-coding:UTF-8 -*

import ConfigParser
import digitalocean
import os
import time

# Parsing Conf File #
configfile = '../config/config.cfg'
cfg = ConfigParser.ConfigParser()
cfg.read(configfile)

token = cfg.get("TOKEN", "token")
ssh_priv = cfg.get("SSH", "priv")
known_hosts = cfg.get("SSH", "hosts")
ssh_pub = cfg.get("SSH", "pub")
ssh_pub = [ssh_pub]
script_file = cfg.get("SCRIPTS", "script")

manager = digitalocean.Manager(token=token)
snapshots = manager.get_my_images()
droplets = manager.get_all_droplets()

# Loading script applied to Droplet
with open(script_file, 'r') as F:
    user_data = F.read()

# If no current running droplets
if len(droplets) == 0:
    droplet = digitalocean.Droplet(token=token,
                                   name=snapshots[0].name,
                                   region=snapshots[0].regions[0],
                                   image=snapshots[0].id,
                                   ssh_keys=ssh_pub,
                                   size_slug='1gb',
                                   size=snapshots[0].min_disk_size,
                                   backups=True,
                                   user_data=user_data)
    droplet.create()
    print "Droplet Successfully Created. Spawning..."

    # Waiting droplet activation to get ip
    while droplet.status != "active":
        time.sleep(1)
        droplet = manager.get_droplet(droplet.id)
        pass

    else:
        ip = droplet.networks['v4'][0]['ip_address']
        print "Ipv4 Adress: " + ip
        # Removing fingerprint from known_host.
        os.system('ssh-keygen -f ' + known_hosts + ' -R ' + ip)

else:
    print "Already 1 Droplet is running: Creation Aborted, Destroying..."

    for drop in droplets:
        print "Destroying Droplet: " + drop.name + " ..."
        drop.destroy()
        print "Complete!"

