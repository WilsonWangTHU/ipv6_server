# from internetInfo import get_slaac_ip6_address, get_router_ipv6
from internetInfo import get_all_global_ip6_address, get_mac_address
from internetInfo import get_ivi_address, get_subnet_prefix
import urllib2
import urllib
from subClient.pid import pid


nms_address = '2001:250:3::191'


def heart_beat_ipv6(heart_beat_time, iface_name, port_num, target_host=0, test_mode=0):
    ''' In this function, we try to send url request to the
    master router. The router's address is deducted from the
    slaac ipv6 address of the current host

    if 'target_host' == 0, then we are using the target_host's intranet address
    if 'test_mode' == 1, then we will send the data to the local ipv4 host 127.0.0.1
    if 'test_mode' == 2, then we will send the data to the local ipv4 host 127.0.0.2

    if the priServer received the data, it returns 'success'
    '''
    try:
        router_address = '2001::1'

        # get all the ipv6 addresses to be sent
        num_address, ipv6_addresses = get_all_global_ip6_address('wlan0')
        address_data = ''
        global_address = ''
        for address in ipv6_addresses:
            if address.find('2001::') == -1:
                global_address = address.replace('/64', '')
            address_data = address_data + address.replace('/64', '') + '\n'

        # send the url request (http post request)
        data = {'global_ipv6_address': global_address}
        data['mac_address'] = get_mac_address(iface_name)
        data['ipv6_addresses'] = address_data
        data['heart_beat_frequency'] = heart_beat_time
        data['ivi_address'] = get_ivi_address(iface_name)
        data['pid'] = pid
        data_urlencode = urllib.urlencode(data)

        if test_mode == 1 or test_mode == 2:
            requrl = 'http://' + '127.0.0.' + str(test_mode) + ':' + str(port_num) + '/heart/'
            req = urllib2.Request(url=requrl, data=data_urlencode)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            print(res)
        else:  # the actual mode
            # also tell the nms about this
            requrl = 'http://[' + nms_address + ']:' + str(port_num) + '/heart/'
            req = urllib2.Request(url=requrl, data=data_urlencode)
            res_data = urllib2.urlopen(req)

            requrl = 'http://[' + router_address + ']:' + str(port_num) + '/heart/'
            req = urllib2.Request(url=requrl, data=data_urlencode)
            res_data = urllib2.urlopen(req)
        return res_data.read()
    except IndexError:
        print("No mac address or IPv6 address available")
    finally:
        print('this Heart beat stopped')
    return


def request_prefix_ipv6(heart_beat_time, iface_name, port_num, target_host=0, test_mode=0):
    ''' In this function, we try to send url request to the
    master router. The router's address is deducted from the
    slaac ipv6 address of the current host

    if 'target_host' == 0, then we are using the target_host's intranet address
    if 'test_mode' == 1, then we will send the data to the local ipv4 host 127.0.0.1
    if 'test_mode' == 2, then we will send the data to the local ipv4 host 127.0.0.2

    if the priServer received the data, it returns 'success'
    '''
    try:
        router_address = '2001::1'

        # get all the ipv6 addresses to be sent
        num_address, ipv6_addresses = get_all_global_ip6_address('wlan0')
        address_data = ''
        global_address = ''
        for address in ipv6_addresses:
            if address.find('2001::') == -1:
                global_address = address.replace('/64', '')
            address_data = address_data + address.replace('/64', '') + '\n'

        # send the url request (http post request)
        data = {'global_ipv6_address': global_address}
        data['mac_address'] = get_mac_address(iface_name)
        data['ipv6_addresses'] = address_data
        data['heart_beat_frequency'] = heart_beat_time
        data['ivi_address'] = get_ivi_address(iface_name)
        data['pid'] = pid
        data['prefix'] = get_subnet_prefix('wlan1')  # it is important
        data_urlencode = urllib.urlencode(data)

        if test_mode == 1 or test_mode == 2:
            requrl = 'http://' + '127.0.0.' + str(test_mode) + ':' + str(port_num) + '/prefix/'
            req = urllib2.Request(url=requrl, data=data_urlencode)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            print(res)
        else:  # the actual mode
            # also tell the nms about this
            # requrl = 'http://[' + nms_address + ']:' + str(port_num) + '/prefix/'
            # req = urllib2.Request(url=requrl, data=data_urlencode)
            # res_data = urllib2.urlopen(req)

            requrl = 'http://[' + router_address + ']:' + str(port_num) + '/prefix/'
            req = urllib2.Request(url=requrl, data=data_urlencode)
            res_data = urllib2.urlopen(req)
        return res_data.read()
    except IndexError:
        print("No mac address or IPv6 address available")
    finally:
        print('this Heart beat stopped')
    return
