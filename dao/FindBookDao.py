import json
from Util.DBMysqlUtil import DBMysqlUtil
from entity.Chapter import Chapter
from entity.FindBook import FindBook


class FindBookDao:
    def __init__(self):
        self.dBMysqlUtil = DBMysqlUtil()

    def add(self, name, auhtor, sourceUrl, wid, sid, isFinish, sourceWeb):
        sql = ("insert into find_book (name, auhtor, source_url, wid, sid, is_finish, source_web) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        values = (name, auhtor, sourceUrl, wid, sid, isFinish, sourceWeb,)
        self.dBMysqlUtil.execute_insert(sql, values)

    def selectByWname(self, name, auhtor):
        sql = "select id,name, auhtor, sourceUrl, wid, sid, is_finish, source_web, targetUrl, target_web from find_book where name = %s and auhtor = %s"
        results = self.dBMysqlUtil.execute_query_one(sql, (name, auhtor))
        if results is None:
            return None
        else:
            findBook = FindBook()
            findBook.id = results[0]
            findBook.name = results[1]
            findBook.auhtor=results[2]
            findBook.sourceUrl = results[3]
            findBook.wid = results[4]
            findBook.sid = results[5]
            findBook.isFinish = results[6]
            findBook.sourceWeb = results[7]
            findBook.targetUrl = results[8]
            findBook.targetWeb = results[9]
            return findBook

    def selectByWname(self,  page):
        # Calculate the OFFSET value based on the page number
        items_per_page = 100
        offset = (page - 1) * items_per_page

        # Define the SQL query with LIMIT and OFFSET
        sql = "SELECT id, name, auhtor, sourceUrl, wid, sid, is_finish, source_web, target_url, target_web FROM find_book where is_finish=2 LIMIT %s OFFSET %s"

        # Execute the query with parameters
        results = self.dBMysqlUtil.execute_query(sql, ( items_per_page, offset))

        # Process the results
        findBooks = []
        for row in results:
            findBook = FindBook()
            findBook.id = row[0]
            findBook.name = row[1]
            findBook.auhtor = row[2]
            findBook.sourceUrl = row[3]
            findBook.wid = row[4]
            findBook.sid = row[5]
            findBook.isFinish = row[6]
            findBook.sourceWeb = row[7]
            findBook.targetUrl = row[8]
            findBook.targetWeb = row[9]
            findBooks.append(findBook)

        return findBooks

    def updateTargetUrl(self, name, auhtor,targetUrl,targetWb):
        sql = "update find_book set target_url = %s,target_wb = %s where name = %s and  auhtor = %s"
        self.dBMysqlUtil.execute_update(sql, (targetUrl,targetWb, name,auhtor))
