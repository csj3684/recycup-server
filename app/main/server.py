from app.main.dataBase import dataBase
from common import *
import os

server = Blueprint('server', __name__)

# User Table
    # [phoneNumber] : CHAR(11)
    # password : VARCHAR(100)
    # name : VARCHAR(45)
    # point : INT(11)

# Head Table
    # [headID] : VARCHAR(45)
    # logoPath : VARCHAR(100)
    # type : VARCHAR(45)

# Cafe Table
    # [cafeID] : CHAR(45)
    # password : VARCHAR(100)
    # headID : VARCHAR(45)      --> Head.headID

# Sales Table
    # [PhoneNumber] : CHAR(11)  --> User.phoneNumber 하고싶은데 안 됨...
    # [cafeID] : CHAR(45)       --> Cafe.cafeID 하고싶은데 안 됨...  슈퍼키라 그런듯?
    # [date] : DATE
    # amount : INT(11)

# Recycle Table
    # [phoneNumber] : CHAR(13)  --> User.phoneNumber 하고싶은데 안 됨...
    # [cafeID] : CHAR(45)       --> Cafe.cafeID 하고싶은데 안 됨...  슈퍼키라 그런듯?
    # [date] : DATE
    # amount : INT(11)

# Location Table
    # [cafeID] : VARCHAR(45)    --> Cafe.cafeID
    # latitude : FLOAT
    # longitude : FLOAT

"""
1. 카카오페이에서 결제하여 포인트 충전
2. 결제시 음료값만 결제, 보증금은 포인트에서 자동 차감
3. 회수시 포인트로 회수
(4. point를 다시 cash로 환전할 수 있어야 할 것 같음.)
(5. 각 고객이 충전한 금액을 저장해 놓았다가, 환전시 충전 금액 초과분은 지급 X)
(6. 즉, 한사람이 여러잔 사고 돌릴경우, 반납시, 산사람 핸드폰번호로 반납하거나, 직접 방문 반납하기)

발생가능한 문제점 : 
어떤 사람 비회원 A가 B 매장에서 음료를 그냥 사고, 길가다가 버림, 길을 지나가던 회원 C가 음료를 들고 반납처리함,
이 때 비회원 A가 B 매장에서 구매할 때 보증금은 B 로 들어감, 이후 C가 반납시 보증금회수는 C가 하면서, 지불은 우리가함.
크게 볼 때 반납도 잘이루어졌고 재활용에도 기여를 하였지만 고객 side 에선 A - C + , 매장 side 에선 B + 우리 - ... zero sum은 맞는데 ...
"""

@server.route('/sales', methods = ['GET', 'POST'])
def sales():
    db = dataBase()

    phoneNumber = request.form['phoneNumber']
    cafeID = request.form['cafeID']
    date = request.form['date']
    amount = request.form['amount']
    
    try:
        db.cursor.execute("select point from RecyCup.User where phoneNumber = {}".format(phoneNumber))
        point = db.cursor.fetchone()

        if point < deposit * amount:
            # 어림없음
            pass
            
        db.cursor.exceute("update RecyCup.User set point = point - {} where phoneNumber = {}".format(deposit * amount, phoneNumber))

        db.cursor.execute("select * from RecyCup.Sales where phoneNumber = {} and cafeID = {} and date = {}".format(phoneNumber, cafeID, date))

        if db.cursor.fetchone() == None:
            db.cursor.execute("insert into RecyCup.Sales(phoneNumber, cafeID, date, amount) values({}, {}, {}, {})".format(phoneNumber, cafeID, date, amount))
        else:
            db.cursor.execute("update RecyCup.Sales set amount = amount + {} where phoneNumber = {} and cafeID = {} and date = {}".format(amount, phoneNumber, careID, date))

        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'sales'", e)
        print("\n\n\n")
    
    else:
        jsonDict = {"phoneNumber" : phoneNumber,
                    "cafeID" : cafeID,
                    "date" : date,
                    "amount" : amount,
                    "point" : point}
    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@server.route('/return', methods = ['GET', 'POST'])
def cupReturn():

    print("cupReturn")

    db = dataBase()

    phoneNumber = request.form['phoneNumber']

    try:
        db.cursor.execute("update RecyCup.User set point = point + {} where phoneNumber = {}".format(deposit, phoneNumber))
        db.cursor.execute("select point from RecyCup.User where phoneNumber = {}".format(phoneNumber))
        point = db.cursor.fetchone()
        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'cupReturn'", e)
        print("\n\n\n")

    else:
        jsonDict = {'phoneNumber' : phoneNumber,
                    'point' : point}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@server.route('/update', methods = ['GET', 'POST'])
def update():

    print("update")
    
    db = dataBase()

    try:
        db.cursor.execute(" \
        select totalSales.cafeID as cafeID, sum(salesAmount - coalesce(returnAmount, 0)) as depositToBeReturned \
        from ( \
            (select phoneNumber, cafeID, sum(amount) as salesAmount \
            from RecyCup.Sales \
            group by phoneNumber, cafeID)totalSales \
            left outer join \
            (select phoneNumber, cafeID, sum(amount) as returnAmount \
            from RecyCup.Back \
            group by phoneNumber, cafeID)totalReturn \
            on totalSales.phoneNumber = totalReturn.phoneNumber and totalSales.cafeID = totalReturn.cafeID \
            ) \
        group by cafeID \
        ")
        
        rows = db.cursor.fetchall()
        jsonDict = {}
        for row in rows:
            jsonDict[row["cafeID"]] = row["depositToBeReturned"]
        
        db.cursor.execute("truncate RecyCup.Sales")
        db.cursor.execute("truncate RecyCup.Back")
    
        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'update'", e)
        print("\n\n\n")

    else:
        pass

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')



    
    