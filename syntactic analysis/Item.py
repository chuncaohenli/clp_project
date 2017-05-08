class Comment:
    def __init__(self,content,creationTime,id,pid):
        self.content = content
        self.date = creationTime
        self.id = id
        self.productID = pid

class HotTag:
    def __init__(self,name,pid,count):
        self.name = name
        self.productID = pid
        self.count = count