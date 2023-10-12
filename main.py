import os
import sys
import time
import concurrent.futures
import requests
from requests_html import HTMLSession
from lxml import etree

urltemplate = "https://xchina.co/photos/kind-1/{}.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44",
    "Content-Type": "text/html;charset=UTF-8"
}
session = HTMLSession()

pdictemplate = "E:\\folder\\xchina\\{}\\"
error_file = "E:\\folder\\xchina\\error.txt"

def download_image(fname, furl):
    response = requests.get(furl)
    if response.status_code == 200:
        with open(fname, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

def download_video(fname, furl):
    response = requests.get(furl, stream=True, headers=headers)
    response.raise_for_status()
    with open(fname, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def get_page_html(pageurl):
    retries = 3
    while retries > 0:
        try:
            response = session.get(pageurl, headers=headers)
            response.raise_for_status()
            return response.html.html
        except requests.exceptions.RequestException as e:
            retries -= 1
            print(f"Error downloading page content: {e}. Retrying {retries} more times...")
            time.sleep(20)
    return None

def download_page_content(starturl):
    resphtmltext = get_page_html(starturl)
    if resphtmltext is None:
        write_to_file(error_file, starturl + "\r\n")
        return

    resphtml = etree.HTML(resphtmltext)
    items = resphtml.xpath('//div[@class="item"]')
    itemindex = 1

    for item in items:
        # ... Rest of the code for processing each item ...
        # (Please keep the existing code as is for item processing)
        suburl = "https://xchina.co{}".format(item.xpath('a/@href')[0])
        filename = os.path.basename(suburl)

        platname = item.xpath('div[1]/div[1]/a/text()')[0]
        modelname = item.xpath('div[1]/div[2]/a/text()')
        if (len(modelname) == 0):
            modelname = "无名"
        else:
            modelname = modelname[0]
        title = item.xpath('div[2]/a/text()')[0]
        piccountstr = item.xpath('div[4]/div[1]/text()')[0]
        piccount = piccountstr.split("P")[0]
        print("title:{} piccountstr：{} piccount：{}】下载开始".format(title, piccountstr, piccount))
        subfolder = pdictemplate.format("{}_{}_{}[{}]_{}".format(
            modelname.strip(), platname.strip(), title.strip(), piccountstr,filename))
        if (not os.path.exists(subfolder)):
            os.makedirs(subfolder)

        subhtmltext = get_page_html(suburl)
        if (subhtmltext == "failed"):
            write_to_file(error_file, suburl + "\r\n")
            print("请求超时")
            sys.exit()
        subhtml = etree.HTML(subhtmltext)
        pages = subhtml.xpath('//div[@class="pager"]/div/a')
        totalpage = 0
        if (len(pages) == 0):
            totalpage = 1
        else:
            totalpage = pages[len(pages) - 2].xpath('text()')[0]
        imgindex = 1
        for j in range(1, int(totalpage) + 1):
            imgpageurl = suburl.replace(os.path.splitext(suburl)[-1], "")
            imgpageurl = imgpageurl + "/{}.html"
            imgpageurl = imgpageurl.format(j)
            imgpagehtmltext = get_page_html(imgpageurl)
            if (imgpagehtmltext == "failed"):
                write_to_file(error_file, imgpageurl + "\r\n")
                print("请求超时")
                sys.exit()
            imgpagehtml = etree.HTML(imgpagehtmltext)
            videos = imgpagehtml.xpath('//video[@class="player"]/source/@src')
            if (len(videos) > 0):
                videourl = videos[0]
                videoname = "{}{}".format(subfolder, os.path.basename(videourl))

                download_video(videoname, videourl)
                print("page vedoo:{}【{}/{}】_{}-{}下载完毕".format(i, itemindex, len(items),
                                                                  title, videoname))
            # 找到包含JSON数据的<script>标签
            script_tag = imgpagehtml.xpath('//script[contains(text(), "var videos = ")]')
            if script_tag:
                write_to_file(error_file, imgpageurl + "\r\n")
            #     # 找到包含domain的脚本部分
            #     script_tag = imgpagehtml.xpath('//script[contains(text(), "var domain = ")]')
            #     domain_str = "https://img.xchina.life";
            #     # 提取domain
            #     domain_element = imgpagehtml.xpath('//script[contains(text(), "var domain =")]')
            #     if domain_element:
            #         domain_script = domain_element[0].text.strip()
            #         domain = domain_script.split('var domain = ')[1].split(';')[0].strip('"')
            #         print("Domain:", domain)
            #     else:
            #         print("Domain not found.")
            #
            #     # 提取videos里的url与filename
            #     videos_element = imgpagehtml.xpath('//script[contains(text(), "var videos =")]')
            #     if videos_element:
            #         videos_script = videos_element[0].text.strip()
            #         videos = eval(videos_script.split('var videos = ')[1].split(';')[0])
            #         for video in videos:
            #             url = video["url"].replace('\\/', '/')
            #             filename = video["filename"]
            #             downloadVideo(subfolder + filename, domain_str + url)
            #     print("page vedoo:{}【{}/{}】_{}下载完毕".format(subfolder, filename, domain_str, url))
            else:
                print("Script tag with videos data not found.")
            imgs = imgpagehtml.xpath('//div[@class="photos"]/a')
            if (len(imgs) == 0):
                continue
            for img in imgs:
                imgurl = img.xpath('figure/img/@src')[0]
                imgurl = imgurl.replace("_600x0", "")
                imgname = "{}{}".format(subfolder, "{}{}".format(
                    str(imgindex).rjust(3, '0'), os.path.splitext(imgurl)[-1]))
                if (not os.path.exists(imgname)):
                    download_image(imgname, imgurl)
                print("page:【{}/{}】item:【{}/{}】_{}_第【{}/{}】页_总【{}/{}】-{}下载完毕".format(i, alltotalpage, itemindex,
                                                                                            len(items),
                                                                                            title, j, int(totalpage),
                                                                                            imgindex, piccount,
                                                                                            imgname))
                imgindex += 1
            time.sleep(3)
        itemindex += 1
# Helper function to write to file
def write_to_file(filename, content):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)

alltotalpage = 632
currentpage = 25
currentitem = 11

max_workers = 10

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    for i in range(currentpage, alltotalpage + 1):
        starturl = urltemplate.format(i)
        executor.submit(download_page_content, starturl)

print("Done")
