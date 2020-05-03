from app.main.dataBase import dateBase
from common import *

server = Blueprint('server', __name__)

# User Table
    # [phoneNumber] : CHAR(13)
    # password : VARCHAR(12)
    # name : VARCHAR(10)
    # account : not yet...

# Cafe Table
    # [id] : CHAR(12)
    # password : VARCHAR(12)
    # name : 
    # type
    # account : not yet...

# Sales Table
    # [PhoneNumber] : CHAR(13)
    # [id] : CHAR(12)
    # [date] : DATE
    # amount : INT(11)

# Return Table
    # [phoneNumber] : CHAR(13)
    # [id] : CHAR(12)
    # [date] : DATE
    # amount : INT(11)

"""
1. 카카오페이에서 결제하여 포인트 충전
2. 결제시 음료값만 결제, 보증금은 포인트에서 자동 차감
3. 회수시 포인트로 회수
(4. point를 다시 cash로 환전할 수 있어야 할 것 같음.)
(5. 각 고객이 충전한 금액을 저장해 놓았다가, 환전시 충전 금액 초과분은 지급 X)
(6. 즉, 한사람이 여러잔 사고 돌릴경우, 반납시, 산사람 핸드폰번호로 반납하거나, 직접 방문 반납하기)
"""

@server.route('/sales', methods = ['GET', 'POST'])
def sales():
    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    cafeID = request.form['cafeID']
    date = request.form['date']
    amount = request.form['amount']
    
    try:
        db.cursor.execute("select * from RecyCup.Sales WHERE phoneNumber = {} and cafeID = {} and date = {}".format(phoneNumber, cafeID, date))

        if db.cursor.fetchone() == None:
            db.cursor.execute("insert into RecyCup.Sales(phoneNumber, cafeID, date, amount) values({}, {}, {}, {})".format(phoneNumber, cafeID, date, amount))
        else:
            db.cursor.execute("update RecyCup.Sales set amount = amount + {} where phoneNumber = {} and cafeID = {} and date = {}".format(amount, phoneNumber, careID, date))

        db.cursor.execute("SELECT point FROM RecyCup.User WHERE phoneNumber = {}".format(phoneNumber))
        point = db.cursor.fetchone()
        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("Error %d: %s" % (e.args[0], e.args[1]))
    
    else:
        jsonDict = {"phoneNumber" : phoneNumber,
                    "cafeID" : cafeID,
                    "date" : date,
                    "amount" : amount,
                    "point" : point)}
    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@server.route('/return', methods = ['GET', 'POST'])
def cupReturn():

    print("cupReturn")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    deposit = request.form['deposit']

    try:
        db.cursor.execute("UPDATE RecyCup.User SET point = point + {} WHERE phoneNumber = {}".format(deposit, phoneNumber))
        db.cursor.execute("SELECT point FROM RecyCup.User WHERE phoneNumber = {}".format(phoneNumber))
        point = db.cursor.fetchone()
        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print(e)

    else:
        jsonDict = {'phoneNumber' : phoneNumber,
                    'point' : point}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@server.route('/update', methods = ['GET', 'POST'])
def update():

    print("update")
    
    db = dateBase()

    try:


        db.cursor.execute("truncate RecyCup.Sales")
        db.cursor.execute("truncate RecyCup.Return")
    
        db.connector.commit()

    except Exception as e:
        jsonDict = {'isSuccess' : False}
        print(e)

    else:
        jsonDict = {'isSuccess' : True}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')

    

