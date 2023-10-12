# This is a sample Python script.
import os

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from requests_html import HTMLSession

import json
MAX_THREADS = 5  # Set the maximum number of threads for downloading images
session = HTMLSession()

out_file="E:\\folder\\jkforum\\"
heard_url="https://www.jkforum.net/"
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
def get_api_data(api_url):
    try:
        response = session.get(api_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
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


def download_image(url, save_path):
    try:
        # Send an HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        filename = os.path.basename(url)

        # Save the content of the response (image) to a file
        with open(save_path+"/"+filename, 'wb') as file:
            file.write(response.content)

        #print("Image downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")

def download_images_in_parallel(image_element,save_path):
    img_cen = image_element.xpath('.//img')[0]
    dataUrl = img_cen.get('data-src')
    data_id = img_cen.get('data-id')
    #print("dataUrl:", dataUrl)
    #print("data_id:", data_id)

    download_image(dataUrl,save_path)
def process_page(page_number):
    api_url = "https://www.jkforum.net/forum-234-{}.html"

    # for i in range(page, pageCount + 1):
    formatted_url = api_url.format(page_number)
    print(f"api_url '{formatted_url}' ")
    api_data = get_api_data(formatted_url)

    tree = etree.fromstring(api_data, etree.HTMLParser())

    # 查找id为"waterfall"的ul元素
    ul_element = tree.xpath("//ul[@id='waterfall']")[0]
    # 获取ul元素中所有li元素
    li_elements = ul_element.xpath(".//li")
    # 遍历每个li元素，并获取a标签的href属性值
    for li_element in li_elements:
        a_element = li_element.xpath(".//a")[0]
        href_attribute = a_element.get("href")
        title = a_element.get("title")
        image_data = get_api_data(heard_url+href_attribute)
        save_path = out_file + "/" + title + "_" + str(href_attribute)
        create_directory_if_not_exists(save_path)
        imageTree = etree.fromstring(image_data, etree.HTMLParser())
        post_element = imageTree.xpath("//div[@class='post first']")[0]
        post_bd = post_element.xpath("//div[@class='post-bd']")[0]
        # 获取所有的ignore_js_op标签
        ignore_js_op_elements = post_bd.xpath('//ignore_js_op')

        # 提取ignore_js_op标签里的img标签的属性
        for ignore_js_op in ignore_js_op_elements:
            img_elements = ignore_js_op.xpath('.//img')
            for img in img_elements:
                img_id = img.get('id')
                img_aid = img.get('aid')
                img_src = img.get('file')
                download_image(img_src, save_path)
                #print(f"img_id: {img_id}, img_aid: {img_aid}, img_src: {img_src}")
                # img_cen = image_element.xpath('.//img')[0]
                # data_src = img_cen.get('data-src')
                # data_id = img_cen.get('data-id')
                # print("data_src:", data_src)
                # print("data_id:", data_id)
                # download_images_in_parallel(image_element, save_path)


    else:
        print("No <div> element with class 'nv-post-thumbnail-wrap img-wrap' found in the HTML.")

def print_hi(name):

    page = 1
    page_count = 4546
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for page_number in range(1, page_count + 1):
            executor.submit(process_page, page_number)

    print(f'Hi, {name}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/