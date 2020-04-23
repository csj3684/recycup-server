import pymysql

print("database.py")

# < connector >
# commit()

# < cursor >
# execute() : SQL 을 DB로, cursor.execute("%s, ..., %s", (parameter1, parameter2))
# fetchall(), fetchone(), fetchmany() : Data 를 server로, execute() 보내고 DB로부터 온 Data 읽기

class dateBase:
    def __init__(self):
        self.dbConnect()
        self.setCursorDic()

    def dbConnect(self):
        self.connector = pymysql.connect(host='localhost',
                                        user='root',
                                        password='caucse',
                                        db='RecyCup',
                                        charset='utf8')

    def setCursorDic(self):
        self.cursor = self.connector.cursor()

    def dbDisconnect(self):
        self.connector.close()