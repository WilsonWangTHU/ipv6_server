% ----------------------------------------------------------------------
% Fig 1 is the comparision of the ipv4 and ipv6 ping speed when the 
% network is good and the link state is good.
%
% Written by Tingwu Wang, for his bachelor thesis (mid term)
% ----------------------------------------------------------------------
ipv4_data = pingReader('../data/ipv46_closePi_data/ipv4_log.txt', 2000, 40);
ipv6_data = pingReader('../data/ipv46_closePi_data/ipv6_log.txt', 2000, 40);

plot(ipv4_data, 'g')
hold on; box on; grid on
plot(ipv6_data, 'r')


average_ipv4 = ones(2000, 1) * 25.054;
average_ipv6 = ones(2000, 1) * 22.670;

average_ipv4_2 = 7.6751;
average_ipv6_2 = 7.5350;

plot(average_ipv4, 'g')
plot(average_ipv6, 'r')

legend('IPv4 traffic delay, average 25.054', 'IPv6 traffic delay, average 22.670')
title('Traffic delay between IPv4 and IPv6')
ylabel('Traffic delay / ms')