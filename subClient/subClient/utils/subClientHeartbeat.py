from internetInfo import get_slaac_ip6_address, get_router_ipv6
from internetInfo import get_all_global_ip6_address
import urllib2
import urllib


def heart_beat_ipv6(time, iface_name, port_num, target_host=0, test_mode=0):
    ''' In this function, we try to send url request to the
    master router. The router's address is deducted from the
    slaac ipv6 address of the current host

    if 'target_host' == 0, then we are using the intranet
    if 'test_mode' == 1, then we will send the data to the local ipv4 host
    '''
    try:

        # get the communicating address
        num_address, my_address = get_slaac_ip6_address(iface_name)
        find_address_flag = 0
        if num_address > 1:  # we have multiple choices
            if target_host == 0:  # we use the subnet 2001::/64 to do this
                for i_address in my_address:
                    if i_address.find('2001::') or i_address.find('2001:0:'):
                        my_address = i_address
                        find_address_flag = 1
                        break
            else:
                for i_address in my_address:
                    if i_address.find('2001::') or i_address.find('2001:0:'):
                        continue
                    my_address = i_address  # use the outernet address
                    find_address_flag = 1
            assert find_address_flag == 1, 'Error when finding the address'

        router_address = get_router_ipv6(my_address, type=1)

        # get all the ipv6 addresses to be sent
        num_address, ipv6_addresses = get_all_global_ip6_address('wlan0')
        address_data = ''
        for address in ipv6_addresses:
            address_data = address_data + address.replace('/64', '') + '\n'

        # send the url request (http post request)
        data = {'data': address_data}
        data_urlencode = urllib.urlencode(data)

        if test_mode == 1:        
            requrl = 'https://[' + '127.0.0.1' + ']:' + str(port_num) + '/heart/'
            req = urllib2.Request(url=requrl, data=data_urlencode)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            print(res)
        else:
            requrl = 'http://[' + router_address + ']:' + str(port_num) + '/heart/'
            req = urllib2.Request(url=requrl, data=data_urlencode)            
            res_data = urllib2.urlopen(req)
        
        # TODO deal with the data received
    except IndexError:
        print("No mac address or IPv6 address available")
    finally:
        print('this Heart beat stopped')
    return
