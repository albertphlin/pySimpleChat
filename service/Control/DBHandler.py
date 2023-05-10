from traceback import print_tb
import pymysql.cursors
import threading

class DBHandler:
    def __init__(self, host="localhost", user="pte", password="mis@6699", database="chat") -> None:
        # Connect to the database
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()
        self.lock = threading.Lock()

    def connect(self):
        self.connection = pymysql.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          database=self.database,
                                          cursorclass=pymysql.cursors.DictCursor)

    def DoSQL(self, sql):
        self.lock.acquire()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                self.connection.commit()
                result = cursor.fetchall()
            except pymysql.err.OperationalError:
                self.connect()
                print("[DBHandler]: re-connect mysql db.")
        self.lock.release()
        return result