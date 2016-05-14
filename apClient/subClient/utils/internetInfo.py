import subprocess  # use the debian/raspbian shell command
import string
import IPy


def get_subnet_prefix(iface_name):
    try:
        subnet_address = get_ivi_address(iface_name)  # get ivi can get static!
        subnet_prefix = get_router_ipv6(subnet_address, type=1)
        std_address = IPy.IP(subnet_prefix).strCompressed()
        pos = std_address.find('::')
        prefix = std_address[0: pos]
    except IndexError:
        return 'None'
    return prefix + '::'


def get_ivi_address(iface_name):
    # it could also be used to find the staticly set ipv6 address
    # such as prefix on wlan1
    get_address_info = subprocess.Popen(['ip', '-6', 'addr', 'show', iface_name],
                                        stdout=subprocess.PIPE)
    get_address_info = subprocess.Popen(['grep', 'global'],
                                        stdout=subprocess.PIPE,
                                        stdin=get_address_info.stdout)
    get_address_info = subprocess.Popen(['grep', '-v', 'dynamic'],
                                        stdout=subprocess.PIPE,
                                        stdin=get_address_info.stdout)
    try:
        addresses = get_address_info.communicate()[0][:-1].split('\n')
        num_address = len(addresses)
        for i_address in xrange(0, num_address):
            addresses[i_address] = addresses[i_address].lstrip(' ').split(' ')[1]
    except IndexError:
        return 'None'

    return addresses[0]


def shrink_hex_string(input_string):
    # from '0b10' to 'b10'. Ah! Why do people always want to look
    # smart? It is really no point to brief an ipv6 address!
    return hex(int(input_string, 16)).lstrip('0x')


def get_mac_address(iface_name):
    get_address_info = subprocess.Popen(['ip', 'link', 'show', iface_name],
                                        stdout=subprocess.PIPE)
    get_address_info = subprocess.Popen(['grep', 'link/ether'],
                                        stdout=subprocess.PIPE,
                                        stdin=get_address_info.stdout)
    return get_address_info.communicate()[0].lstrip(' ').split(' ')[1]


def get_all_global_ip6_address(iface_name):
    get_address_info = subprocess.Popen(['ip', '-6', 'addr', 'show', iface_name],
                                        stdout=subprocess.PIPE)
    get_address_info = subprocess.Popen(['grep', 'global'],
                                        stdout=subprocess.PIPE,
                                        stdin=get_address_info.stdout)

    addresses = get_address_info.communicate()[0][:-1].split('\n')
    num_address = len(addresses)
    for i_address in xrange(0, num_address):
        addresses[i_address] = addresses[i_address].lstrip(' ').split(' ')[1]

    return num_address, addresses


def get_slaac_ip6_address(iface_name):
    '''
    In this function, try to return the slaac 64 ipv6 address of the subClient.
    Note that the majorClient is not configured by slaac 64
    '''
    get_address_info = subprocess.Popen(['ip', '-6', 'addr', 'show', iface_name],
                                        stdout=subprocess.PIPE)
    get_address_info = subprocess.Popen(['grep', 'global dynamic'],
                                        stdout=subprocess.PIPE,
                                        stdin=get_address_info.stdout)

    # 1. find the one that is slaac64 configured, the slaac 64
    # is configured from the mac address **:**:**:**:**:** into
    # **:**:**:FF:FE:**:**:**. It is a standard Modified EUI-64 address
    # 2. The ipv6 stateless configuration reverse the 7th bit of EUI-64
    mac_part = get_mac_address(iface_name).split(':')

    # reverse the 7th bit in the EUI-64 into '1'. '1' denotes universal
    slaac_part1 = string.rjust(bin(int(mac_part[0] + mac_part[1], 16)).lstrip('0b'), 16, '0')
    slaac_part1 = slaac_part1[0:6] + '1' + slaac_part1[7::]

    slaac_part1 = shrink_hex_string(hex(int(slaac_part1, 2)))
    slaac_part2 = shrink_hex_string(mac_part[2] + 'ff')
    slaac_part3 = shrink_hex_string('fe' + mac_part[3])
    slaac_part4 = shrink_hex_string(mac_part[4] + mac_part[5])
    matching_address = slaac_part1 + ':' + slaac_part2 + ':' + \
        slaac_part3 + ':' + slaac_part4
    get_address_info = subprocess.Popen(['grep', matching_address],
                                        stdout=subprocess.PIPE,
                                        stdin=get_address_info.stdout)

    addresses = get_address_info.communicate()[0][:-1].split('\n')
    num_address = len(addresses)
    for i_address in xrange(0, num_address):
        addresses[i_address] = addresses[i_address].lstrip(' ').split(' ')[1]

    return num_address, addresses


def get_router_ipv6(ipv6_address, type=1):
    '''
    type=1 means that the router is the 64 prefix::1, other type might be possible
    '''

    # take out possible prefix, and take into consideration of abbreviation
    ipv6_pure_address = ipv6_address.replace('/64', '')
    if ipv6_pure_address.find('::') == -1:
        ipv6prefix = ipv6_pure_address.split(':')
        return ipv6prefix[0] + ':' + ipv6prefix[1] + ':' + \
            ipv6prefix[2] + ':' + ipv6prefix[3] + '::1'
    else:
        # in the case abbreviation
        ipv6part = ipv6_pure_address.split('::')
        ipv6prefix = ipv6part[0].split(':')
        if len(ipv6prefix) >= 4:  # the prefix is all here
            return ipv6prefix[0] + ':' + ipv6prefix[1] + ':' + \
                ipv6prefix[2] + ':' + ipv6prefix[3] + '::1'
        else:
            # the address must have all been write out, then just switch
            # the last 8 xxxx:xxxx:xxxx:xxxx into 0:0:0:1
            ipvsubfix = ipv6part[1].split(':')
            if len(ipvsubfix) < 4:
                return ipv6part[0] + '::1'
            ipv6_address = ipv6part[0]
            hiden_prefix = 8 - len(ipv6prefix) - len(ipvsubfix)
            if hiden_prefix > 0:
                ipv6_address = ipv6_address + hiden_prefix * ':0'
            for address_component in ipvsubfix[:len(ipvsubfix) - 4]:
                ipv6_address = ipv6_address + ':' + address_component
            return ipv6_address + ':0:0:0:1'
