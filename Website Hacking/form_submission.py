#!/usr/bin/env python

import requests

# This script just submits a details to a form url

target_url = "http://10.0.2.8/dvwa/login.php"
# value for submit button in dictionary = value of 'type' attribute in html code
form_data = {"username": "admin", "password": "password", "Login": "submit"}
response = requests.post(target_url, data=form_data)
print(response.content)