from app.main.dataBase import dataBase
from commons import *

server = Blueprint('server', __name__)


# starbucks' server 에 있는 포스 andriod와 연동된 sales 가정 

# 보증금 내역 DB에 저장
@server.route('/sales', methods = ['GET', 'POST'])
def sales():

    db = dataBase()
    phoneNumber = request.form['phoneNumber']
    date = request.form['date']
    amount = int(request.form['amount'])
    status = request.form['status']
    
    try:
        
        # starbucks cash(deposit) 증가
        sql = "update starbucks.information set deposit = deposit + %s"
        db.cursor.execute(sql, (amount * DEPOSIT))

        
        # sales 업데이트
        sql = 'select date from starbucks.sales where phoneNumber = %s and date = %s'
        db.cursor.execute(sql, (phoneNumber, date))

        if db.cursor.fetchone() == None:
            sql = 'insert into starbucks.sales(phoneNumber, date, amount) values(%s, %s, %s)'
            db.cursor.execute(sql, (phoneNumber, date, amount))
        else:
            sql = 'update starbucks.sales set amount = amount + %s where phoneNumber = %s and date = %s'
            db.cursor.execute(sql, (amount, phoneNumber, date))


        # depositFlow 업데이트
        sql = "select phoneNumber from starbucks.depositFlow where phoneNumber = %s and date = %s and status = %s"
        db.cursor.execute(sql, (phoneNumber, date, status))
        if db.cursor.fetchone() == None:
            sql = 'insert into starbucks.depositFlow(date, phoneNumber, amount, status, deposit) values(%s, %s, %s, %s, %s)'
            db.cursor.execute(sql, (date, phoneNumber, amount, status, amount * DEPOSIT))
        else:
            sql = 'update starbucks.depositFlow set amount = amount + %s, deposit = deposit + %s where phoneNumber = %s and date = %s and status = %s'
            db.cursor.execute(sql, (amount, amount * DEPOSIT, phoneNumber, date, status))


        db.connector.commit()

    except Exception as e:
        jsonDict = {"success": False}
        print("error in 'server.py > sales' : {}\n\n".format(e))

    else:
        jsonDict = {"success": True}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@server.route('/recycle', methods = ['GET', 'POST'])
def recycle():

    db = dataBase()
    phoneNumber = request.form['phoneNumber']
    date = request.form['date']
    amount = int(request.form['amount'])
    status = request.form['status']

    try: 
        # starbucks cash(deposit) 감소
        sql = "update starbucks.information set deposit = deposit - %s"
        db.cursor.execute(sql, (amount * DEPOSIT))

        # recycle 업데이트
        sql = 'select phoneNumber from starbucks.recycle where phoneNumber = %s and date = %s'
        db.cursor.execute(sql, (phoneNumber, date))
        if db.cursor.fetchone() == None:
            sql = 'insert into starbucks.recycle(phoneNumber, date, amount) values(%s, %s, %s)'
            db.cursor.execute(sql, (phoneNumber, date, amount))
        else:
            sql = 'update starbucks.recycle set amount = amount + %s where phoneNumber = %s and date = %s'
            db.cursor.execute(sql, (amount, phoneNumber, date))

        # depositFlow 업데이트
        sql = "select phoneNumber from starbucks.depositFlow where phoneNumber = %s and date = %s and status = %s"
        db.cursor.execute(sql, (phoneNumber, date, status))
        if db.cursor.fetchone() == None:
            sql = 'insert into starbucks.depositFlow(date, phoneNumber, amount, status, deposit) values(%s, %s, %s, %s, %s)'
            db.cursor.execute(sql, (date, phoneNumber, amount, status, amount * DEPOSIT))
        else:
            sql = 'update starbucks.depositFlow set amount = amount + %s, deposit = deposit + %s where phoneNumber = %s and date = %s and status = %s'
            db.cursor.execute(sql, (amount, amount * DEPOSIT, phoneNumber, date, status))

        db.connector.commit()

    except Exception as e:
        jsonDict = {"success": False}
        print("error in 'server.py > recycle' : {}\n\n".format(e))

    else:
        jsonDict = {"success": True}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')

    
@server.route('/test', methods = ['GET', 'POST'])
def test():
    db = dataBase()
    sql = "select COALESCE(sum(amount), 0) from recycup.recycle where month(date) = 3"
    db.cursor.execute(sql)
    print(db.cursor.fetchone())
    return "Done"


    
    