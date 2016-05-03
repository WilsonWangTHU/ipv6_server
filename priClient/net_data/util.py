from models import ipv6_address
from models import client_info
from models import wlan_configuration
import os  # to obtain the conf files
import subprocess


def modify_hostapd_conf():
    configuration = wlan_configuration.objects.all()
    if len(configuration) == 0:
        configuration = wlan_configuration()
        configuration.save()
    else:
        configuration = configuration[0]

    base_bir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_hostapd = \
        os.path.join(base_bir, 'hostapd_conf', 'hostapd_template.conf')
    output_hostapd = \
        os.path.join(base_bir, 'hostapd_conf', 'hostapd.conf')
    subprocess.call(["cp", template_hostapd, output_hostapd])
    subprocess.Popen("echo 'wpa_passphrase=" + configuration.password + "' >>" + output_hostapd, shell=True)
    subprocess.Popen("echo 'channel=" + str(configuration.channel) + "' >> " + output_hostapd, shell=True)


def create_client_info(mac_address, ipv6_addresses,
                       global_ipv6_address, heart_beat_frequency):

    client = client_info(mac_address=mac_address,
                         global_ipv6_address=global_ipv6_address,
                         heart_beat_frequency=heart_beat_frequency)
    client.save()

    # the address format:
    # address_data = address_data + address.replace('/64', '') + '\n'
    for address in ipv6_addresses.split('\n')[:-1]:  # one '' string removed
        address_object = ipv6_address(ipv6_address=address)
        address_object.save()
        client.ipv6_addresses.add(address_object)

    client.save()


def change_client_info(client, mac_address, ipv6_addresses,
                       global_ipv6_address, heart_beat_frequency):
    client.mac_address = mac_address
    client.global_ipv6_address = global_ipv6_address
    client.heart_beat_frequency = heart_beat_frequency

    for address in client.ipv6_addresses.all():
        address.delete()

    for address in ipv6_addresses.split('\n')[:-1]:  # one '' string removed
        address_object = ipv6_address(ipv6_address=address)
        address_object.save()
        client.ipv6_addresses.add(address_object)

    client.save()


def delete_client_info(client):
    for address in client.ipv6_addresses.all():
        address.delete()
    client.delete()
