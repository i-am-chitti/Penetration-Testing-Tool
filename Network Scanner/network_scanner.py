#!/usr/bin/env python

import scapy.all as scapy
import optparse


# This script discovers all the hosts that are connected to the same subnet as the hacker. The connection could be
# either wired or wireless

def getIpRange():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip", dest="iprange", help="Specify Ip Range in CIDR format")
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
    answered_list = scapy.srp(arp_request_broadcast, timeout=4, verbose=False)[0]
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
