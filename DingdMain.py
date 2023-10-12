import threading
from bs4 import BeautifulSoup
from ParseHtml.DingdHtml import DingdHtml
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
            responText = HtmlUtil.get_api_data(url, HeadUtil.bjg())
            if responText is None:
                LogUtil.error(f"url:{url} 获取数据失败")
            file_path = acaheFileUtil.save(responText, url)

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(responText, 'html.parser')

    # 提取id为"newscontent"的内容
    newscontent_div = soup.find(id='newscontent')
    # 找到class="l"下的ul元素
    l_div = newscontent_div.find(class_='l')
    ul = l_div.find('ul')

    # 遍历所有的li元素
    for li in ul.find_all('li'):
        # 提取详细信息
        title = li.find('span', class_='s2').text.strip().replace('《', '').replace('》', '')  # 提取标题
        book_link = li.find('a', href=True)['href']  # 提取书籍链接
        chapter_title = li.find('span', class_='s3').text.strip()  # 提取章节标题
        new_chapter = li.find('span', class_='s3').find('a').text.strip()  # 提取章节发布日期
        author = li.find('span', class_='s5').text.strip()  # 提取作者

        dingdHtml = DingdHtml()
        dingdHtml.detail(book_link, title, author, "11", "科幻", new_chapter)

    # 使用锁来保护对AcaheFileUtil的删除操作
    with lock:
        acaheFileUtil.delete(url)


# 创建一个包含400个URL的列表
urls = ["https://www.230book.net/kehuanxiaoshuo/6_" + str(i) + ".html" for i in range(1, 184)]

# 最大线程数
max_threads = 5

# 创建多个线程来处理URL
threads = []

for i in range(0, len(urls), max_threads):
    batch_urls = urls[i:i + max_threads]  # 获取当前批次的URL
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
