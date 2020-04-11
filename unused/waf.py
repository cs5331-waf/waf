# from web_app_handler import WebAppHandler
# from http.server import BaseHTTPRequestHandler,HTTPServer
# from werkzeug import urls
# import requests
#
#
# # Class necessary to pass in `app_address` argument
# class WAFServer(HTTPServer):
#     def __init__(self, server_address, RequestHandlerClass, app_address):
#         HTTPServer.__init__(self, server_address, RequestHandlerClass)
#         self.web_app_handler = WebAppHandler(app_address)
#
#
# class WAFHandler(BaseHTTPRequestHandler):
#     def __init__(self, request, client_address, server):
#         BaseHTTPRequestHandler.__init__(self, request, client_address, server)
#
#     # Handler for the GET requests
#     def do_GET(self):
#         def check_para_pollution(url_path):
#             qns_idx = url_path.find('?')
#             if qns_idx > -1:
#                 url_path = url_path[qns_idx+1:]
#                 parameters = urls.url_decode(url_path).lists()
#                 for k, v in parameters:
#                     if len(v) > 1 and "[]" not in k:
#                         return True
#             return False
#
#         msg = b""
#
#         if check_para_pollution(self.path):
#             msg += b"HTTP parameter pollution detected"
#
#         # If no malicious content is detected, then we send the request to the server
#         if len(msg) == 0:
#             old_headers = self.parse_headers()
#             new_headers, url = self.server.web_app_handler.update_headers_req_url(old_headers, self.path)
#             response = requests.get(url, headers=new_headers, verify=False)
#             self.send_response(response.status_code)
#             self.send_response_headers(response)
#             msg = response.content
#
#         # Send the html message
#         self.wfile.write(msg)
#         return
#
#     def do_POST(self):
#         req_header = self.headers
#
#     def parse_headers(self):
#         req_headers = {}
#         for k, v in self.headers.items():
#             req_headers[k] = v
#         return req_headers
#
#     def send_response_headers(self, response):
#         headers = response.headers
#         for k in headers:
#             if k not in ['Content-Encoding', 'Content-Length']:
#                 self.send_header(k, headers[k])
#         self.send_header('Content-Length', len(response.content))
#         self.end_headers()
#
#     def send_response_headers_stub(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
