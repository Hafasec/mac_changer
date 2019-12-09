#!/usr/bin/env python

import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address for")
    parser.add_option("-m", "--mac", dest="new_MAC", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_MAC:
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options


def MAC_changer(interface, new_MAC):
    print("[+] Changing MAC address for " + interface + " to " + new_MAC)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_MAC])
    subprocess.call(["sudo", "ifconfig", interface, "up"])


def get_MAC(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_args()
MAC_changer(options.interface, options.new_MAC)
current_MAC = get_MAC(options.interface)

if current_MAC == options.new_MAC:
    print("[+] MAC address was successfully changed to " + current_MAC)
else:
    print("[-] Couldn't change the MAC address")

