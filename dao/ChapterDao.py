import json
from Util.DBMysqlUtil import DBMysqlUtil
from entity.Chapter import Chapter


class ChapterDao:
    def __init__(self):
        self.dBMysqlUtil = DBMysqlUtil()

    def add(self, chapter):
        sql = "insert into wiki_chapter (title, status, serial_number, pid, level, " \
              "wid, sid, content, pname, sname,up_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        values = (chapter.title, chapter.status, chapter.serialNumber, chapter.pid, chapter.level,
                  chapter.wid, chapter.sid, chapter.content, chapter.pname, chapter.sname,chapter.upId)

        self.dBMysqlUtil.execute_insert(sql, values)

        sql = "select id,title,serial_number,sid,sname,status from wiki_chapter where title = %s and sid = %s"
        results = self.dBMysqlUtil.execute_query_one(sql, (chapter.title, chapter.sid))

        if results is None:
            return None
        else:
            chapter = Chapter()
            chapter.id = results[0]
            chapter.title = results[1]
            chapter.serialNumber = results[2]
            chapter.sid = results[3]
            chapter.sname = results[4]
            chapter.status = results[5]
            return chapter

    def selectByWname(self, title, sid):
        sql = "select id,title,serial_number,sid,sname,status from wiki_chapter where title = %s and sid = %s"
        results = self.dBMysqlUtil.execute_query_one(sql, (title, sid))
        if results is None:
            return None
        else:
            chapter = Chapter()
            chapter.id = results[0]
            chapter.title = results[1]
            chapter.serialNumber=results[2]
            chapter.sid = results[3]
            chapter.sname = results[4]
            chapter.status = results[5]
            return chapter

    def updateContent(self, id, content):
        sql = "update wiki_chapter set content = %s ,status=1 where id = %s"
        self.dBMysqlUtil.execute_update(sql, (content, id))

    def updateDownId(self,sid, id, downId):
        sql = "update wiki_chapter set down_id = %s where id = %s and sid = %s"
        self.dBMysqlUtil.execute_update(sql, (downId, id,sid,))

    def upUpId(self,sid, id, upId):
        sql = "update wiki_chapter set up_id = %s where id = %s and sid = %s"
        self.dBMysqlUtil.execute_update(sql, (upId, id,sid,))

    def updateSerialNumber(self,serialNumber,sid, id):
        sql = "update wiki_chapter set serial_number = %s where id = %s and sid = %s"
        self.dBMysqlUtil.execute_update(sql, (serialNumber, id,sid,))