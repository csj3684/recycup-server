import mysql.connector

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
        self.connector = mysql.connector.connect(host='35.229.219.32:8888',
                                                 user='admin',
                                                 password='',
                                                 db='dailyhappiness',
                                                 charset='utf8')

    def setCursorDic(self):
        self.cursor = self.conn.cursor(dictionary=True)

    def dbDisconnect(self):
        self.connector.close()