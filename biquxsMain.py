import threading
from bs4 import BeautifulSoup

from ParseHtml.BiquxsHtml import BiquxsHtml
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
            responText = HtmlUtil.get_api_data(url)
            if responText is None:
                LogUtil.error(f"url:{url} 获取数据失败")
            else:
              file_path = acaheFileUtil.save(responText, url)

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(responText, 'html.parser')
    # 找到所有的列表项
    list_items = soup.find_all('li')

    biquxsHtml =BiquxsHtml()
    for item in list_items:
        typeName = item.find('span', class_='s1').text
        title = item.find('a').text
        href = item.find('a')['href']
        author = item.find('span', class_='s3').text
        biquxsHtml.detail("http://www.biquxs.com"+href, title, author, "0", typeName)
    # 使用锁来保护对AcaheFileUtil的删除操作
    with lock:
        acaheFileUtil.delete(url)

# 创建一个包含400个URL的列表
urls = ["http://m.biquxs.com/class/1/" + str(i) + ".html" for i in range(1, 2)]

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
