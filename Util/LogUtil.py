import logging

# 创建一个 logger 对象
logger = logging.getLogger(__name__)

# 设置 logger 的级别
logger.setLevel(logging.INFO)

# 添加一个 handler 对象
handler1 = logging.StreamHandler()

# 设置 handler 的格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler1.setFormatter(formatter)

# 将 handler 添加到 logger 对象中
logger.addHandler(handler1)

# 添加一个 handler 对象
handler2 = logging.FileHandler('log.txt')

# 设置 handler 的格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler2.setFormatter(formatter)

# 将 handler 添加到 logger 对象中
logger.addHandler(handler2)
def info(log):
   # 记录日志
   logger.info(log)
def debug(log):
   # 记录日志
   logger.debug(log)
def warning(log):
   # 记录日志
   logger.warning(log)
def error(log):
   # 记录日志
   logger.error(log)