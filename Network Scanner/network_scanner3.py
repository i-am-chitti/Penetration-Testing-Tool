#!/usr/bin/env python3

import scapy.all as scapy
import argparse


def getIpRange():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="iprange", help="Specify Ip Range in CIDR format")
    options, arguments = parser.parse_args()
    if not options.iprange:
        print("[-] Specify Ip Range")
    else:
        return options.iprange


def scan(ip):
    # scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    # arp_request.show()  # print details of the packet
    # print(arp_request.summary())
    # scapy.ls(scapy.ARP())
    broadcast_ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast_ether / arp_request
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # verbose makes it print details about its status like "sending 256 packets"

    # creating a list of dictionaries of ip as key and mac as value
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    print_ip_mac(client_list)


def print_ip_mac(client_list):
    print("Ip\t\t\tMAC Address\n--------------------------------------------------------")
    for element in client_list:
        print(element["ip"] + "\t\t" + element["mac"])


ipRange = getIpRange()
if ipRange:
    scan(ipRange)
