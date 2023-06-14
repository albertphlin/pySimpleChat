class FileData(object):
    def __init__(self) -> None:
        self.Topic = ""
        self.User = 0       # 所得
        self.FileName = 0    # 重量
        self.tDateTime = "" # 開始日期

    def to_dict(self):
        return {
            "Topic": self.Topic,
            "User": self.User,
            "FileName": self.FileName,
            "tDateTime": self.tDateTime
            }