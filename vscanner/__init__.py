# Extract all parameters of a page: In Query Str (URL), In links and forms of body
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs

class Vscanner:
    def __init__(self):
        self.ignored_input_type = ['submit', 'reset', 'button', 'image']
        self.pollute_str = '%26hppollution%3Dtest'
        self.vuln_pages = []

    def get_vuln_pages(self):
        return self.get_vuln_pages

    def log_vuln_pages(self, grp_type, vuln_url, vuln_param):
        if grp_type == "C":
            str = "Type C: Base Url: " + vuln_url + " has links containing injected paramters"
            self.vuln_pages.append(str)
        else:
            str = "Type " + grp_type + ": Base Url: " + vuln_url + " Polluted Parameter: " + vuln_param
                    + " [Page has links containing injected parameters]"
            self.vuln_pages.append(str)

    def test_page(self, crafted_url, driver):
        driver.get(crafted_url)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        for link in soup.find_all('a'):
            if link.has_attr('href') and self.pollute_str in link.get('href'):
                return True

        forms = soup.find_all('form')

        for form in forms:
            body_params = {}
            if form.has_attr('action') and self.pollute_str in form.get('action'):
                return True
        return False

    def vscan(self, url, driver, url_response):
        base_url = ""
        if '?' in url:
            base_url = url.rsplit('?', 1)[0]
        else:
            base_url = url.rsplit('#', 1)[0]

        driver.get(url)

        html = url_response
        soup = BeautifulSoup(html, "html.parser")

        url_params = parse_qs(urlparse(curr_url).query)
        body_params = {}

        for link in soup.find_all('a'):
            if link.has_attr('href'):
                body_params.update(parse_qs(urlparse(link.get('href')).query))

        forms = soup.find_all('form')

        for form in forms:
            body_params = {}
            if form.has_attr('action'):
                body_params.update(parse_qs(urlparse(form.get('action')).query))

        for input in form.find_all('input'):
            input_type = input.get('type')
            if input_type in self.ignored_input_type:
                continue
            if input.has_attr('name'):
                body_params.update({input['name']: input.get('value', '')})\

        # After extraction, form into 3 groups
        group_a = {k:v for k,v in url_params.items() if k in body_params}

        group_b = {k:v for k,v in url_params.items() if k not in body_params}

        group_c = {k:v for k,v in body_params.items() if k not in url_params}

        # Test each parameter in each group
        # Groups A&B require query string to be present in URL
        for k,v in group_a.items():
            crafted_str = str(k) + '=' + str(v) + self.pollute_str
            crafted_url = base_url + '?' + crafted_str
            for name,val in url_params:
                if name != k:
                    crafted_url = crafted_url + '&' + str(k) + '=' + str(v)
                if test_page(self, crafted_url, driver):
                    log_vuln_pages(self, 'A', base_url, name)

        for k,v in group_b.items():
            crafted_str = str(k) + '=' + str(v) + self.pollute_str
            crafted_url = base_url + '?' + crafted_str
            for name,val in url_params:
                if name != k:
                    crafted_url = crafted_url + '&' + str(k) + '=' + str(v)
                if test_page(self, crafted_url, driver):
                    log_vuln_pages(self, 'B', base_url, name)

        # Add all parameters in c into 1 single URL
        crafted_url = base_url + '?'
        for k,v in group_c.items():
            crafted_str = str(k) + '=' + str(v)
            if crafted_url[-1] == '?':
                crafted_url = crafted_url + crafted_str
            else:
                crafted_url = crafted_url + '&' + crafted_str
        crafted_url = crafted_url + self.pollute_str
        if test_page(self, crafted_url, driver):
            log_vuln_pages(self, 'C', base_url, 'NIL')
