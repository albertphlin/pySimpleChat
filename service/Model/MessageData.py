class MessageData(object):
    def __init__(self) -> None:
        self.Topic = ""
        self.User = 0       # 所得
        self.IP = 0         # 成本
        self.Message = 0    # 重量
        self.tDateTime = "" # 開始日期

    def to_dict(self):
        return {
            "Topic": self.Topic,
            "User": self.User,
            "IP": self.IP,
            "Message": self.Message,
            "tDateTime": self.tDateTime
            }