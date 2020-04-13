# Extract all parameters of a page: In Query Str (URL), In links and forms of body
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs


def test_page(crafted_url):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-setuid-sandbox") 
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-dev-shm-using") 
    chrome_options.add_argument("--disable-extensions") 
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("start-maximized") 
    chrome_options.add_argument("disable-infobars") 
    chrome_options.add_argument("--headless")
    driver_path = '/usr/lib/chromium-browser/chromedriver' # Edit as needed
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)

    driver.get(crafted_url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all('a'):
        if link.has_attr('href') and "&hpp=test" in link.get('href'):
            return True

    forms = soup.find_all('form')


    for form in forms:
        body_params = {}
        if form.has_attr('action') and "&hpp=test" in form.get('action'):
            return true
    return False

chrome_options = Options()
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-setuid-sandbox") 
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-dev-shm-using") 
chrome_options.add_argument("--disable-extensions") 
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("start-maximized") 
chrome_options.add_argument("disable-infobars") 
chrome_options.add_argument("--headless")

driver_path = '/usr/lib/chromium-browser/chromedriver' # Edit as needed
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
curr_url = 'http://localhost/DVWA/vulnerabilities/xss_r/'
if '?' in curr_url:
    base_url = curr_url.rsplit('?', 1)[0]
else:
    base_url = curr_url.rsplit('#', 1)[0]


driver.get(curr_url)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

url_params = parse_qs(urlparse(curr_url).query)
body_params = {}

for link in soup.find_all('a'):
    if link.has_attr('href'):
        body_params.update(parse_qs(urlparse(link.get('href')).query))

forms = soup.find_all('form')

for form in forms:
    body_params = {}
    if form.has_attr('action'):
        body_params.update(parse_qs(urlparse(form.get('action')).query))

    for input in form.find_all('input'):
        input_type = input.get('type')
        if input_type in ['submit', 'reset', 'button', 'image']:
            continue
        if input.has_attr('name'):
            body_params.update({input['name']: input.get('value', '')})

driver.quit()

# After extraction, form into 3 groups
group_a = {k:v for k,v in url_params.items() if k in body_params}

group_b = {k:v for k,v in url_params.items() if k not in body_params}

group_c = {k:v for k,v in body_params.items() if k not in url_params}

# Test each parameter in each group
# Groups A&B require query string to be present in URL
for k,v in group_a.items():
    crafted_str = str(k) + '=' + str(v) + '%26hpp%3Dtest'
    crafted_url = base_url + '?' + crafted_str
    for name,val in url_params:
        if name != k:
            crafted_url = crafted_url + '&' + str(k) + '=' + str(v)
    if test_page(crafted_url):
        print("Page parameters potentially vulnerable to HPP\n")

for k,v in group_b.items():
    crafted_str = str(k) + '=' + str(v) + '%26hpp%3Dtest'
    crafted_url = base_url + '?' + crafted_str
    for name,val in url_params:
        if name != k:
            crafted_url = crafted_url + '&' + str(k) + '=' + str(v)
    if test_page(crafted_url):
        print("Page parameters potentially vulnerable to HPP\n")

for k,v in group_b.items():
    crafted_str = str(k) + '=' + str(v) + '%26hpp%3Dtest'
    crafted_url = base_url + '?' + crafted_str
    for name,val in url_params:
        if name != k:
            crafted_url = crafted_url + '&' + str(k) + '=' + str(v)
    if test_page(crafted_url):
        print("Page parameters potentially vulnerable to HPP\n")

# Add all parameters in c into 1 single URL
crafted_url = base_url + '?'
for k,v in group_c.items():
    crafted_str = str(k) + '=' + str(v)
    if crafted_url[-1] == '?':
        crafted_url = crafted_url + crafted_str
    else:
        crafted_url = crafted_url + '&' + crafted_str
crafted_url = crafted_url + '%26hpp%3Dtest'
if test_page(crafted_url):
    print("Page parameters potentially vulnerable to HPP\n")


