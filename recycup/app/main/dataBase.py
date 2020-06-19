from common import *

# < connector >
# commit()

# < cursor >
# execute() : SQL 을 DB로, cursor.execute("%s, ..., %s", (parameter1, parameter2))
# fetchall(), fetchone(), fetchmany() : Data 를 server로, execute() 보내고 DB로부터 온 Data 읽기

class dataBase:
    def __init__(self):
        self.dbConnect()
        self.setCursorDic()

    def dbConnect(self):
        self.connector = pymysql.connect(host='localhost',
                                        user='root',
                                        password='caucse',
                                        db='recycup',
                                        charset='utf8',
                                        cursorclass = pymysql.cursors.DictCursor)

    def setCursorDic(self):
        self.cursor = self.connector.cursor()

    def dbDisconnect(self):
        self.connector.close()

class cafeDB:
    def __init__(self):
        self.dbConnect()
        self.setCursorDic()

    def dbConnect(self):
        self.connector = pymysql.connect(host='localhost',
                                        user='root',
                                        password='caucse',
                                        db='cafe',
                                        charset='utf8',
                                        cursorclass = pymysql.cursors.DictCursor)

    def setCursorDic(self):
        self.cursor = self.connector.cursor()

    def dbDisconnect(self):
        self.connector.close()
        