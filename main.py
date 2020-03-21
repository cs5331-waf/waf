from http.server import HTTPServer
import waf_handler
import sys
import time



def main(config):
    waf_server = HTTPServer((config["HOST_NAME"], config["LISTEN_PORT"]), waf_handler.WAFHandler)
    print(time.asctime(), "WAF started listening at %s:%s" % (config["HOST_NAME"], config["LISTEN_PORT"]))

    try:
        waf_server.serve_forever()
    except KeyboardInterrupt:
        waf_server.server_close()

    print(time.asctime(), "WAF stopped listening listening")


if __name__ == "__main__":
    server_config = dict()
    server_config["LISTEN_PORT"] = int(sys.argv[1])
    server_config["APP_PORT"] = int(sys.argv[2])
    server_config["HOST_NAME"] = '127.0.0.1'
    main(server_config)