from Util import LogUtil
from dao.ChapterDao import ChapterDao
from entity.Chapter import Chapter

class ChapterService:

    def __init__(self):
        self.chapterDao = ChapterDao();

    def add(self,title, serialNumber, pid, level, wid, sid, content, pname, sname,up_id=0,status=1):
        chapter = Chapter();
        chapter.sid = sid
        chapter.sname = sname
        chapter.wid = wid
        chapter.title = title
        chapter.status = status
        chapter.pid = pid
        chapter.level = level
        chapter.content = content
        chapter.serialNumber = serialNumber
        chapter.pname = pname
        chapter.source = "转载"
        chapter.up_id = up_id
        chapter = self.chapterDao.add(chapter);
        return chapter;

    def select(self,sid, title):
        chapter = self.chapterDao.selectByWname(title, sid)
        if (chapter is None):
            return None;
        else:
            return chapter;

    def updateContent(self,sid,id,downId):
         self.chapterDao.updateContent(sid,id,downId)

    def upDowId(self,sid,id,downId):
         self.chapterDao.updateDownId(sid,id,downId)

    def upUpId(self,sid,id,upId):
         self.chapterDao.upUpId(sid,id,upId)

    def updateSerialNumber(self, serialNumber, sid,id ):
        self.chapterDao.updateSerialNumber(serialNumber,sid, id)