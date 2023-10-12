# This is a sample Python script.
import os
import time
import re
from PIL import Image
from io import BytesIO
from datetime import datetime
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from requests_html import HTMLSession

import json

from poxy import get_free_proxy_list, send_request_using_proxy, send_request_image_proxy

MAX_THREADS = 5  # Set the maximum number of threads for downloading images
session = HTMLSession()

out_file="E:\\folder\\hotgirl\\"
headers = {
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "referer": "https://everia.club",
    "sec-ch-ua": 'Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": 'macOS',
    "sec-fetch-dest": 'empty',
    "sec-fetch-mode": 'cors',
    "sec-fetch-site": 'same-origin',
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def get_api_data(api_url,proxies):
    try:
        response_text = send_request_using_proxy(api_url, proxies)
        # response = session.get(api_url, headers=headers)
        # response.raise_for_status()
        return response_text
    except requests.exceptions.RequestException as e:
        svae_log_file(f"Error making API request: {e}")
        print(f"Error making API request: {e}")
        return None
def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{directory_path}': {e}")
    else:
        print(f"Directory '{directory_path}' already exists.")

def remove_special_characters_and_escape_spaces(input_string):
    # 使用正则表达式匹配中文、日文、数字和英文字符
    pattern = r'[^\u4e00-\u9fa5\u3040-\u30FF\u3131-\u318E\uAC00-\uD7A3a-zA-Z0-9]'
    # 将匹配到的字符替换为下划线
    result = re.sub(pattern, '_', input_string)
    return result
def download_image(href_attribute,url, save_path,proxies):
    try:
        # 取消空格转义
        url = url.strip()

        filename = os.path.basename(url)
        if(has_file_extension(filename,"jpg") == False):
            timestamp_milliseconds = int(time.time() * 1000)
            save_image_from_url(url,save_path+"/"+str(timestamp_milliseconds)+".png")
        else:
            # Send an HTTP request to the URL
            response = send_request_image_proxy(url, proxies);
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            # Save the content of the response (image) to a file
            with open(save_path+"/"+filename, 'wb') as file:
                file.write(response.content)
        #print("Image downloaded successfully.")
    except requests.exceptions.RequestException as e:
        svae_log_file(f"Error {href_attribute} downloading {url} the image: {e}")
        print(f"Error downloading the image: {e}")

def save_image_from_url(url, save_path,proxies):
    image_format = "PNG"  # 可以替换为 "PNG" 等其他支持的格式
    image_data  = requests.get(url, headers=headers).content
    if image_data:
        image = Image.open(BytesIO(image_data))
        image.save(save_path, format=image_format)
       # print(f"Image saved as {image_format} format: {save_path}")
    else:
        svae_log_file(f"Error Image download failed.: {url}")
        print("Image download failed.")
def download_images_in_parallel(image_element,save_path):
    img_cen = image_element.xpath('.//img')[0]
    dataUrl = img_cen.get('data-src')
    data_id = img_cen.get('data-id')
    #print("dataUrl:", dataUrl)
    #print("data_id:", data_id)

    download_image(dataUrl,save_path)

def svae_log_file(content_to_print):
    # 打开文件并写入内容
    file_path = "output_hotgirl.txt"  # 文件路径，可以是相对路径或绝对路径
    # 获取当前时间
    current_time = datetime.now()

    # 定义想要的时间格式
    time_format = "%Y-%m-%d %H:%M:%S"  # 例如："2023-08-03 10:30:45"

    # 格式化当前时间
    formatted_time = current_time.strftime(time_format)
    content_to_print=formatted_time+" "+ content_to_print+" \n"
    with open(file_path, 'a') as file:
        file.write(content_to_print)


def has_file_extension(filename, extension):
    return filename.endswith(extension)

def page(href_attribute,save_path,proxies):
    image_data = get_api_data(href_attribute,proxies)

    imageTree = etree.fromstring(image_data, etree.HTMLParser())
    main_element = imageTree.xpath("//div[@class='main-content main-detail']")[0]
    img_elements = main_element.xpath("//div[@class='galeria_img']")

    # 提取ignore_js_op标签里的img标签的属性
    for ignore_js_op in img_elements:
        img_elements = ignore_js_op.xpath('.//img')
        for img in img_elements:
            img_src = img.get('src')
            download_image(href_attribute, img_src, save_path)

def process_page(page_number,proxies):
    api_url = "https://hotgirl.asia/photos/page/{}/"

    # for i in range(page, pageCount + 1):
    formatted_url = api_url.format(page_number)
    api_data = get_api_data(formatted_url,proxies)
    print(f"api_url '{formatted_url}' ")
    svae_log_file(f"api_url '{formatted_url}' ")
    tree = etree.fromstring(api_data, etree.HTMLParser())

    # 查找id为"waterfall"的ul元素
    ul_element = tree.xpath("//div[@class='movies-list movies-list-full']")[0]
    # 获取ul元素中所有li元素
    li_elements = ul_element.xpath("//div[@class='ml-item']")
    # 遍历每个li元素，并获取a标签的href属性值
    for li_element in li_elements:
        a_element = li_element.xpath(".//a")[0]
        href_attribute = a_element.get("href")
        title = a_element.get("oldtitle")
        image_data = get_api_data(href_attribute,proxies)
        title = remove_special_characters_and_escape_spaces(title)

        save_path = out_file + "/" + title + "_" + str(time.time())
        create_directory_if_not_exists(save_path)
        imageTree = etree.fromstring(image_data, etree.HTMLParser())
        main_element = imageTree.xpath("//div[@class='main-content main-detail']")[0]
        img_elements = main_element.xpath("//div[@class='galeria_img']")

        # 提取ignore_js_op标签里的img标签的属性
        for ignore_js_op in img_elements:
            img_elements = ignore_js_op.xpath('.//img')
            for img in img_elements:
                img_src = img.get('src')
                download_image(href_attribute,img_src, save_path)
               # print(f" img_src: {img_src}")
                # img_cen = image_element.xpath('.//img')[0]
                # data_src = img_cen.get('data-src')
                # data_id = img_cen.get('data-id')
                # print("data_src:", data_src)
                # print("data_id:", data_id)
                # download_images_in_parallel(image_element, save_path)

        page_elements = main_element.xpath("//div[@class='page larger']")
        for page_element in page_elements:
            page_url = page_element.get("src")
            page(page_url, save_path,proxies)
    else:
        print("No <div> element with class 'nv-post-thumbnail-wrap img-wrap' found in the HTML.")

def print_hi(name):
    proxies = get_free_proxy_list()

    page = 180
    # page_count = 1892
    page_count=180
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for page_number in range(page, page_count + 1):
            executor.submit(process_page, page_number,proxies)

    print(f'Hi, {name}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/