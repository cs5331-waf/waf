import random
import string
import webbrowser



def form_cookie(cookie_list):
    cookie_str = ""
    for cookie in cookie_list:
        cookie_str += cookie['name'] + "=" + cookie['value']
        cookie_str += "; "

    return {'Cookie': cookie_str}


def display_in_browser(rsp, file_name="response.html"):
    with open(file_name, "w") as f:
        for line in rsp.text:
            f.write(line)

    webbrowser.open_new(file_name)


def generate_random_string(n=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))
