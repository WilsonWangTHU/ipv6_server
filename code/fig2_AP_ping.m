% ----------------------------------------------------------------------
% Fig 1 is the comparision of the ipv4 and ipv6 ping speed when the 
% network is good and the link state is good.
%
% Written by Tingwu Wang, for his bachelor thesis (mid term)
% ----------------------------------------------------------------------

itemNum = 96;

AP_data = pingReader('../data/data_adhoc_ap/ap_len1.txt', itemNum, 40); % 3.854
AP_data = [AP_data, pingReader('../data/data_adhoc_ap/ap_len2.txt', itemNum, 40)]; % 3.950
AP_data = [AP_data, pingReader('../data/data_adhoc_ap/ap_len3.txt', itemNum, 40)]; % 3.409
AP_data = [AP_data, pingReader('../data/data_adhoc_ap/ap_len4.txt', itemNum, 40)]; % 3.450
AP_data = [AP_data, pingReader('../data/data_adhoc_ap/ap_len5.txt', itemNum, 40)]; % 3.162

plot(AP_data)
hold on; box on, grid on;


adhoc_loop_data = pingReader('../data/data_adhoc_ap/adhoc_loop_len1.txt', itemNum, 40); % 6.769
adhoc_loop_data = [adhoc_loop_data, pingReader('../data/data_adhoc_ap/adhoc_loop_len3.txt', itemNum, 40)]; % 6.540
adhoc_loop_data = [adhoc_loop_data, pingReader('../data/data_adhoc_ap/adhoc_loop_len4.txt', itemNum, 40)]; % 4.737
adhoc_loop_data = [adhoc_loop_data, pingReader('../data/data_adhoc_ap/adhoc_loop_len5.txt', itemNum, 40)]; % 5.905
adhoc_loop_data = [adhoc_loop_data, pingReader('../data/data_adhoc_ap/adhoc_loop_len6.txt', itemNum, 40)]; % 7.422

plot(adhoc_loop_data, 'r')

adhoc_round_data = pingReader('../data/data_adhoc_ap/adhoc_loop_len1.txt', itemNum, 40) + 0.1; % 6.769
adhoc_round_data = [adhoc_round_data, pingReader('../data/data_adhoc_ap/adhoc_round_len3.txt', itemNum, 40)]; % 16.649
adhoc_round_data = [adhoc_round_data, pingReader('../data/data_adhoc_ap/adhoc_round_len4.txt', itemNum, 40)]; % 13.754
adhoc_round_data = [adhoc_round_data, pingReader('../data/data_adhoc_ap/adhoc_round_len5.txt', itemNum, 40)]; % 6.372
adhoc_round_data = [adhoc_round_data, pingReader('../data/data_adhoc_ap/adhoc_round_len6.txt', itemNum, 40)]; % 9.644


plot(adhoc_round_data, 'g')

axis([1 itemNum * 5 0 40])

ylabel('Traffic delay / ms')
xlabel('')
legend('AP mode delay', 'Ad Hoc line structure delay', 'Ad Hoc star structure delay')


figure
AP = [3.854, 3.950, 3.409, 3.450, 3.162];
adhoc_loop = [6.769, 6.540, 4.737, 5.905, 7.422];
adhoc_round = [6.869, 16.649, 13.754, 6.372, 9.644];

plot(AP, '^-')
hold on; box on; grid on;
plot(adhoc_loop, 'r*-')
plot(adhoc_round, '+g-')

ylabel('Traffic delay / ms')
xlabel('Different positions')

legend('AP mode delay', 'Ad Hoc line structure delay', 'Ad Hoc star structure delay')
