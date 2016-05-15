from internetInfo import get_ivi_address
from netaddr.ip import IPNetwork
import subprocess
import urllib
import urllib2


def set_second_ivi_route(target_address, target_via, iface_name):
    # first find out if the target is with in the next hop
    target_via_prefix = str(IPNetwork(target_via + '/64').network)
    my_next_hop_addr = get_ivi_address('wlan0')
    my_next_prefix = str(IPNetwork(my_next_hop_addr).network)

    # add the needed route table on this machine
    subprocess.Popen('ip -6 route add ' + target_address + ' via ' + target_via + ' dev ' + iface_name, shell=True)

    if my_next_prefix != target_via_prefix:
        # we need to tell the next hop machine what to do!
        tell_next_machine(70, target_address, target_via)
        return


def tell_next_machine(port_num, target_address, target_via):
    try:
        target_via_prefix = str(IPNetwork(target_via + '/64').network)
        router_address = subprocess.Popen('ip -6 route | grep ' + target_via_prefix, shell=True,
                                          stdout=subprocess.PIPE)
        router_address = router_address.communicate()[0].split('\n')[2]

        # send the url request (http post request)
        data = {'target_address': target_address}
        data['target_via'] = target_via
        data_urlencode = urllib.urlencode(data)

        requrl = 'http://[' + router_address + ']:' + str(port_num) + '/update_route/'
        req = urllib2.Request(url=requrl, data=data_urlencode)
        res_data = urllib2.urlopen(req)
        return res_data.read()
    except IndexError:
        print("No mac address or IPv6 address available")
    finally:
        print('this Heart beat stopped')
    return
