import datetime
import re
import time

from bs4 import BeautifulSoup

from Util import HtmlUtil, HeadUtil, LogUtil, OSSUtil
from Util.AcaheFileUtil import AcaheFileUtil
from service.ChapterService import ChapterService
from service.StoryService import StoryService
from service.WorldService import WorldService

url="http://www.biquxs.com"
class BiquxsHtml:

    def __init__(self):
        self.worldService = WorldService();
        self.storyService = StoryService();
        self.chapterService = ChapterService();
        self.acaheFileUtil = AcaheFileUtil();


    def detail(self,href, name, author, types, typesName):
        if (self.acaheFileUtil.exists(href)):
            responText = self.acaheFileUtil.read(href);
        # HtmlUtil.get_api_data(url);
        else:
            responText = HtmlUtil.get_api_data(href)
            if (responText == None):
                LogUtil.error(f"url {href} 获取数据失败")
            file_path = self.acaheFileUtil.save(responText, href);
        soup = BeautifulSoup(responText, 'html.parser')

        # 提取img标签中的src属性
        img_tag = soup.find('div', id='fmimg').find('img')
        img_src = img_tag['src']
        OSSUtil.upload(url + img_src)

        # 获取书籍信息
        info = soup.find("div", id="info")
        img_tag = soup.find('div', id='fmimg').find('img')
        img_src = img_tag['src']
        status = info.find_all("p")[1].text.split("：")[1]
        latest_chapter =info.find_all("p")[4].find("a").text

        # 获取简介
        intro = soup.find("div", id="intro")
        summary = intro.find("p").text

        world = self.worldService.select(name);
        if (world is None):
            world = self.worldService.select(name+"("+author+")");
            if (world is None):
                 world = self.worldService.add(name, summary, summary, "\\"+"sotry" + img_src, types, typesName, author)
        else:
            if(world.source != author):
                world = self.worldService.add(name+"("+author+")", summary, summary, "\\" + "sotry" + img_src,
                                              types, typesName, author)
        story = self.storyService.select(name);
        if (story is None):
            isFinish = 1;
            if status in ['连载', '连载中']:
                isFinish = 2
            elif status in ['完结', '完本', '已完结', '全本']:
                isFinish = 1
            story = self.storyService.add(world.id, world.name, author, name, summary, summary,
                                          "\\"+ "sotry" + img_src, types, typesName, isFinish, latest_chapter,url)

        unique_int = int(time.time() * 1000)

        pChapter = self.chapterService.select(story.id, "其他");
        if (pChapter is None):
            pChapter = self.chapterService.add("其他", unique_int, 0, 0, world.id, story.id, "", "其他", story.name)
        # 提取章节内容
        chapter_uls = soup.find('div', class_='listmain').find_all('dd')
        upId=0
        serialNumber=pChapter.serialNumber;
        for chapter_ul in chapter_uls:
            chapter_name = chapter_ul.a.get_text().strip()
            chapter_url = chapter_ul.a['href']
            print('Chapter Name:', chapter_name)
            print('Chapter URL:', chapter_url)
            nexChapter = self.chapterService.select(story.id, chapter_name);
            if (nexChapter is None):
                nexChapter = self.addChapter( url+ chapter_url, pChapter, story, chapter_name, upId);
            if (nexChapter is not None):
                self.upDowId(story.id, upId, nexChapter.id);
                self.upUpId(story.id, nexChapter.id, upId);
                if (nexChapter.serialNumber < serialNumber):
                    self.updateSerialNumber(serialNumber + 1, story.id, nexChapter.id);
                serialNumber = nexChapter.serialNumber;
                upId = nexChapter.id;
        self.acaheFileUtil.delete(url);

    def addChapter(self,chapterUrl, pChapter, story, chapterName,upId):
        if (self.acaheFileUtil.exists(chapterUrl)):
            responText = self.acaheFileUtil.read(chapterUrl);
        else:
            responText = HtmlUtil.get_api_data(chapterUrl, HeadUtil.bjg())
            if (responText == None):
                upId=0;
                LogUtil.error(f"url:{chapterUrl} sotry:{story.name} chapterName:{chapterName} 获取数据失败")
                return;
            file_path = self.acaheFileUtil.save(responText, chapterUrl);
        soup = BeautifulSoup(responText, 'html.parser')
        # 使用find()方法查找具有id="content"的<div>元素
        content_div = soup.find('div', id='content')
        # 提取<div>元素的内容
        if content_div:
            content = content_div.decode_contents().replace("首发域名ｍ.biquxs。com","")
            # content = content_div
            unique_int = int(time.time() * 1000)
            title = chapterName
            content = re.sub(r'(<br/>\s*)+', '<br/>', content)

            chapter = self.chapterService.add(title, unique_int, pChapter.id, 1, story.wid, story.id, content,
                                         pChapter.title,
                                         story.name,upId)
            self.acaheFileUtil.delete(chapterUrl)
            return chapter;
            # print(content)
        else:
            LogUtil.error(f"chapterUrl:{chapterUrl} sotry:{story.name} chapterName:{chapterName} 未找到具有id='content'的<div>元素。")

    def upDowId(self,sid,id, dowId):
        self.chapterService.upDowId(sid,id,dowId)

    def upUpId(self, sid, id, upId):
        self.chapterService.upUpId(sid, id, upId)
    def updateSerialNumber(self, serialNumber,sid, id):
        self.chapterService.updateSerialNumber(serialNumber,sid, id)