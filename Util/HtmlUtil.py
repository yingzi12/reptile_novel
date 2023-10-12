import logging
import random
import time

import requests
import urllib3

from Util import LogUtil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def get_api_data(api_url,proxies,heads):
    try:
        response_text = send_request_using_proxy(api_url, proxies,heads)
        # response = session.get(api_url, headers=headers)
        # response.raise_for_status()
        return response_text
    except requests.exceptions.RequestException as e:
        LogUtil.error(f"Error making API request: {e}")
        return None

def get_api_data(url,headers={},isEncoding=True):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url, headers=headers, verify=False)  # Set verify=True to enable certificate verification
        # Check if the request was successful
        if response.status_code == 200:
            if (isEncoding):
                # 这里设置编码格式
                response.encoding = response.apparent_encoding
            return response.text
        else:
            return None
    except requests.exceptions.RequestException as e:
        LogUtil.error(f"Error making API request: {e}")
        return None
def send_request_using_proxy(url, proxies,headers):
    retries = 0
    max_retries=20
    delay_seconds=2
    while retries < max_retries:
        try:
            proxy = random.choice(proxies)
            LogUtil.info(f"Using proxy: {proxy}")
            response = requests.get(url, proxies={'http': proxy, 'https': proxy}, headers=headers, verify=False)
            if response.status_code == 200:
                return response.text
            else:
                LogUtil.info(f"Failed to make request. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            LogUtil.error(f"Error occurred: {e}")
        retries += 1
        LogUtil.info(f"Retrying... (Attempt {retries}/{max_retries})")
        time.sleep(delay_seconds)

    LogUtil.info(f"Max retries reached. Failed to get a successful response.")
    return None

def send_request_image_proxy(url, proxies,headers):
    try:
        proxy = random.choice(proxies)
        LogUtil.info(f"Using proxy: {proxy}")
        response = requests.get(url, proxies={'http': proxy, 'https': proxy},headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            LogUtil.error(f"Failed to make request. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        LogUtil.error(f"Error occurred: {e}")
        return None