import fuzzer
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse

from spider.util import construct_full_url


class Spider:
    def __init__(self, driver_path="C:/Program Files (x86)/Google/Chrome/Application/"
                                   "chromedriver_win32/chromedriver.exe"):
        self.fuzzer = fuzzer.Fuzzer()
        self.driver = webdriver.Chrome(executable_path=driver_path)

    def teardown(self):
        self.driver.close()

    def crawl(self, base_url, cred):
        visited_url_list = set()    # List of URL that were visited
        url_q = set()               # A queue to store URLs to visit

        url_q.add(base_url)
        parsed_base_url = urlparse(base_url)
        while len(url_q) > 0:
            try:
                url = url_q.pop()
                visited_url_list.add(url)
                sites_found = self.scrape_page(parsed_base_url, url, cred)
                for site in sites_found:
                    if site not in visited_url_list:
                        url_q.add(site)
            except Exception as e:
                print("Crawling failed", e, flush=True)

    def scrape_page(self, parsed_base_url, url, cred):
        """
        Scrape the given URL for href in a tags and input tags to fuzz
        :param url: The URL to crawl
        :return: a list of links found within the page
        """
        sites_found = []
        try:
            self.driver.get(url)
            input_els = self.driver.find_elements_by_tag_name("input")
            for input_el in input_els:
                if "user" in input_el.get_attribute("name"):
                    input_el.clear()
                    input_el.send_keys(cred["USER_NAME"])
                elif "password" in input_el.get_attribute("type"):
                    input_el.clear()
                    input_el.send_keys(cred["PASS"])
                elif "submit" in input_el.get_attribute("type"):
                    input_el.click()
                else:
                    self.fuzzer.hpp_fuzz(url, input_els, self.driver.get_cookies())

            a_els = self.driver.find_elements_by_tag_name("a")
            for a_el in a_els:
                site_found = a_el.get_attribute("href")
                parsed_site_found = urlparse(site_found)
                # We do not want to visit anywhere that is not part of the web app
                if parsed_site_found.netloc == parsed_base_url.netloc:
                    sites_found.append(a_el.get_attribute("href"))
        except Exception as e:
            print(e)

        return sites_found

