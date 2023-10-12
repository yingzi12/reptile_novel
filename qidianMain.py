import threading
from bs4 import BeautifulSoup

from ParseHtml.QidianHtml import QidianHtml
from Util import LogUtil, HtmlUtil, HeadUtil
from Util.AcaheFileUtil import AcaheFileUtil

# 创建一个互斥锁来保护共享资源
lock = threading.Lock()


# 定义一个函数来处理每个URL
def process_url(url):
    acaheFileUtil = AcaheFileUtil()

    # 使用锁来保护对AcaheFileUtil的访问
    with lock:
        if acaheFileUtil.exists(url):
            responText = acaheFileUtil.read(url)
        else:
            responText = HtmlUtil.get_api_data(url,HeadUtil.qid())
            if responText is None:
                LogUtil.error(f"url:{url} 获取数据失败")
            else:
              file_path = acaheFileUtil.save(responText, url)

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(responText, 'html.parser')

    # Find the <ul> element under the specific <div> by its ID
    ul_element = soup.find('div', {'class': 'book-img-text', 'id': 'book-img-text'}).find('ul')

    # Find all <li> elements within the <ul>
    li_elements = ul_element.find_all('li')
    qidianHtml = QidianHtml()
    # Loop through each <li> element to extract information
    for li in li_elements:
        # # Extract information from the <div> elements within each <li>
        # book_img_box = li.find('div', {'class': 'book-img-box'})
        # book_mid_info = li.find('div', {'class': 'book-mid-info'})
        # book_right_info = li.find('div', {'class': 'book-right-info'})
        #
        # # Extract specific information from these <div> elements as needed
        #
        # # For example, to extract the title and author:
        # title = book_mid_info.find('h2').find('a').get_text()
        # author = book_mid_info.find('p', {'class': 'author'}).find('a', {'class': 'name'}).get_text()
        #
        # # Print or store the extracted information
        # print("Title:", title)
        # print("Author:", author)
        # print("-------")
        # book_info = {}
        href= li.find("div", class_="book-img-box").find("a").get("href")
        imgUrl =li.find("div", class_="book-img-box").find("img").get("src")
        # href = soup.find("a").get("href")
        # src = soup.find("img").get("src")

        title = li.find("h2").text
        author = li.find("p", class_="author").find("a").text
        categorys = li.find("p", class_="author").find_all("a")[1:]
        typeName=""
        for category in categorys:
            typeName=category.text+","+typeName
        status= li.find("p", class_="author").find("span").text
        intro= li.find("p", class_="intro").text
        update = li.find("p", class_="update").find("a").text
        qidianHtml.detail(href, title, author, intro, "0", typeName, update, status, imgUrl)

    # 使用锁来保护对AcaheFileUtil的删除操作
    with lock:
        acaheFileUtil.delete(url)

# 创建一个包含400个URL的列表
urls = ["https://www.qidian.com/rank/recom/chn21/datetype3/page" + str(i) + "/" for i in range(1, 5)]

# 最大线程数
max_threads = 5

# 创建多个线程来处理URL
threads = []

for i in range(0, len(urls), max_threads):
    batch_urls = urls[i:i + max_threads]  # 获取当前批次的URL
    LogUtil.info(batch_urls)
    batch_threads = []  # 用于存放当前批次的线程
    for url in batch_urls:
        thread = threading.Thread(target=process_url, args=(url,))
        thread.start()
        batch_threads.append(thread)
    for thread in batch_threads:
        thread.join()
    threads.extend(batch_threads)

# 等待所有线程完成
for thread in threads:
    thread.join()
