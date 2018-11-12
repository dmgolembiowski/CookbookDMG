#!/usr/bin/env python3
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        # Just opens the browser
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
    
"""                                                                                                                                                                            2010 $ ./test.py
.
----------------------------------------------------------------------
Ran 1 test in 4.793s

OK
"""
# An extended example incorporating the java webdriver is available at:
# https://selenium-python.readthedocs.io/getting-started.html
