class SQL:
    INSERT_MESSAGE = "INSERT INTO chat.Messages (Topic, User, IP, Message, tDateTime)\
                      VALUES ('{Topic}', '{User}', '{IP}', '{Message}', '{tDateTime}')"
    UPDATE_MESSAGE="UPDATE chat.Messages SET Topic={Topic}, User={User}, IP={IP}, Message={Message}, tDateTime={tDateTime} WHERE Id='{Id}'"
    QUERY_MESSAGE_BY_STIME_ETIME="SELECT * FROM chat.Messages WHERE tDateTime BETWEEN '{sTime}' and '{eTime}'"
    QUERY_MESSAGE_FROM_TIME_AT_TOPN="SELECT * FROM chat.Messages WHERE Topic = '{Topic}' and tDateTime < '{Time}' ORDER BY tDateTime DESC LIMIT {N}"


    INSERT_FILE = "INSERT INTO chat.Storage (Topic, User, FileName, tDateTime)\
                   VALUES ('{Topic}', '{User}', '{FileName}', '{tDateTime}')"
    QUERY_FILE_BY_TOPIC = "SELECT * FROM chat.Storage WHERE Topic='{Topic}'"