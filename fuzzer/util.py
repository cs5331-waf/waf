def form_cookie(cookie_list):
    cookie_str = ""
    for cookie in cookie_list:
        cookie_str += cookie['name'] + "=" + cookie['value']
        cookie_str += "; "

    return {'Cookie': cookie_str}
