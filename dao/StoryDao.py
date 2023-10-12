import json
from Util.DBMysqlUtil import DBMysqlUtil
from dao.FindBookDao import FindBookDao
from entity.Story import Story


class StoryDao:
    def __init__(self):
        self.dBMysqlUtil = DBMysqlUtil()
        self.findBookDao = FindBookDao()

    def add(self, story):
        sql = "INSERT INTO wiki_story (name, intro, description, permission, author, " \
              "category, status, tags, exp, ranks," \
              "types, img_url, is_vip, wid, wname, " \
              "type_name, source, is_private, is_finish, update_chapter) " \
              "VALUES (%s, %s, %s, %s, %s," \
              " %s, %s, %s, %s, %s," \
              " %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s)"

        wid = story.wid
        wname = story.wname

        values = (story.name, story.intro, story.description, story.permission, story.author,
                  story.category, story.status, story.tags, story.exp, story.ranks,
                  story.types, story.imgUrl, story.isVip, story.wid, story.wname,
                  story.typeName, story.source, story.isPrivate, story.isFinish, story.updateChapter)

        self.dBMysqlUtil.execute_insert(sql, values)

        sql = "select * from wiki_story where name = %s"
        results = self.dBMysqlUtil.execute_query_one(sql, (story.name,))
        if results is None:
            return None
        else:
            story2 = Story()
            story2.id = results[0]
            story2.name = results[1]
            story2.wid = wid
            story2.wname = wname
            #创建作者
            sql = "insert into wiki_author (wid, wname, sid, sname, user_id, " \
                  "user_name, types) " \
                  "values (%s, %s, %s, %s, %s, %s, %s)"
            values = (story2.wid, story2.wname, story2.id, story2.name, 1, "admin", 3)
            self.dBMysqlUtil.execute_insert(sql, values)
            #保存到寻找书中
            self.findBookDao.add(story.name,story.author,story.sourceUrl,story.wid,story2.id,story.isFinish,story.sourceWeb)
            return story2

    def selectByWname(self, name):
        sql = "select * from wiki_story where name = %s"
        results = self.dBMysqlUtil.execute_query_one(sql, (name,))
        if results is None:
            return None
        else:
            story = Story()
            story.id = results[0]
            story.name = results[1]
            story.wid = results[30]
            story.wname = results[31]
            return story
