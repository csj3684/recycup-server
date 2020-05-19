from common import *
from app import app
from app.main.dataBase import dataBase

@app.route("/")
def mainPage():                           
    return "mainPage"

@app.route("/test")
def test():
    db = dataBase()

    userName = '캡스톤'
    phoneNumber = '01065453152'

    point = 1000

    try:
        db.cursor.execute("select * from User where name = '{}'".format(userName))
        print(db.cursor.fetchone()['name'])

        db.cursor.execute("select * from User where phoneNumber = {}".format(phoneNumber))
        print(db.cursor.fetchone()['phoneNumber'])
    except Exception as e:
        print(e)
        isSuccess = None

    else:
        isSuccess = True

    finally:
        db.dbDisconnect()

    return json.dumps(isSuccess).encode('utf-8')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

