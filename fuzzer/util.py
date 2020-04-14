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


def clean_html(soup):
    """
    Remove all javascript and stylesheet code and
    cleanup whitespaces
    """

    # remove all javascript and stylesheet code
    for script in soup(["script", "style"]):
        script.extract()

    # note that `get_text` does not seperate text in different elements with '\n'
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # # break multi-headlines into a line each
    # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ' '.join(line for line in lines if line)

    return text
