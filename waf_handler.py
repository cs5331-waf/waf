from http.server import BaseHTTPRequestHandler,HTTPServer
from werkzeug import urls


class WAFHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        def check_para_pollution(url_path):
            qns_idx = url_path.find('?')
            if qns_idx > -1:
                url_path = url_path[qns_idx+1:]
                parameters = urls.url_decode(url_path).lists()
                for k, v in parameters:
                    if len(v) > 1:
                        return True
            return False

        path = self.path
        req_header = self.headers
        msg = ""

        if check_para_pollution(path):
            msg += u"HTTP parameter pollution detected"

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        if len(msg) == 0:
            msg = u"Hello World !"

        # Send the html message
        self.wfile.write(msg.encode("utf8"))
        return

    def do_POST(self):
        req_header = self.headers
