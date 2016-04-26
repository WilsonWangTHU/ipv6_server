from internetInfo import get_slaac_ip6_address, get_router_ipv6
import urllib2
import urllib


def heart_beat_ipv6(time, iface_name, port_num, target_host=0):
    ''' In this function, we try to send url request to the
    master router. The router's address is deducted from the
    slaac ipv6 address of the current host
    '''
    try:
        my_address = get_slaac_ip6_address(iface_name)
        router_address = get_router_ipv6(my_address, 1)

        # send the url request (http post request)
        #test_data = {'ServiceCode': 'aaaa'}
        #test_data_urlencode = urllib.urlencode(test_data)
        #requrl = '[' + router_address + ']:' + str(port_num) + '/heart'
        requrl = 'http://[' + '2001:da8:b100:101d::1' + ']:' + str(port_num) + '/heart'
        print requrl
        req = urllib2.Request(url=requrl, data='2001:da8:b100:101d:76e5:bff:fee3:1db6')
        print(req)

        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print(res)
    except IndexError:
        print("No mac address or IPv6 address available")
    finally:
        print('this Heart beat stopped')
    return
