class Chapter:
    def __init__(self, title="", status=0, serialNumber=0, pid=0, level=0, wid=0, sid=0, content="", pname="", sname="",upId=0,downId=0):
        self.id = 0  # 如果需要设置默认值的属性，可以在这里初始化
        self.title = title
        self.status = status
        self.serialNumber = serialNumber
        self.pid = pid
        self.level = level
        self.wid = wid
        self.sid = sid
        self.content = content
        self.pname = pname
        self.sname = sname
        self.upId = upId
        self.downId = downId

    def __str__(self):
        return f"Chapter(title='{self.title}', wid={self.wid}, sid={self.sid})"
