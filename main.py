#from waf import WAFHandler, WAFServer
import spider
import sys
import time


def main(config):

    app_spider = spider.Spider()
    user_rsp = input("Does the web application require authentication: [y/n]")
    cred = dict()
    if user_rsp is "y" or user_rsp is "Y":
        cred["USER_NAME"] = input("Username: ")
        cred["PASS"] = input("Password: ")

    print(time.asctime(), "Web App Spider started crawling %s" % (config["APP_ADDRESS"]))
    app_spider.crawl(config["APP_ADDRESS"], cred)

    # waf_server = WAFServer((config["HOST_NAME"], config["LISTEN_PORT"]), WAFHandler, config["APP_ADDRESS"])
    # print(time.asctime(), "WAF started listening at %s:%s" % (config["HOST_NAME"], config["LISTEN_PORT"]))
    #
    # try:
    #     waf_server.serve_forever()
    # except KeyboardInterrupt:
    #     waf_server.server_close()
    #

    app_spider.teardown()
    print(time.asctime(), "WAF finished crawling")


if __name__ == "__main__":
    server_config = dict()
    #server_config["LISTEN_PORT"] = int(sys.argv[1])
    server_config["APP_ADDRESS"] = sys.argv[1]
    #server_config["HOST_NAME"] = '127.0.0.1'
    main(server_config)
