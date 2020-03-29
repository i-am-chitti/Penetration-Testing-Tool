#!/usr/bin/env python

# This script crawls a website that has login or session pages and also does login. Basically, it creates a session
# in its constructor to store a login session and then doesn't crawls log out links.

# This script has crawling feature, link extraction, form extraction and submission etc.
# This script is used in vulnerbility_scanner.py file

import re
import requests
import urlparse
from bs4 import BeautifulSoup


class Scanner:

    def __init__(self, url, ignore_link_list):
        self.session = requests.Session()
        self.links_to_ignore_list = ignore_link_list
        self.target_url = url

        # self.target_links_list is list that would be containing the links which are discovered while crawling a
        # given link
        self.target_links_list = []

    def extract_links_from(self, url):
        # once the session has been created, we have to get response with that session
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content)

    def crawl(self, target_url=None):
        if target_url is None:
            target_url = self.target_url
        href_links_list = self.extract_links_from(target_url)
        for link in href_links_list:
            # joining relative links with current link
            link = urlparse.urljoin(target_url, link)

            # removing links starting with '#'
            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links_list and link not in self.links_to_ignore_list:
                self.target_links_list.append(link)
                self.crawl(link)

    def extract_forms(self, target_url):
        # extracting all the forms that are present in this url
        response = self.session.get(target_url)

        # parsing the response content
        parse_html = BeautifulSoup(response.content, 'html.parser')
        # findAll returns the list containing the provided element
        return parse_html.findAll("form")

    def submit_form(self, form, value, page_url):
        form_action_link = form.get("action")
        # link may be relative. So, we have to convert it using urlpasrse
        form_action_link = urlparse.urljoin(page_url, form_action_link)
        method = form.get("method")

        # identifying <input> fields in this form
        form_input_list = form.findAll("input")
        # iterating for each input field

        post_data = {}

        for input_field in form_input_list:
            # getting 'name' attribute value
            input_field_name = input_field.get("name")
            input_field_type = input_field.get("type")
            input_field_value = input_field.get("value")
            if input_field_type == "text":
                input_field_value = value

            # binding each input field value into dictionary element
            post_data[input_field_name] = input_field_value
        if method == "post":
            return self.session.post(form_action_link, data=post_data)
        return self.session.get(form_action_link, params=post_data)

    def run_scanner(self):
        for link in self.target_links_list:
            forms = self.extract_forms(link)
            for form in forms:
                print("[+] Testing form in " + link)
                is_form_vulnerable_to_xss = self.test_xss_in_form(form, link)
                if is_form_vulnerable_to_xss:
                    print("\n\n[***] XSS discovered in the following form at " + link)
                    print(form)
                    print("\n\n")

            if "=" in link:
                is_link_vulnerable_to_xss = self.test_xss_in_link(link)
                if is_link_vulnerable_to_xss:
                    print("\n[***] XSS discovered at " + link + "\n\n")

    def test_xss_in_link(self, url):
        xss_test_script = "<sCript>alert('Hello')</scriPT>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.content

    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>alert('Hello')</scriPT>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.content
