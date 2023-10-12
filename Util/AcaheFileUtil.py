import hashlib
import os

from Util import LogUtil

htmlPath="./html/"
class AcaheFileUtil:
    def save(self,content, url):
        md5name = self.md5(url)
        LogUtil.info("md5:" + url + "   " + md5name)
        # 指定文件路径和名称
        file_path = htmlPath+md5name + ".html";

        # 使用 "w" 模式打开文件（如果文件存在则覆盖，如果不存在则创建）
        with open(file_path, "w", encoding="utf-8") as file:
            # 将内容写入文件
            file.write(content)

        print(f"内容已保存到文件 {file_path}")
        return file_path;

    def saveFile(self,content, file_path):
        # md5name = self.md5(url)
        # LogUtil.info("md5:" + url + "   " + md5name)
        # 指定文件路径和名称
        # file_path = htmlPath+md5name + ".html";
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 使用 "w" 模式打开文件（如果文件存在则覆盖，如果不存在则创建）
        with open(file_path, "w", encoding="utf-8") as file:
            # 将内容写入文件
            file.write(content)

        print(f"内容已保存到文件 {file_path}")
        return file_path;

    def delete(self,url):
        md5name = self.md5(url)
        # 指定文件路径和名称
        file_path = htmlPath+md5name + ".html";
        # 使用os.remove()删除文件
        try:
            os.remove(file_path)
            print(f"文件 {file_path} 已成功删除。")
        except OSError as e:
            print(f"删除文件时发生错误：{e}")

    def md5(self,input_string):
        # 定义要计算哈希值的字符串

        # 创建一个 MD5 哈希对象
        md5_hash = hashlib.md5()

        # 更新哈希对象以处理输入字符串
        md5_hash.update(input_string.encode('utf-8'))
        md5_hex = md5_hash.hexdigest()

        # 获取 MD5 哈希值的十六进制表示
        return md5_hex;

    def exists(self,url):
        md5name = self.md5(url)
        # 指定文件路径和名称
        file_path = htmlPath+md5name + ".html";

        # 使用os.path.exists()检查文件是否存在
        if os.path.exists(file_path):
            return True;
        else:
            return False;

    def read(self,url):
        md5name = self.md5(url)
        # 指定文件路径和名称
        file_path = htmlPath+md5name + ".html";
        # 打开文件并读取整个内容
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
        return content;

