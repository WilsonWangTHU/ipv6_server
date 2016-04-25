% ----------------------------------------------------------------------
% Fig 1 is the comparision of the ipv4 and ipv6 ping speed when the 
% network is good and the link state is good.
%
% Written by Tingwu Wang, for his bachelor thesis (mid term)
% ----------------------------------------------------------------------
itemNum = 280;

ipv4_data = iperfReader('../data/ipv46_closePi_data/iperf_ipv4_data.txt', itemNum, 100);
ipv6_data = iperfReader('../data/ipv46_closePi_data/iperf_ipv6_data.txt', itemNum, 100);

plot(ipv4_data, 'g')
hold on;
plot(ipv6_data, 'r')


average_ipv4 = ones(itemNum, 1) * sum(ipv4_data) / itemNum;
average_ipv6 = ones(itemNum, 1) * sum(ipv6_data) / itemNum;

plot(average_ipv4, 'g', 'LineWidth', 3)
plot(average_ipv6, 'r', 'LineWidth', 3)

legend('IPv4 bandwith, average 12.2213', 'IPv6 bandwith, average 12.7023')
title('Bandwith between IPv4 and IPv6')
ylabel('bandwith / (Mbits/sec)')
axis([1 itemNum 5 25])


box on; grid on