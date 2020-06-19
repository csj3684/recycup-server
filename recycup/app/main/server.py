from app.main.dataBase import dataBase
from common import *
import os

server = Blueprint('server', __name__)

@server.route('/isUser', methods = ['GET', 'POST'])
def isUser():
    db = dataBase()

    phoneNumber = request.form['phoneNumber']
    try:
        sql = "select phoneNumber from recycup.user where phoneNumber = %s"
        db.cursor.execute(sql, (phoneNumber))
        if db.cursor.fetchone() == None:
            jsonDict = {'success' : True,
                        'isUser' : True}
        else:
            jsonDict = {'success' : True,
                        'isUser' : False}
    except Exception as e:
        jsonDict = {'success' : False}
        print("error in 'server.py > isUser' : {}\n\n".format(e))
    
    else:
        pass
    
    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@server.route('/sales', methods = ['GET', 'POST'])
def sales():
    db = dataBase()

    phoneNumber = request.form['phoneNumber']
    headName = request.form['headName']
    now = datetime.now()
    year = now.year
    month = "0{}".format(now.month) if now.month < 10 else now.month
    day = "0{}".format(now.day) if now.day < 10 else now.day
    date = '%s%s%s'%(year, month, day)
    amount = int(request.form['amount'])

    try:
        # head server 연결 확인
        sql = "select url from recycup.head where headName = %s"
        db.cursor.execute(sql, (headName))
        url = db.cursor.fetchone()['url']
        requests.post(url) 

        # user point 감소
        sql = "update recycup.user set point = point - %s where phoneNumber = %s"
        db.cursor.execute(sql, (DEPOSIT * amount, phoneNumber))

        # recycup cash(deposit) 감소
        sql = "update recycup.information set deposit = deposit - %s"
        db.cursor.execute(sql, (DEPOSIT * amount))
        
        # recycup sales update
        sql = 'select phoneNumber from recycup.sales where phoneNumber = %s and headName = %s and date = %s'
        db.cursor.execute(sql, (phoneNumber, headName, date))
        if db.cursor.fetchone() == None:
            sql = 'insert into recycup.sales(phoneNumber, headName, date, amount) values(%s, %s, %s, %s)'
            db.cursor.execute(sql, (phoneNumber, headName, date, amount))
        else:
            sql = 'update recycup.sales set amount = amount + %s where phoneNumber = %s and headname = %s and date = %s'
            db.cursor.execute(sql, (amount, phoneNumber, headName, date))
        
        # head 에 sales request
        requests.post("%s/server/sales"%(url), {'phoneNumber' : phoneNumber, 'date' : date, 'amount' : amount, 'status' : 'in'}) 

        db.connector.commit()

    except requests.exceptions.ConnectionError:
        jsonDict = {"success" : False,
                    "msg" : "{} server is not running".format(headName)}
        print("{} server is not running".format(headName))

    except Exception as e:
        jsonDict = {"success" : False,
                    "msg" : "server error"}
        print("error in 'server.py > sales' : {}\n\n".format(e))
        
    else:
        jsonDict = {'success' : True,
                    'headName' : headName,
                    'amount' : amount}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@server.route('/recycle', methods = ['GET', 'POST'])
def cupReturn():
    db = dataBase()

    phoneNumber = request.form['phoneNumber']
    headName = request.form['headName']
    cupHeadName = request.form['cupHeadName']

    if headName == "pet쓰레기통":
        headName = cupHeadName

    print(headName)

    now = datetime.now()
    year = now.year
    month = "0{}".format(now.month) if now.month < 10 else now.month
    day = "0{}".format(now.day) if now.day < 10 else now.day
    date = '%s%s%s'%(year, month, day)
    amount = 1

    try:
        # head server 연결 확인
        sql = "select url from recycup.head where headName = %s"
        db.cursor.execute(sql, (headName))
        url = db.cursor.fetchone()['url']
        requests.post(url)

        # user point 증가
        sql = "update recycup.user set point = point + %s where phoneNumber = %s"
        db.cursor.execute(sql, (DEPOSIT * amount, phoneNumber))

        # recycup cash(deposit) 증가
        sql = "update recycup.information set deposit = deposit + %s"
        db.cursor.execute(sql, (DEPOSIT * amount))

        # recycup recycle update
        sql = 'select phoneNumber from recycup.recycle where phoneNumber = %s and headName = %s and date = %s'
        db.cursor.execute(sql, (phoneNumber, headName, date))
        if db.cursor.fetchone() == None:
            sql = 'insert into recycup.recycle(phoneNumber, headName, date, amount) values(%s, %s, %s, %s)'
            db.cursor.execute(sql, (phoneNumber, headName, date, amount))
        else:
            sql = 'update recycup.recycle set amount = amount + %s where phoneNumber = %s and headname = %s and date = %s'
            db.cursor.execute(sql, (amount, phoneNumber, headName, date))

        # head 에 recycle request
        requests.post("%s/server/recycle"%(url), {'phoneNumber' : phoneNumber, 'date' : date, 'amount' : amount, 'status' : 'out'})
        
        db.connector.commit()

    except requests.exceptions.ConnectionError:
        jsonDict = {"success" : False,
                    "msg" : "{} server is not running".format(headName)}
        print("{} server is not running".format(headName))

    except Exception as e:
        jsonDict = {"success" : False,
                    "msg" : "server error"}
        print("error in 'server.py > cupReturn' : {}\n\n".format(e))
        

    else:
         jsonDict = {'success' : True,
                    'headName' : headName,
                    'amount' : amount}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@server.route('/update', methods = ['GET', 'POST'])
def updateBody():

    if date.today().day != DAY_OF_THE_UPDATE:
        return json.dumps({'success' : False}).encode('utf-8')

    print("기록보관 업데이트, 현재시각 : {}".format(datetime.now()))

    db = dataBase()
    now = datetime.now()
    
    try:
        sql = 'delete from recycup.sales where year(date) = %s and month(date) = %s'
        db.cursor.execute(sql, (now.year - RETENTION_PERIOD, now.month))

        sql = 'delete from recycup.recycle where year(date) = %s and month(date) = %s'
        db.cursor.execute(sql, (now.year - RETENTION_PERIOD, now.month))
   
        db.connector.commit()
    
    except Exception as e:
        print("error in 'server.py > updateBody' : {}\n\n".format(e))

    else:
        pass

    finally:
        db.dbDisconnect()

    return json.dumps({'done' : True}).encode('utf-8')
    

def update():
    schedule.every().day.at(TIME_OF_THE_UPDATE).do(updateBody)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

@server.route('/recognition', methods = ['GET', 'POST'])
def recognition():
    return render_template('recognition.html')


@server.route('/headLogin', methods = ['GET', 'POST'])
def headLogin():
    return render_template('/headLogin.html')