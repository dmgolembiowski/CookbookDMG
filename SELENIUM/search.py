#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# This next line creates a firefox GUI
driver = webdriver.Firefox()

# Submitting a websocket GET request
# (I'm pretty sure python doesn't do READ/WRITE requests)
driver.get("http://www.python.org")
assert "Python" in driver.title
# ^Not totally sure if this line actually returns True/False
# because it didn't when I ran it in idle
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()

"""
Useful webcrawling explanation at:
https://selenium-python.readthedocs.io/navigating.html
"""
