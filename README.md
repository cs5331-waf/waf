# CS5331 Web Application Firewall (WAF)

Tested using Python 3.6.4. Our web app spider which looks for input elements within the web application 
and crafts payloads to test the configuration of the server.  

Note: This WAF works only on Windows and not Linux.

### Requirements
Below are the python packages required:
* `werkzeug`
* `beautifulsoup`
* `selenium`: choice of browser is chrome which requires `chromedriver`


Use `pip` to install the required packages before running the program.

## Instructions to use
To start the WAF, use `python main.py <web-app-address>`. Examples:
* `python main.py 192.168.30.30/dvwa/login.php`
