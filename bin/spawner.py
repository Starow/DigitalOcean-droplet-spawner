#!/usr/bin/env python2
# -*-coding:UTF-8 -*

import ConfigParser
import digitalocean
import time

# Parsing Conf File #
configfile = '../config/config.cfg'
cfg = ConfigParser.ConfigParser()
cfg.read(configfile)

token = cfg.get("TOKEN", "token")
ssh_key = cfg.get("SSH", "key")
ssh_key = [ssh_key]
script_file = cfg.get("SCRIPTS", "script")

manager = digitalocean.Manager(token=token)

snapshots = manager.get_my_images()
droplets = manager.get_all_droplets()

with open(script_file, 'r') as F:
    user_data = F.read()

# No current running droplets
if len(droplets) == 0:
    droplet = digitalocean.Droplet(token=token,
                                   name=snapshots[0].name,
                                   region=snapshots[0].regions[0],
                                   image=snapshots[0].id,
                                   ssh_keys=ssh_key,
                                   size_slug='1gb',
                                   size=snapshots[0].min_disk_size,
                                   backups=True,
                                   user_data=user_data)
    droplet.create()

    while droplet.status != "active":
        droplet = manager.get_droplet(droplet.id)
        pass
    else:
        print droplet.networks
else:
    print "Already 1 Droplet is running: Creation Aborted."

