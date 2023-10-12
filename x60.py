# This is a sample Python script.
import os

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

import json
MAX_THREADS = 5  # Set the maximum number of threads for downloading images

out_file="E:\\folder\\x6o\\"

headers = {
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "referer": "https://www.x6o.com/topics/14",
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
        response = requests.get(api_url,headers=headers)
        response.raise_for_status()  # 检查是否有错误
        # 手动指定编码方式为UTF-8
        # response.encoding = 'utf-8'
        # 解析JSON数据
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
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

def download_images_in_parallel(article_data):
    article_id = article_data['article_id']
    title = article_data['title']
    content_rendered = article_data['content_rendered']

    soup = BeautifulSoup(content_rendered, 'html.parser')

    save_path = out_file + "/" + title + "_" + str(article_id)
    create_directory_if_not_exists(save_path)

    figure_tags = soup.find_all('figure')
    data_original_values = [figure.img.get('data-original') for figure in figure_tags]

    # Download images concurrently using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for dataUrl in data_original_values:
            executor.submit(download_image, dataUrl, save_path)

def print_hi(name):
    api_url = "https://www.x6o.com/api/topics/14/articles?page={}&per_page=100&order=-create_time&include=user%2Ctopics%2Cis_following"

    page = 1
    pageCount = 88

    for i in range(page, pageCount + 1):
        formatted_url = api_url.format(i)
        api_data = get_api_data(formatted_url)

        if api_data:
            articles = api_data['data']
            print("下载"+"  "+formatted_url)
            # Download images in parallel for each article
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                executor.map(download_images_in_parallel, articles)
        else:
            print("Failed to get API data.")

    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/