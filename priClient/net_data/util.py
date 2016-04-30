from models import ipv6_address
from models import client_info


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
