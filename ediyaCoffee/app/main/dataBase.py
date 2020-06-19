from commons import *

class dataBase:
    def __init__(self):
        self.dbConnect()
        self.setCursorDic()

    def dbConnect(self):
        self.connector = pymysql.connect(host='localhost',
                                        user='root',
                                        password='caucse',
                                        db='ediyacoffee',
                                        charset='utf8',
                                        cursorclass = pymysql.cursors.DictCursor)

    def setCursorDic(self):
        self.cursor = self.connector.cursor()

    def dbDisconnect(self):
        self.connector.close()