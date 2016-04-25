/sbin/iptables -F
/sbin/iptables -X
/sbin/iptables -t nat -F

iptables -A FORWARD -o eth0 -i wlan0 -s 192.168.0.0/24 -m conntrack --ctstate NEW -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sysctl -w net.ipv4.ip_forward=1
/sbin/sysctl -w net.ipv6.conf.all.forwarding=1
/sbin/sysctl -w net.ipv4.conf.all.forwarding=1

killall hostapd
/etc/init.d/dnsmasq restart
