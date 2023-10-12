import re
import time

from bs4 import BeautifulSoup

from Util import HtmlUtil, LogUtil, OSSUtil
from Util.AcaheFileUtil import AcaheFileUtil
from service.ChapterService import ChapterService
from service.StoryService import StoryService
from service.WorldService import WorldService

from urllib.parse import urlparse

class shuba69Html:

    def __init__(self):
        self.worldService = WorldService();
        self.storyService = StoryService();
        self.chapterService = ChapterService();
        self.acaheFileUtil = AcaheFileUtil();


    def detail(self,url, name, author, intro,types, typesName, updateChapter,status,imgUrl):
        # if (self.acaheFileUtil.exists(url)):
        #     responText = self.acaheFileUtil.read(url);
        # # HtmlUtil.get_api_data(url);
        # else:
        #     responText = HtmlUtil.get_api_data(url, HeadUtil.bjg())
        #     if (responText == None):
        #         LogUtil.error(f"url {url} 获取数据失败")
        #     file_path = self.acaheFileUtil.save(responText, url);
        # soup = BeautifulSoup(responText, 'html.parser')

        # 提取img标签中的src属性
        # img_tag = soup.find('div', id='fmimg').find('img')
        # img_src = img_tag['src']
        parsed_url = urlparse(imgUrl)
        img_src=parsed_url.path
        OSSUtil.upload(imgUrl)
        # intro = soup.find(id='intro')
        info = intro
        Description = intro
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
            isFinish=1;
            if status in ['连载', '连载中']:
                isFinish = 2
            elif status in ['完结', '已完结', '全本']:
                isFinish = 1
            story = self.storyService.add(world.id, world.name, author, name, info, Description,
                                          "\\"+ "sotry" + img_src, types, typesName, isFinish, updateChapter)

        # Replace ".htm" with "/"
        chapterUrl = url.replace(".htm", "/")
        if (self.acaheFileUtil.exists(chapterUrl)):
            responText = self.acaheFileUtil.read(chapterUrl);
        # HtmlUtil.get_api_data(url);
        else:
            responText = HtmlUtil.get_api_data(chapterUrl)
            if (responText == None):
                LogUtil.error(f"url {chapterUrl} 获取数据失败")
            file_path = self.acaheFileUtil.save(responText, chapterUrl);

        soup = BeautifulSoup(responText, 'html.parser')

        #保存到文件中
        # parsed_url = urlparse(chapterUrl)
        # content_url = parsed_url.path
        # file_path = self.acaheFileUtil.saveFile(soup, content_url);

        unique_int = int(time.time() * 1000)

        pChapter = self.chapterService.select(story.id, "其他");
        if (pChapter is None):
            pChapter = self.chapterService.add("其他", unique_int, 0, 0, world.id, story.id, "", "其他", story.name)

        # Find the <ul> element containing the chapter information
        content_div = soup.find('div', id='catalog')
        chapter_list = content_div.find('ul')
        upId=0
        serialNumber=pChapter.serialNumber;

        # Iterate through each <li> element within the <ul>
        for li in chapter_list.find_all('li'):
            chapter_data = li.find('a')  # Find the <a> element within the <li>

            if chapter_data:
                chapter_name = chapter_data.text.strip()  # Extract the chapter title
                chapter_url = chapter_data['href']  # Extract the chapter URL

                # Extract the chapter number from the "data-num" attribute
                chapter_number = li.get('data-num')

                nexChapter = self.chapterService.select(story.id, chapter_name);
                if (nexChapter is None):
                    nexChapter = self.addChapter( chapter_url, pChapter, story, chapter_name, upId);
                if (nexChapter is not None):
                    self.upDowId(story.id, upId, nexChapter.id);
                    self.upUpId(story.id, nexChapter.id, upId);

                    if (nexChapter.serialNumber < serialNumber):
                        self.updateSerialNumber(serialNumber + 1, story.id, nexChapter.id);
                    serialNumber = nexChapter.serialNumber;
                    upId = nexChapter.id;

        self.acaheFileUtil.delete(url);

    def addChapter(self,url, pChapter, story, chapterName,upId):
        if (self.acaheFileUtil.exists(url)):
            responText = self.acaheFileUtil.read(url);
        else:
            responText = HtmlUtil.get_api_data(url)
            if (responText == None):
                upId=0;
                LogUtil.error(f"url:{url} sotry:{story.name} chapterName:{chapterName} 获取数据失败")
                return;
            else:
                file_path = self.acaheFileUtil.save(responText, url);
        soup = BeautifulSoup(responText, 'html.parser')
        # 使用find()方法查找具有id="content"的<div>元素
        content_div = soup.find('div', class_='txtnav')

        tags = content_div.find_all("div")

        # Remove the content of each tag
        for tag in tags:
            tag.string = ""
        h1 = content_div.find("h1");
        h1.string="";
        # 提取<div>元素的内容
        if content_div:
            content = content_div.decode_contents().replace(chapterName,"")


            # content = content_div
            unique_int = int(time.time() * 1000)
            title = chapterName
            content = re.sub(r'(<br/>\s*)+', '<br/>', content)

            chapter = self.chapterService.add(title, unique_int, pChapter.id, 1, story.wid, story.id, content,
                                         pChapter.title,
                                         story.name,upId)
            file_path = self.acaheFileUtil.saveFile(content,"world/"+str(story.wid)+"/"+str(story.id)+"/"+str(chapter.id));
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