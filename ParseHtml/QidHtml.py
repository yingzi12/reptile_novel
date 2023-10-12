import json
import re
import time
import uuid

import execjs
from bs4 import BeautifulSoup

from service import WorldService, StoryService, ChapterService


def order():
    # url = "https://www.qidian.com/so/%E5%9B%9E%E5%88%B0%E6%98%8E%E6%9C%9D%E5%BD%93%E7%8E%8B%E7%88%B7.html";
    #
    # responText=HtmlUtil.get_api_data(url,HeadUtil.qid())
    # if(responText == None):
    #     LogUtil.error(f"url {url} 获取数据失败")

    # 打开文件并读取整个内容
    with open('C:\\git\\reptile-myself\\ParseHtml\\qid_order.html', 'r') as file:
        content = file.read()
    # 这是你提供的HTML代码
    html_code =content

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html_code, 'html.parser')

    # Find script tags containing 'g_data' variable
    g_data_scripts = soup.find_all(find_g_data_script)
    # 找到包含g_data变量的<script>标签
    # script_tags = soup.find_all('script')
    for script_tag in g_data_scripts:
        #if script_tag:
        # 获取JavaScript代码块内容
        javascript_code = script_tag.string


        # Execute JavaScript code and get the result
        ctx = execjs.compile(javascript_code)
        # result = ctx.eval("g_data.listInfo")
        #
        # print(result)
        list_info = ctx.eval("g_data.listInfo")

        # Iterate through and print each item in g_data.listInfo
        for item in list_info:
            print("Book ID:", item["bookId"])
            print("Book Name:", item["bookName"])
            print("Book Info:", item["bookInfo"])
            print("Book URL:", item["bookUrl"])
            print("Description:", item["desc"])
            print("Channel ID:", item["chanId"])
            print("Channel Name:", item["chanName"])
            print("Author ID:", item["authorId"])
            print("Author Name:", item["authorName"])
            print("Book Status:", item["bookStatus"])
            print("Sign Status:", item["signStatus"])
            print("Image URL:", item["imgUrl"])
            print("Is VIP:", item["isVip"])
            print("Last Chapter Name:", item["lastChapterName"])
            print("Last Chapter URL:", item["lastChapterUrl"])
            print("Chapter List URL:", item["chapterListUrl"])
            print("Last Update Time:", item["lastUpdateTime"])
            print("Author URL:", item["authorUrl"])
            print("Book Type:", item["bookType"])
            print("Is Pub:", item["isPub"])
            print("Ecytag:", item["ecytag"])
            print("Ecytag Link:", item["ecytagLink"])
            print("CBID:", item["cbid"])
            print("Update Time:", item["updateTime"])
            print("Algorithm Info:", item["algInfo"])
            print("Click Count:", item["clickCnt"])
            print("Recommendation Count:", item["recomendCnt"])
            print("Words Count:", item["wordsCnt"])
            print("Is In Shelf:", item["isInShelf"])
            print()



def detail():
    info="阴差阳错间，乌龙九世善人郑少鹏回到了大明正德年间。那是一个多姿多彩的时代，既有京师八虎的邪恶，又有江南四大才子的风流，还有大儒王阳明的心学，再加上荒诞不经的正德皇帝朱厚照。浑浑噩噩中踏进这个世界的主角，不得不为了自己的命运，周旋在这形形色色的人物之中。东厂、西厂、内厂、外廷之间的纷争；代天巡狩清除贪官的故事；剿倭寇、驱鞑靼、灭都掌蛮、大战佛郎机；开海禁、移民西伯利亚……，精彩的故事纷至沓来……国家和个人的命运，就象历史长河中的一条船，因为他的意外出现，这艘原本注定驶向没落的巨轮，会不会偏移它的方向呢？";
    Description="阴差阳错间，乌龙九世善人郑少鹏回到了大明正德年间。那是一个多姿多彩的时代，既有京师八虎的邪恶，又有江南四大才子的风流，还有大儒王阳明的心学，再"
    world=WorldService.add("回到明朝当王爷",info,Description,"//bookcover.yuewen.com/qdbimg/349573/84024/180",10,"历史","月关")
    story=StoryService.add(world.id,world.name,"月关","回到明朝当王爷",info,Description,"//bookcover.yuewen.com/qdbimg/349573/84024/180",10,"历史",1,"")

    # 打开文件并读取整个内容
    with open("C:\\git\\reptile-myself\\ParseHtml\\qid_detail.html", 'r') as file:
        content = file.read()
    # 这是你提供的HTML代码
    html_code = content

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_code, 'html.parser')

    # Find the <div class="catalog-all" id="allCatalog">
    catalog_all_div = soup.find('div', {'class': 'catalog-all', 'id': 'allCatalog'})

    if catalog_all_div:
        # Find all <div class="catalog-volume"> elements within <div class="catalog-all" id="allCatalog">
        volume_divs = catalog_all_div.find_all('div', {'class': 'catalog-volume'})

        # Loop through each <div class="catalog-volume"> element
        for volume_div in volume_divs:
            # Find <h3 class="volume-name"> within the current <div class="catalog-volume">
            volume_name = volume_div.find('h3', {'class': 'volume-name'})
            if volume_name:
                print("Volume Name:", volume_name.get_text(strip=True))

                title= volume_name.get_text(strip=True);
                parts = title.split("·")
                title = parts[0]
                # 生成一个随机的UUID
                # 将UUID转换为整数
                unique_int = time.time()
                pChapter = ChapterService.add(title, unique_int, 0, 0, world.id, story.id, "",title, story.name)
                print(pChapter)
            # Find <ul class="volume-chapters"> within the current <div class="catalog-volume">
            volume_chapters_ul = volume_div.find('ul', {'class': 'volume-chapters'})
            if volume_chapters_ul:
                # Find all <li class="chapter-item"> elements within <ul class="volume-chapters">
                chapter_items = volume_chapters_ul.find_all('li', {'class': 'chapter-item'})
                for chapter_item in chapter_items:
                    # Find <a class="chapter-name"> within the current <li class="chapter-item">
                    chapter_name = chapter_item.find('a', {'class': 'chapter-name'})
                    if chapter_name:
                        print("Chapter Name:", chapter_name.get_text(strip=True))
                        print("Chapter URL:", chapter_name['href'])
                        unique_int = time.time()
                        title=chapter_name.get_text(strip=True);
                        chapter = ChapterService.add(title, unique_int, pChapter.id, 1, world.id, story.id, chapter_name['href'],  pChapter.title,
                                                      story.name)
                        # # 使用正则表达式匹配最后一对斜杠之间的数字
                        # match = re.search(r'/(\d+)/$',  chapter_name['href'])
                        # if match:
                        #     last_number = match.group(1)
                        #     print("最后的数字是:", last_number)
                        # else:
                        #     print("没有找到匹配的数字")
                    print()  # Print an empty line to separate chapters


# Custom function to find script tags containing 'g_data' variable
def find_g_data_script(tag):
    return tag.name == 'script' and 'g_data' in tag.text

detail()