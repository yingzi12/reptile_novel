import requests
from bs4 import BeautifulSoup
import random
from requests_html import HTMLSession
import time

session = HTMLSession()
headers = {
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": 'Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": 'macOS',
    "sec-fetch-dest": 'empty',
    "sec-fetch-mode": 'cors',
    "sec-fetch-site": 'same-origin',
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

def get_free_proxy_list():
    url = "https://www.sslproxies.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_list = []
    table = soup.find('table', class_='table table-striped table-bordered')

    for row in table.find_all('tr'):
        columns = row.select("td")
        if len(columns) >= 7 and columns[6].text == "yes":
            proxy = f"{columns[0].text}:{columns[1].text}"
            proxy_list.append(proxy)

    return proxy_list

def send_request_using_proxy(url, proxies):
    retries = 0
    max_retries=20
    delay_seconds=2
    while retries < max_retries:
        try:
            proxy = random.choice(proxies)
            print(f"Using proxy: {proxy}")
            response = requests.get(url, proxies={'http': proxy, 'https': proxy}, headers=headers, verify=False)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to make request. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
        retries += 1
        print(f"Retrying... (Attempt {retries}/{max_retries})")
        time.sleep(delay_seconds)

    print(f"Max retries reached. Failed to get a successful response.")
    return None

def send_request_image_proxy(url, proxies):
    try:
        proxy = random.choice(proxies)
        print(f"Using proxy: {proxy}")
        response = requests.get(url, proxies={'http': proxy, 'https': proxy},headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to make request. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

# 示例用法
url = "https://www.google.com/"
proxies = get_free_proxy_list()

response_text = send_request_using_proxy(url, proxies)
if response_text:
    print(response_text)
