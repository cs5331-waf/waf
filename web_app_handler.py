import re

class WebAppHandler:
    def __init__(self, app_address):
        self.app_address = app_address
        self.host_header = {'Host': app_address}
        self.IP_REGEX = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d{1,5})*"
        self.REFERER_KEY = "Referer"

    def update_headers_req_url(self, old, path):
        new = old.copy()
        if self.REFERER_KEY in new:
            ref_val = new[self.REFERER_KEY]
            # Replace the proxy's IP with the actual web application IP
            ref_val = re.sub(self.IP_REGEX, self.app_address, ref_val)
            #print("Ref_val: {}".format(ref_val))
            url = ref_val + path[1:] if ref_val[-1] == '/' else ref_val + path
        else:
            url = "http://{}".format(self.app_address)

        #print("URL: {}".format(url))
        new.update(self.host_header)
        return new, url
