#! /bin/sh

sudo /usr/local/bin/hostapd -B /priClient/hostapd_conf/hostapd.conf

echo 'Starting the hostapd!'

sudo /sbin/ip -6 addr add 2001::1/64 dev wlan0
