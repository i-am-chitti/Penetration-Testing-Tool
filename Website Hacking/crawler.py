#!/usr/bin/env python

# This script discovers hidden sub domains and directories of a website

import requests
import optparse


def getInput():
    parser = optparse.OptionParser(usage="Usage: crawler [-w] [website] [-h] [hostname]\n"
                                         "Usage Example:\t crawler -w google.com -h 10.0.2.8/mutildae/")
    parser.add_option("-d", "--web1", dest="web1", help="Specify website name for domain discovery without http or "
                                                        "https")
    parser.add_option("-w", "--web2", dest="web2", help="Specify website name for hidden directory discovery")
    return parser.parse_args()[0]


def request(url):
    if "http://" not in url:
        url = "http://" + url
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


def discover_subdomain(target_url, subdomain_word_list):
    try:
        with open(subdomain_word_list, "r") as word_list_file:
            for line in word_list_file:
                word = line.strip()
                test_url = word + "." + target_url
                response = request(test_url)
                if response:
                    print("--> " + test_url)

    except KeyboardInterrupt:
        print("[-] Discovery Interrupted")


def discover_directories(target_url, directory_word_list):
    try:
        with open(directory_word_list, "r") as word_list_file:
            for line in word_list_file:
                word = line.strip()
                test_url = target_url + "/" + word
                response = request(test_url)
                if response:
                    print("--> " + test_url)

    except KeyboardInterrupt:
        print("[-] Discovery Interrupted")


options = getInput()
if not options.web1 and not options.web2:
    print("[-] Specify at least one argument")
elif options.web1 and not options.web2:
    print("----------------------------------------------------------------")
    print("[+] Subdomain Discovery")
    print("*****************************************************************")
    discover_subdomain(options.web1, "subdomain_wordList.txt")
    print("******************************************************************")
elif options.web2 and not options.web1:
    print("------------------------------------------------------------------")
    print("[+] Hidden sub directory discovery")
    print("******************************************************************")
    discover_directories(options.web2, "subdirectories_wordList.txt")
    print("******************************************************************")
else:
    print("-------------------------------------------------------------------")
    print("[+] subdomain discovery")
    print("*******************************************************************")
    discover_subdomain(options.web1, "subdomain_wordList.txt")
    print("*******************************************************************")
    print("\n\n--------------------------------------------------------------------")
    print("[+] Hidden sub directory discovery")
    print("*********************************************************************")
    discover_directories(options.web2, "subdirectories_wordList.txt")
    print("**********************************************************************")