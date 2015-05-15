#!/bin/sh
echo "Droplet spawned at $(date -R)!" >> /root/output.log
echo "1" >> /proc/sys/net/ipv4/ip_forward

iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -j MASQUERADE
