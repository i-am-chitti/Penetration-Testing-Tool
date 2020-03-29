#!/usr/bin/env python

# This script scans a website for different vulnerabilities in a website. It is supported by scanner.py file
# Specify the target_url and links to be ignored along with form_login_data for logging and creating session

import scanner

target_url = "http://10.0.2.8/dvwa/"
links_to_ignore = ["http://10.0.2.8/dvwa/logout.php"]
form_login_data = {"username": "admin", "password": "password", "Login": "submit"}

vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
# first logging in by submitting the form login data
response = vuln_scanner.session.post("http://10.0.2.8/dvwa/login.php", data=form_login_data)
# print(response.content)
vuln_scanner.crawl()
vuln_scanner.run_scanner()
