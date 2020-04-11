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
    web_app_config = app_spider.crawl(config["APP_ADDRESS"], cred)

    print(web_app_config)
    app_spider.teardown()
    print(time.asctime(), "WAF finished crawling")


if __name__ == "__main__":
    server_config = dict()
    server_config["APP_ADDRESS"] = sys.argv[1]
    main(server_config)
