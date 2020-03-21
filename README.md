# CS5331 Web Application Firewall (WAF)

Tested using Python 3.6.4.

### Requirements
Below are the python packages required:
* `werkzeug`

Use `pip` to install the required packages before running the program.

## Instructions to use
To start the WAF, use `python main.py <port-to-listen> <web-app-port>`.

`waf_handler.py` handles the functionality of the WAF. The `do_GET`
and `do_POST` methods of the handler handles the respective requests.
Thus, to add functionalities, edit the respective methods.
