import pymysql
from dbutils.persistent_db import PersistentDB
persist = PersistentDB(pymysql, 10, host='', db='', user='', password='')
class DBMysqlUtil:
   def __init__(self):
       print("DBMysqlUtil csh")

   # 定义一个函数来执行SQL语句并获取结果
   def execute_query(slft,sql, values=None):
       with persist.connection() as conn:
           try:
               with conn.cursor() as cursor:
                   cursor.execute(sql, values)
                   results = cursor.fetchall()
               return results
           except Exception as e:
               # 处理异常
               print(f"Error executing SQL: {str(e)}")
               return None

   def execute_query_one(slft,sql, values=None):
       with persist.connection() as conn:
           try:
               with conn.cursor() as cursor:
                   cursor.execute(sql, values)
                   results = cursor.fetchone()
               return results
           except Exception as e:
               # 处理异常
               print(f"Error executing SQL: {str(e)}")
               return None

   # 定义一个函数来执行SQL语句并插入数据
   def execute_insert(slft,sql, values):
       with persist.connection() as conn:
           try:
               with conn.cursor() as cursor:
                   cursor.execute(sql, values)
               conn.commit()
           except Exception as e:
               # 处理异常
               print(f"Error inserting data: {str(e)}")

   def execute_update(slft, sql, values):
       with persist.connection() as conn:
           try:
               with conn.cursor() as cursor:
                   cursor.execute(sql, values)

               conn.commit()
           except Exception as e:
               # 处理异常
               print(f"Error inserting data: {str(e)}")
# 使用示例
# select_sql = "SELECT * FROM wiki_world WHERE id = %s"
# # insert_sql = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
#
# # 查询数据
# results = execute_query(select_sql, (1,))
# if results:
#     for row in results:
#         print(row)
#
# # 插入数据
# insert_values = ("value1", "value2")
# execute_insert(insert_sql, insert_values)

import datetime
import time

# 获取当前时间（包括毫秒）
current_time = datetime.datetime.now()

# 提取毫秒部分
sjc = int(time.time() * 1000)

# 打印当前时间和毫秒
print("时间戳:", sjc)
