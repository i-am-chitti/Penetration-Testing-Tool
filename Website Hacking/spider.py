#!/usr/bin/env python

# This script analyse the source code of a website and extract all links (image, href tags) and then recursively
# identify all of them to map the website. It does not crawl a page inside login or sign up. For this,
# see scanner.py where seesion has been implemented

import re
import requests
import urlparse


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content)


def crawl(target_url):
    href_links_list = extract_links_from(target_url)
    for link in href_links_list:
        # joining relative links with current link
        link = urlparse.urljoin(target_url, link)

        # removing links starting with '#'
        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in unique_link_list:
            unique_link_list.append(link)
            print(link)
            crawl(link)


target_url = "http://10.0.2.8/mutillidae/"
unique_link_list = []

crawl(target_url)
