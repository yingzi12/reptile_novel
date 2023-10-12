import datetime
import re
import time

from bs4 import BeautifulSoup

from Util import HtmlUtil, HeadUtil, LogUtil, OSSUtil
from Util.AcaheFileUtil import AcaheFileUtil
from service.ChapterService import ChapterService
from service.StoryService import StoryService
from service.WorldService import WorldService


class DingdHtml:

    def __init__(self):
        self.worldService = WorldService();
        self.storyService = StoryService();
        self.chapterService = ChapterService();
        self.acaheFileUtil = AcaheFileUtil();


    def detail(self,url, name, author, types, typesName, updateChapter):
        if (self.acaheFileUtil.exists(url)):
            responText = self.acaheFileUtil.read(url);
        # HtmlUtil.get_api_data(url);
        else:
            responText = HtmlUtil.get_api_data(url, HeadUtil.bjg())
            if (responText == None):
                LogUtil.error(f"url {url} 获取数据失败")
            file_path = self.acaheFileUtil.save(responText, url);
        soup = BeautifulSoup(responText, 'html.parser')
        # 提取img标签中的src属性
        img_tag = soup.find('div', id='fmimg').find('img')
        img_src = img_tag['src']
        OSSUtil.upload("https://www.230book.net/" + img_src)

        intro = soup.find(id='intro')
        info = intro.text
        Description = intro.text
        world = self.worldService.select(name);
        if (world is None):
            world = self.worldService.select(name+"("+author+")");
            if (world is None):
                 world = self.worldService.add(name, info, Description, "\\"+"sotry" + img_src, types, typesName, author)
        else:
            if(world.source != author):
                world = self.worldService.add(name+"("+author+")", info, Description, "\\" + "sotry" + img_src,
                                              types, typesName, author)
        story = self.storyService.select(name);
        if (story is None):
            story = self.storyService.add(world.id, world.name, author, name, info, Description,
                                          "\\"+ "sotry" + img_src, types, typesName, 1, updateChapter,url)



        unique_int = int(time.time() * 1000)
        pChapter = self.chapterService.select(story.id, "其他");
        if (pChapter is None):
            pChapter = self.chapterService.add("其他", unique_int, 0, 0, world.id, story.id, "", "其他", story.name)
        # 提取章节内容
        chapter_uls = soup.find('div', id='list').find_all('ul', class_='_chapter')
        upId=0
        serialNumber=pChapter.serialNumber;
        for chapter_ul in chapter_uls:
            for li in chapter_ul.find_all('li'):
                try:
                    if (li.a is not None):
                        chapter_name = li.a.get_text()
                        chapter_url = li.a['href']
                        print('Chapter Name:', chapter_name)
                        print('Chapter URL:', chapter_url)
                        nexChapter = self.chapterService.select(story.id, chapter_name);
                        if (nexChapter is None):
                            nexChapter = self.addChapter(url + chapter_url, pChapter, story, chapter_name,upId);
                        if (nexChapter is not None):
                           self.upDowId(story.id, upId, nexChapter.id);
                           self.upUpId(story.id, nexChapter.id, upId);

                           if(nexChapter.serialNumber < serialNumber):
                               self.updateSerialNumber(serialNumber+1,story.id,nexChapter.id);
                           serialNumber = nexChapter.serialNumber;
                           upId = nexChapter.id;


                except Exception:
                    LogUtil.error("解析错误:" + li);
        self.acaheFileUtil.delete(url);

    def addChapter(self,url, pChapter, story, chapterName,upId):
        if (self.acaheFileUtil.exists(url)):
            responText = self.acaheFileUtil.read(url);
        else:
            responText = HtmlUtil.get_api_data(url, HeadUtil.bjg())
            if (responText == None):
                upId=0;
                LogUtil.error(f"url:{url} sotry:{story.name} chapterName:{chapterName} 获取数据失败")
                return;
            file_path = self.acaheFileUtil.save(responText, url);
        soup = BeautifulSoup(responText, 'html.parser')
        # 使用find()方法查找具有id="content"的<div>元素
        content_div = soup.find('div', id='content')
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