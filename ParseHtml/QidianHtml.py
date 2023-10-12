import re
import time

from bs4 import BeautifulSoup
from sqlalchemy.sql.functions import current_date

from Util import HtmlUtil, LogUtil, OSSUtil, HeadUtil
from Util.AcaheFileUtil import AcaheFileUtil
from service.ChapterService import ChapterService
from service.StoryService import StoryService
from service.WorldService import WorldService


class QidianHtml:

    def __init__(self):
        self.worldService = WorldService();
        self.storyService = StoryService();
        self.chapterService = ChapterService();
        self.acaheFileUtil = AcaheFileUtil();


    def detail(self,url, name, author, intro,types, typesName, updateChapter,status,imgUrl):
        if (self.acaheFileUtil.exists(url)):
            responText = self.acaheFileUtil.read(url);
        else:
            responText = HtmlUtil.get_api_data("https:"+url,HeadUtil.qid())
            if (responText == None):
                LogUtil.error(f"url {url} 获取数据失败")
            file_path = self.acaheFileUtil.save(responText, url);
        soup = BeautifulSoup(responText, 'html.parser')


        # 提取img标签中的src属性
        # img_tag = soup.find('div', id='fmimg').find('img')
        # img_src = img_tag['src']
        # 获取当前时间戳（以秒为单位）
        OSSUtil.upload("https:"+imgUrl)
        description = soup.find('p',id='book-intro-detail')
        intro = soup.find('div',class_="book-info-top").find('p',class_='intro')
        # info = intro.text

        # Description = intro.text
        world = self.worldService.select(name);
        if (world is None):
            world = self.worldService.select(name + "(" + author + ")");
            if (world is None):
                world = self.worldService.add(name, intro, description, "\\" + "sotry" + imgUrl, types, typesName,
                                              author)
        else:
            if (world.source != author):
                world = self.worldService.add(name + "(" + author + ")", intro, description, "\\" + "sotry" + imgUrl,
                                              types, typesName, author)
        story = self.storyService.select(name);
        if (story is None):
            isFinish = 1;
            if status in ['连载', '连载中']:
                isFinish = 2
            elif status in ['完结', '完本', '已完结', '全本']:
                isFinish = 1
            story = self.storyService.add(world.id, world.name, author, name, intro, description,
                                          "\\" + "sotry" + imgUrl, types, typesName, isFinish, updateChapter)

        upId = 0
        # Find the <div class="catalog-all" id="allCatalog">
        catalog_all_div = soup.find('div', {'class': 'catalog-all', 'id': 'allCatalog'})
        serialNumber=0;
        vip =None;
        if catalog_all_div:
            # Find all <div class="catalog-volume"> elements within <div class="catalog-all" id="allCatalog">
            volume_divs = catalog_all_div.find_all('div', {'class': 'catalog-volume'})

            # Loop through each <div class="catalog-volume"> element
            for volume_div in volume_divs:
                # Find <h3 class="volume-name"> within the current <div class="catalog-volume">
                volume_name = volume_div.find('h3', {'class': 'volume-name'})
                if volume_name:
                    vip = volume_div.find('span', {'class': 'vip'})
                    title = volume_name.get_text(strip=True);
                    parts = title.split("·")
                    title = parts[0]
                    # 生成一个随机的UUID
                    # 将UUID转换为整数
                    unique_int = int(time.time() * 1000)
                    pChapter = self.chapterService.select(story.id, title);
                    if (pChapter is None):
                        pChapter = self.chapterService.add(title, unique_int, 0, 0, world.id, story.id, "", "其他",
                                                           story.name)
                    serialNumber = pChapter.serialNumber;
                # Find <ul class="volume-chapters"> within the current <div class="catalog-volume">
                volume_chapters_ul = volume_div.find('ul', {'class': 'volume-chapters'})
                upId = 0
                if volume_chapters_ul:
                    # Find all <li class="chapter-item"> elements within <ul class="volume-chapters">
                    chapter_items = volume_chapters_ul.find_all('li', {'class': 'chapter-item'})
                    for chapter_item in chapter_items:
                        # Find <a class="chapter-name"> within the current <li class="chapter-item">
                        chapter_name_html = chapter_item.find('a', {'class': 'chapter-name'})
                        if chapter_name_html:
                            print("Chapter Name:", chapter_name_html.get_text(strip=True))
                            print("Chapter URL:", chapter_name_html['href'])
                            chapter_name = chapter_name_html.get_text(strip=True);
                            href = chapter_name_html['href'];
                            nexChapter = self.chapterService.select(story.id, chapter_name);
                            if (nexChapter is None):
                                if(vip  is  None):
                                    nexChapter = self.addChapter(href, pChapter, story, chapter_name, upId);
                                else:
                                    #VIP章节直接保存
                                    unique_int = int(time.time() * 1000)
                                    nexChapter = self.chapterService.add(chapter_name, unique_int, pChapter.id, 1, story.wid,
                                                                     story.id, "",
                                                                     pChapter.title,
                                                                     story.name, upId,0)
                            if (nexChapter is not None):
                                self.upDowId(story.id, upId, nexChapter.id);
                                self.upUpId(story.id, nexChapter.id, upId);
                                if (nexChapter.serialNumber < serialNumber):
                                    self.updateSerialNumber(serialNumber + 1, story.id, nexChapter.id);
                                serialNumber = nexChapter.serialNumber;
                                upId = nexChapter.id;
                            # chapter = ChapterService.add(title, unique_int, pChapter.id, 1, world.id, story.id,
                            #                              chapter_name['href'], pChapter.title,
                            #                              story.name)
        self.acaheFileUtil.delete(url);

    def addChapter(self,url, pChapter, story, chapterName,upId):
        if (self.acaheFileUtil.exists(url)):
            responText = self.acaheFileUtil.read(url);
        else:
            responText = HtmlUtil.get_api_data("https:"+url,HeadUtil.qid())
            if (responText == None):
                upId=0;
                LogUtil.error(f"url:{url} sotry:{story.name} chapterName:{chapterName} 获取数据失败")
                return;
            else:
                OSSUtil.uploadChapter("https:"+url)
            file_path = self.acaheFileUtil.save(responText, url);
        soup = BeautifulSoup(responText, 'html.parser')
        # 使用find()方法查找具有id="content"的<div>元素
        content_div = soup.find('main')
        # 提取<div>元素的内容
        if content_div:
            content = content_div.decode_contents()
            # content = content_div
            unique_int = int(time.time() * 1000)
            title = chapterName
            content = re.sub(r'(<br/>\s*)+', '<br/>', content)

            chapter = self.chapterService.add(title, unique_int, pChapter.id, 1, story.wid, story.id, content,
                                         pChapter.title,
                                         story.name,upId)
            # file_path = self.acaheFileUtil.saveFile(content,"world/"+wid+"/"+story.id+"/"+chapter.id);
            self.acaheFileUtil.delete(url)
            return chapter;
            # print(content)
        else:
            LogUtil.error(f"url:{url} sotry:{story.name} chapterName:{chapterName} 未找到具有id='content'的<div>元素。")

    def upDowId(self,sid,id, dowId):
        self.chapterService.upDowId(sid,id,dowId)

    def upUpId(self, sid, id, upId):
        self.chapterService.upUpId(sid, id, upId)
    def updateSerialNumber(self, serialNumber,sid, id):
        self.chapterService.updateSerialNumber(serialNumber,sid, id)