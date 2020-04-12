import re
from bs4 import BeautifulSoup
from werkzeug.datastructures import MultiDict
from werkzeug.urls import url_encode

import fuzzer.util
import vul_database

class Fuzzer:
    def __init__(self):
        #   ["var1,var2"],
        #   ["var1,var2", "var3"]

        self.payloads = [
            ["var1"],
            ["var1", "var2"],
            ["var2", "var1"]
        ]

        self.invalid_input_type = ["submit", "button", "hidden"]
        self.values = ["var1", "var2"]
        self.concat_values = ["var1,var2", "var2,var1"]
        self.invalid_rsp_code = ["500"]

    def hpp_fuzz(self, driver, url, input_els, cookie_list):
        """
        Fuzz URL with parameter pollution payloads
        :param url: URL to send GET request
        :param input_el: Input element to pollute
        :return:
        """
        para_name_list = []
        polluted_rsp = []
        random_str = util.generate_random_string()

        for input_el in input_els:
            input_type = input_el.get_attribute("type")
            if input_type not in self.invalid_input_type:
                para_name = input_el.get_attribute("name")
                para_name_list.append(para_name)

        for payload in self.payloads:
            # Convert to MultiDict for easy encoding to query string
            query_list = [(para_name_list[0], v) for v in payload]
            # For all the other input elements in the form we input a fixed random string
            for i in range(1, len(para_name_list)):
                query_list.append((para_name_list[i], random_str))

            query_str = url_encode(MultiDict(query_list))
            get_url = url + "?" + query_str

            print("Fuzzing ", get_url)

            # Use web driver to load URL, to let dynamic elements load
            driver.get(get_url)
            rsp = driver.page_source

            soup = BeautifulSoup(rsp, "html.parser")

            # Check for response status code
            rsp_check = [soup.find(text=re.compile(rsp_code)) for rsp_code in self.invalid_rsp_code]
            rsp_check = [check for check in rsp_check if check]

            # We do not add error response to the list
            if len(rsp_check) == 0:
                cleaned_rsp = util.clean_html(soup)
                polluted_rsp.append(cleaned_rsp)

        return self.compare_rsp(polluted_rsp)

    def compare_rsp(self, polluted_rsp):
        """
        Compares the polluted responses from the server to determine
        :param polluted_rsp: Responses from server
        :return:
        """

        # To prevent false positives, we check for the payload in the unpolluted request
        payload_found = False
        for v in self.values:
            if v in polluted_rsp[0]:
                payload_found = True

        # If there is only 1 response without errors - the unpolluted response
        if len(polluted_rsp) == 1:
            return ('HPP', 4), vul_database.vul_list[('HPP', 4)]

        # Search for presence of concatenated result
        for v in self.concat_values:
            for i in range(1, len(polluted_rsp)):
                if v in polluted_rsp[i]:
                    return ('HPP', 3), vul_database.vul_list[('HPP', 3)]

        if payload_found:
            if polluted_rsp[0] == polluted_rsp[1] == polluted_rsp[2]:
                return ('HPP', 0), vul_database.vul_list[('HPP', 0)]
            if polluted_rsp[0] == polluted_rsp[1]:
                return ('HPP', 1), vul_database.vul_list[('HPP', 1)]
            elif polluted_rsp[0] == polluted_rsp[2]:
                return ('HPP', 2), vul_database.vul_list[('HPP', 2)]

        return None
