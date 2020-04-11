import requests
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
        self.values = ["var1", "var2", "var3"]

    def hpp_fuzz(self, url, input_els, cookie_list):
        """
        Fuzz URL with parameter pollution payloads
        :param url: URL to send GET request
        :param input_el: Input element to pollute
        :return:
        """
        para_name_list = []
        polluted_rsp = []
        random_str = util.generate_random_string()
        cookie = util.form_cookie(cookie_list)

        for input_el in input_els:
            type = input_el.get_attribute("type")
            if type not in self.invalid_input_type:
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

            rsp = requests.get(get_url, verify=False, headers=cookie)

            # util.display_in_browser(rsp)
            polluted_rsp.append(rsp.content)

        return self.compare_rsp(polluted_rsp)

    def compare_rsp(self, polluted_rsp):
        """
        Compares the polluted responses from the server to determine
        :param polluted_rsp: Response from server
        :return:
        """
        # TODO: Need to find payload in the response as well
        if polluted_rsp[0] == polluted_rsp[1] == polluted_rsp[2]:
            return ('HPP', 0), vul_database.vul_list[('HPP', 0)]
        if polluted_rsp[0] == polluted_rsp[1]:
            return ('HPP', 1), vul_database.vul_list[('HPP', 1)]
        elif polluted_rsp[0] == polluted_rsp[2]:
            return ('HPP', 2), vul_database.vul_list[('HPP', 2)]
