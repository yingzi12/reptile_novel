import threading
from bs4 import BeautifulSoup
from ParseHtml.DingdHtml import DingdHtml
from ParseHtml.shuba69Html import shuba69Html
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
            responText = HtmlUtil.get_api_data(url)
            if responText is None:
                LogUtil.error(f"url:{url} 获取数据失败")
            else:
              file_path = acaheFileUtil.save(responText, url)

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(responText, 'html.parser')

    # Find all <li> elements, which represent each book entry
    book_entries = soup.find_all('li')
    dingdHtml = shuba69Html()

    # Iterate through each book entry and extract information
    for entry in book_entries:
        title = entry.find('h3').text.strip()
        author = entry.find_all('label')[0].text.strip()
        typeName = entry.find_all('label')[1].text.strip()
        status = entry.find_all('label')[2].text.strip()
        intro = entry.find('ol').text.strip()
        latest_chapter = entry.find('div', class_='zxzj').find('p').text.strip()
        read_link = entry.find('a', class_='btn-tp')['href']

        # Extract the data-src attribute
        imgUrl = entry.find('img')['data-src']
        dingdHtml.detail(read_link, title, author, intro,"0", typeName, latest_chapter,status,imgUrl)

    # 使用锁来保护对AcaheFileUtil的删除操作
    with lock:
        acaheFileUtil.delete(url)


# 创建一个包含400个URL的列表
urls = ["https://www.69shuba.com/ajax_topindex/" + str(i) + "" for i in range(5, 500)]

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
