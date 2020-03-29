#!/usr/bin env python

import subprocess
import optparse
import re


def getInput():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface name")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] error interface name not provided")
    if not options.new_mac:
        parser.error("[-] error MAC not provided")
    return options


def mac_changer(interface, mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    print(ifconfig_result)
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_result:
        return mac_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = getInput()

curr_mac_address = get_current_mac_address(options.interface)
print("Last MAC : "+str(curr_mac_address))

mac_changer(options.interface, options.new_mac)

curr_mac_address = get_current_mac_address(options.interface)
if curr_mac_address == options.new_mac:
    print("[+] MAC address was successfully changed "+ options.interface + " to "+curr_mac_address)
else:
    print("[-] MAC address did not get changed.")