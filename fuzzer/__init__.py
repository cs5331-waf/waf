import requests
from werkzeug.datastructures import MultiDict
from werkzeug.urls import url_encode
from bs4 import BeautifulSoup

from fuzzer.util import form_cookie

class Fuzzer:
    def __init__(self):
        self.payloads = [
            ["var1", "var2"],
            ["var1,var2"],
            ["var1,var2", "var3"]
        ]
        self.values = ["var1", "var2", "var3"]

    def hpp_fuzz(self, url, input_el, cookie_list):
        """
        Fuzz URL with parameter pollution payloads
        :param url: URL to send GET request
        :param input_el: Input element to pollute
        :return:
        """

        cookie = form_cookie(cookie_list)

        para_name = input_el.get_attribute("name")
        for payload in self.payloads:
            # Convert to MultiDict for easy encoding to query string
            query_dict = MultiDict([(para_name, v) for v in payload])
            query_str = url_encode(query_dict)
            get_url = url + "?" + query_str

            print("Fuzzing ", get_url)
            # Send request
            rsp = requests.get(get_url, headers=cookie)
            self.find_val(rsp, payload)

    def find_val(self, rsp, payload):
        """
        Find payload (parameter value) in response page
        :param rsp: Response from server
        :param payload: Payload sent to server
        :return:
        """
        soup = BeautifulSoup(rsp.content, "html.parser")

        # Try to find parameter value in the response page
        for idx, value in zip(range(len(self.values)), self.values):
            if len(soup.find_all(string=value)) > 0:
                self.analyse_behaviour(idx)

    def analyse_behaviour(self, idx):
        print("payload found in response ", idx)


