from Util import LogUtil
from dao.WorldDao import WorldDao
from entity.World import World

class WorldService:

    def __init__(self):
        self.worldDao = WorldDao();

    def add(sflt,name, description, intro, imgUrl, types, typesName, source):
        world = World();
        world.imgUrl = imgUrl
        world.name = name
        world.description = description
        world.types = types
        world.typesName = typesName
        world.intro = intro
        world.source = source
        world =  sflt.worldDao.add(world);
        return world;

    def select(sflt,name):
        world = sflt.worldDao.selectByWname(name)
        if (world is None):
            return None;
        return world;