% ----------------------------------------------------------------------
% It is the figure to see the histgram of average ping delay
% Written by Tingwu Wang
% ----------------------------------------------------------------------


% the bar element
average_delay = zeros(4,2);

itemNum = 2000;
ipv4_data = pingReader('../data/ipv46_farPi_data/ping4.data', itemNum, 40);
ipv6_data = pingReader('../data/ipv46_farPi_data/ping6.data', itemNum, 40);

average_delay(1, 1) = sum(ipv4_data) / itemNum;
average_delay(1, 2) = sum(ipv6_data) / itemNum;


average_delay(2, 1) = 25.054;
average_delay(2, 2) = 22.670;


itemNum = 216;
ipv4_data = pingReader('../data/ipv46_closePi_data/ipv4_log.txt', itemNum, 40);
ipv6_data = pingReader('../data/ipv46_closePi_data/ipv6_log.txt', itemNum, 40);

average_delay(3, 1) = sum(ipv4_data) / itemNum;
average_delay(3, 2) = sum(ipv6_data) / itemNum;

average_delay(4, 1) = 33.775;
average_delay(4, 2) = 25.382;

bar(average_delay, 1);
colormap([0 1 0; 1 0 0]);
box on; grid on;
title('Avarage traffic delay under different pis')
ylabel('Traffic delay /ms')
legend('IPv4 traffic', 'IPv6 traffic')