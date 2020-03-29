#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue


def cut_internet_connection(packet):
    packet.drop()


nfqueue = netfilterqueue.NetfilterQueue()
nfqueue.bind(0, cut_internet_connection())
try:
    nfqueue.run()
except KeyboardInterrupt:
    print("[+] Quitting")
    nfqueue.unbind()
