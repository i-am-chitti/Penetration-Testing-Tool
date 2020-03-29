#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import urlparse


# This script extracts all the form from a given url and then submits it with the value 'test' if
# the input field type is 'text' else default value is submitted

def request(url):
    return requests.get(url)


# extracting all the forms that are present in this url
target_url = "http://10.0.2.8/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)
# parsing the response content
parse_html = BeautifulSoup(response.content, 'html.parser')
# findAll returns the list containing the provided element
forms_list = parse_html.findAll("form")

# submitting the form
for form in forms_list:

    # getting the attribute 'action' value
    form_action_link = form.get("action")
    # link may be relative. So, we have to convert it using urlpasrse
    form_action_link = urlparse.urljoin(target_url, form_action_link)

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
            input_field_value = "test"

        # binding each input field value into dictionary element
        post_data[input_field_name] = input_field_value

    result = requests.post(form_action_link, data=post_data)
    print(result.content)
