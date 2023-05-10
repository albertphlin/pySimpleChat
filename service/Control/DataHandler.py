import datetime

import Control.DBHandler as DB
import Model.CHATSQL as ModelCHATSQL
import Model.MessageData as messagedatatemplate

class DataHandler:
    def __init__(self) -> None:
        self.dbHandler = DB.DBHandler()
        self.CHATSQL= ModelCHATSQL.SQL

    def AddMessage(self, Topic, User, IP, Message, tDateTime=str(datetime.datetime.now())):
        self.dbHandler.DoSQL(self.CHATSQL.INSERT_MESSAGE.format(Topic=Topic,
                                                           User=User,
                                                           Message=Message,
                                                           IP=IP,
                                                           tDateTime=tDateTime))

    def QueryTopNMessagesByTime(self, Topic, N, Time):
        DataList = []
        dbresult = self.dbHandler.DoSQL(self.CHATSQL.QUERY_MESSAGE_FROM_TIME_AT_TOPN.format(Topic=Topic,
                                                                                       N=N,
                                                                                       Time=Time))
        for result in dbresult:
            data = messagedatatemplate.MessageData()
            data.Topic = str(result['Topic'])
            data.User = str(result['User'])
            data.IP = str(result['IP'])
            data.Message = str(result['Message'])
            data.tDateTime = str(result['tDateTime'])
            #DataList.append(data)
            DataList.insert(0, data) #倒序
            #print(f"[QueryTopNMessagesByTime] payload: {data.Topic, data.User, data.IP, data.Message, data.tDateTime}")
        return DataList