import json

from Util.DBMysqlUtil import DBMysqlUtil
from entity.World import World


class WorldDao:

    def __init__(self):
        self.dBMysqlUtil = DBMysqlUtil()

    def add(self, world):
       sql="insert into wiki_world (name,description,types,types_name,intro," \
           "ranks, exp, scores,status,img_url," \
           "source,is_private)  values  (%s,%s,%s,%s,%s," \
           "%s,%s,%s,%s,%s," \
           "%s,%s)"

       values=(world.name,world.description,world.types,world.typesName,world.intro,world.ranks,world.exp,world.scores,world.status,world.imgUrl,world.source,world.isPrive);
       self.dBMysqlUtil.execute_insert(sql,values);

       sql = "select id,name,source from wiki_world where name=%s";
       resluts = self.dBMysqlUtil.execute_query_one(sql, (world.name,));
       if (resluts is None):
           return None
       else:
           world = World();
           world.id = resluts[0];
           world.name = resluts[1];
           world.source = resluts[2];
           sql = "insert into wiki_manage (wid,wname,user_id,user_name,types) " \
                 " values  (%s,%s,%s,%s,%s)"
           values = (world.id, world.name, 1,"admin",1);
           self.dBMysqlUtil.execute_insert(sql, values);

           return world;

    def selectByWname(self,name):
       sql="select id,name,source from wiki_world where name=%s ";
       resluts = self.dBMysqlUtil.execute_query_one(sql, (name,));
       if(resluts is None):
           return None
       else:
           world=World();
           world.id=resluts[0];
           world.name = resluts[1];
           world.source = resluts[2];
           return world;