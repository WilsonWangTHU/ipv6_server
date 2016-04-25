% ----------------------------------------------------------------------
% Fig 1 is the comparision of the ipv4 and ipv6 ping speed when the 
% network is good and the link state is good.
%
% Written by Tingwu Wang, for his bachelor thesis (mid term)
% ----------------------------------------------------------------------
itemNum = 216;
ipv4_data = pingReader('../data/ipv46_farPi_data/ping4.data', itemNum, 40);
ipv6_data = pingReader('../data/ipv46_farPi_data/ping6.data', itemNum, 40);

plot(ipv4_data, 'g')
hold on; box on; grid on
plot(ipv6_data, 'r')



ipv4_data = pingReader('../data/ipv46_closePi_data/ipv4_log.txt', itemNum, 40);
ipv6_data = pingReader('../data/ipv46_closePi_data/ipv6_log.txt', itemNum, 40);

plot(ipv4_data, 'y')
plot(ipv6_data, 'c')


legend('IPv4 traffic delay of Pi 1', 'IPv6 traffic delay of Pi 1', ...
    'IPv4 traffic delay of Pi 2', 'IPv6 traffic delay of Pi 2')
title('Traffic delay between IPv4 and IPv6')
ylabel('Traffic delay / ms')
axis([1 216 0 25])