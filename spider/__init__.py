import requests
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse

import fuzzer
import vscanner
from spider.util import construct_full_url
import vul_database


class Spider:
    def __init__(self, driver_path="C:/Program Files (x86)/Google/Chrome/Application/"
                                   "chromedriver_win32/chromedriver.exe"):
        self.fuzzer = fuzzer.Fuzzer()
        self.vscanner = vscanner.Vscanner()
        options = webdriver.ChromeOptions()
        prefs = {
            "download.open_pdf_in_system_reader": False,
            "download.prompt_for_download": True,
            "plugins.always_open_pdf_externally": False
        }
        options.add_experimental_option(
            "prefs", prefs
        )
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def teardown(self):
        self.driver.close()

    def crawl(self, base_url, cred):
        visited_url_list = set()    # List of URL that were visited
        url_q = set()               # A queue to store URLs to visit
        web_app_config = defaultdict(list)
        vul_pages = set()

        url_q.add(base_url)
        parsed_base_url = urlparse(base_url)

        # Get characteristics of server
        rsp = requests.get(base_url, verify=False)
        server_type = rsp.headers['Server']
        print(server_type)

        while len(url_q) > 0:
            try:
                url = url_q.pop()
                visited_url_list.add(url)
                sites_found, vul_found = self.scrape_page(parsed_base_url, url, cred)
                for site in sites_found:
                    if site not in visited_url_list:
                        url_q.add(site)

                if vul_found.vul:
                    vul_pages.add(vul_found.url)
                    # If the vulnerability type has yet been classified
                    if vul_database.vul_list[(vul_found.vul, vul_found.vul_type)] not in web_app_config[vul_found.vul]:
                        web_app_config[vul_found.vul].append(vul_database.vul_list[(vul_found.vul,
                                                                                  vul_found.vul_type)])
            except Exception as e:
                print("Crawling failed", e, flush=True)

        return web_app_config, list(vul_pages)

    def scrape_page(self, parsed_base_url, url, cred):
        """
        Scrape the given URL for href in a tags and input tags to fuzz
        :param parsed_base_url: The base URL the spider started crawling from
        :param url: The URL to crawl
        :param cred: The credentials of the supplied account
        :return: a list of links found within the page
        """
        sites_found = []
        config_found = util.VulPage(None, None, None)

        try:
            self.driver.get(url)
            self.vscanner.vscan(self.vscanner, url, self.driver)
            input_els = self.driver.find_elements_by_tag_name("input")
            for input_el in input_els:
                # Find parent form element
                form_method = input_el.find_element_by_xpath("//form[1]").get_attribute("method")
                if "user" in input_el.get_attribute("name"):
                    input_el.clear()
                    input_el.send_keys(cred["USER_NAME"])
                elif "password" in input_el.get_attribute("type"):
                    input_el.clear()
                    input_el.send_keys(cred["PASS"])
                elif "submit" in input_el.get_attribute("type"):
                    input_el.click()
                else:
                    result = self.fuzzer.hpp_fuzz(self.driver, url, input_els, form_method)
                    if result:
                        config_found = util.VulPage(result[0], result[1], url)
                    break

            a_els = self.driver.find_elements_by_tag_name("a")
            for a_el in a_els:
                site_found = a_el.get_attribute("href")
                parsed_site_found = urlparse(site_found)
                # We do not want to visit anywhere that is not part of the web app
                if parsed_site_found.netloc == parsed_base_url.netloc:
                    sites_found.append(a_el.get_attribute("href"))
        except Exception as e:
            print("Error found in `scrape_page`:", e)

        return sites_found, config_found
