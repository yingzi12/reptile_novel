# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse

import oss2
import requests
import urllib3
from oss2.credentials import EnvironmentVariableCredentialsProvider
from sqlalchemy.sql.functions import current_date
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 填写RAM用户的访问密钥（AccessKey ID和AccessKey Secret）。
accessKeyId = ''
accessKeySecret = ''
# 使用代码嵌入的RAM用户的访问密钥配置访问凭证。
auth = oss2.Auth(accessKeyId, accessKeySecret)
# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称。
bucket = oss2.Bucket(auth, '', '')
def upload(url,path=""):
    # requests.get返回的是一个可迭代对象（Iterable），此时Python SDK会通过Chunked Encoding方式上传。
    parsed_url = urlparse(url)
    # 从路径中获取最后一部分
    last_part = parsed_url.path.split("/")[-1]
    formatted_date = current_date.strftime("%m%d")
    path=formatted_date+"/"+path
    # 填写网络流地址。
    input = requests.get(url, verify=False)

    # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
    bucket.put_object("story/" +path+"/"+last_part, input)


def uploadChapter(url,path=""):
    # requests.get返回的是一个可迭代对象（Iterable），此时Python SDK会通过Chunked Encoding方式上传。
    # 使用 urlparse 函数解析 URL
    parsed_url = urlparse(url)
    # 获取除域名之外的部分
    path_without_domain = parsed_url.path
    path=path+"/"+path_without_domain
    # 填写网络流地址。
    input = requests.get(url, verify=False)
    # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
    bucket.put_object("chapter" + path+"", input)

uploadChapter("https://www.x23zw.com/book/282845/25.html")