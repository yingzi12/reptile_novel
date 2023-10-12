from Util import LogUtil
from dao.StoryDao import StoryDao
from entity.Story import Story
class StoryService:
    def __init__(self):
        self.storyDao = StoryDao();

    def add(sflt,wid, wname, author, name, description, intro, imgUrl, types, typesName, isFinish, updateChapter,source="转载"):

        story = Story();
        story.imgUrl = imgUrl
        story.wid = wid
        story.wname = wname
        story.name = name
        story.description = description
        story.types = types
        story.typesName = typesName
        story.intro = intro
        story.source =source
        story.author = author
        story.isFinish = isFinish
        story.updateChapter = updateChapter
        story = sflt.storyDao.add(story);
        return story;

    def select(sflt,name):
        story = sflt.storyDao.selectByWname(name)
        if (story is None):
            return None;
        else:
            return story;