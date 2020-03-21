from http.server import BaseHTTPRequestHandler,HTTPServer


class WAFHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        req_header = self.headers
        print(req_header)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        msg = u"Hello World !"
        self.wfile.write(msg.encode("utf8"))
        return