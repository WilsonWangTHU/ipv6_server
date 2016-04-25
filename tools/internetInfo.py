import subprocess  # use the debian/raspbian shell command
import string


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


def get_slaac_ip6_address(iface_name):
    '''
    In this function, try to return the slaac 64 ipv6 address of the subClient.
    Note that the majorClient is not configured by slaac 64
    '''
    get_address_info = subprocess.Popen(['ip', '-6', 'addr', 'show', iface_name],
                                        stdout=subprocess.PIPE)
    get_address_info = subprocess.Popen(['grep', 'global'],
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
    return get_address_info.communicate()[0].lstrip(' ').split(' ')[1]
