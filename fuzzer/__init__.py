import re
from bs4 import BeautifulSoup
from werkzeug.datastructures import MultiDict
from werkzeug.urls import url_encode

import fuzzer.util


class Fuzzer:
    def __init__(self):
        self.payloads = [
            ["var1"],
            ["var1", "var2"],
            ["var2", "var1"]
        ]

        self.err_msgs = [r".*Exception:", r".*Error: 'list'"]
        self.invalid_input_type = ["button", "hidden", "image", "submit", 'checkbox', 'radio']
        self.values = ["var1", "var2"]
        # Values that are more human in nature that are more suitable for search bars
        self.search_bar_val = ["overview", "references"]
        self.concat_values = [r"var1[^a-zA-Z\d\s:]+var2", r"var2[^a-zA-Z\d\s:]+var1"]

    def hpp_fuzz(self, driver, url, input_els, form_method):
        return self.p_scan(driver, url, input_els, form_method)

    def p_scan(self, driver, url, input_els, form_method):
        """
        Fuzz URL with parameter pollution payloads
        :param driver: web driver
        :param url: URL to send GET request
        :param input_els: Input elements to pollute
        :param form_method: method used to pass parameters
        :return:
        """
        para_name_list = []
        polluted_rsp = []
        random_str = util.generate_random_string()
        result = None

        for input_el in input_els:
            input_type = input_el.get_attribute("type")
            if input_type not in self.invalid_input_type:
                para_name_list.append(input_el.get_attribute("name"))

        # We iterate through all the parameters choosing 1 at each iteration
        for para_name in para_name_list:
            for payload in self.payloads:
                filtered_para = para_name_list.copy()
                filtered_para.remove(para_name)

                query_list = [(para_name, v) for v in payload]

                # For all the other input elements in the form we input a fixed random string
                for i in range(len(filtered_para)):
                    query_list.append((filtered_para[i], random_str))

                # Convert to MultiDict for easy encoding to query string
                query_str = url_encode(MultiDict(query_list))
                print("Method: {}, Query String: {}".format(form_method, query_str))
                if "get" in form_method :
                    url = url + "?" + query_str
                    # Use web driver to load URL, to let dynamic elements load
                    driver.get(url)
                elif "post" in form_method:
                    driver.get(url)
                    # Javascript code to execute POST request
                    driver.execute_script("""
                    var xhttp = new XMLHttpRequest();
                    xhttp.open('POST', '{}', true);
                    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                    xhttp.send('{}');
                    alert(xhttp.response);
                    """.format(url, query_str)
                    )
                else:
                    raise Exception("Unknown method to pass parameter values")

                rsp = driver.page_source
                result = self.check_arr_in_rsp(rsp, payload)
                if result:
                    return result

                soup = BeautifulSoup(rsp, "html.parser")
                cleaned_rsp = util.clean_html(soup)

                polluted_rsp.append(cleaned_rsp)

            result = self.p_test(polluted_rsp)
            if result:
                break

        return result

    def check_arr_in_rsp(self, rsp, payload):
        if len(payload) < 2: return None

        # Form "['var1','var2']" string
        arr_lit_regex = "\['" + "',\s*'".join(payload) + "'\]"

        # Look for array string literal
        if re.search(re.compile(arr_lit_regex), rsp):
            return 'HPP', 4

        # Look for compile error messages
        for err_msg in self.err_msgs:
            if re.search(err_msg, rsp):
                return 'HPP', 4

        return None

    def p_test(self, polluted_rsp):
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
                break

        # Search for presence of concatenated result
        for v in self.concat_values:
            for i in range(1, len(polluted_rsp)):
                if re.search(v, polluted_rsp[i]):
                    return 'HPP', 3

        if payload_found:
            if polluted_rsp[0] == polluted_rsp[1] == polluted_rsp[2]:
                return 'HPP', 0
            if polluted_rsp[0] == polluted_rsp[1]:
                return 'HPP', 1
            elif polluted_rsp[0] == polluted_rsp[2]:
                return 'HPP', 2

        return None

    def v_scan(self):
        pass
