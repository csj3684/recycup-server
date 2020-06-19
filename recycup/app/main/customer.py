from app.main.dataBase import dataBase
from common import *

customer = Blueprint('customer', __name__)

@customer.route('/')
def sp_customerPage():
    return "sp_customerPage"

@customer.route('/duplicateCheck', methods = ['GET', 'POST'])
def duplicateCheck():

    db = dataBase()
    phoneNumber = request.form['phoneNumber']
    print("phoneNumber : {}".format(phoneNumber))

    try:
        sql = "select * from recycup.user where phoneNumber = %s"
        db.cursor.execute(sql, (phoneNumber))
        if db.cursor.fetchone() == None:
            duplicate = False
        else:
            duplicate = True

        db.connector.commit()

    except Exception as e:
        jsonDict = {'duplicated' : "server error"}
        print("error in 'customer.py > duplicateCheck':{}\n\n".format(e))

    else:
        jsonDict = {'duplicate': duplicate}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@customer.route('/signUp', methods = ['GET', 'POST'])
def createAccount():

    db = dataBase()
    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    name = request.form['name']

    print("phoneNumber : {}".format(phoneNumber))
    print("password : {}".format(password))
    print("name : {}".format(name))

    try:
        sql = "insert into recycup.user(phoneNumber, password, name, point) values(%s, %s, %s, %s)"
        db.cursor.execute(sql,(phoneNumber, password,name,0))
        db.connector.commit()

    except Exception as e:
        jsonDict = {'success' : False,
                    'error' : "server error"}
        print("error in 'customer.py > createAcount' : {}\n\n".format(e))
        
    else:
        jsonDict = {'success' : True,
                    'phoneNumber' : phoneNumber,
                    'password' : password,
                    'name' : name}
    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@customer.route('/signIn', methods = ['GET', 'POST'])
def signIn():

    db = dataBase()
    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    name = None
    point = None
    jsonDict = {}
    
    try:
        sql = "select * from recycup.user where phoneNumber = %s and password = %s"
        db.cursor.execute(sql,(phoneNumber, password))
        row = db.cursor.fetchone() 

        if row == None:
            jsonDict['success'] = False
            jsonDict['error'] = "No such (ID, password) exists"
        else:
            jsonDict['success'] = True
            name = row['name']
            point = row['point']


        db.connector.commit()

    except Exception as e:
        jsonDict['success'] = False
        jsonDict['error'] = "server error"
        print("error in 'customer.py > signIn': {}\n\n".format(e))

    else:
        jsonDict['name'] = name
        jsonDict['point'] = point
        jsonDict['phoneNumber'] = phoneNumber
        jsonDict['password'] = password

    finally:
        db.dbDisconnect()

    print(jsonDict)
    return json.dumps(jsonDict).encode('utf-8')



@customer.route('/customerInfo/get', methods = ['GET', 'POST'])
def getCustomerInfo():

    db = dataBase()
    phoneNumber = request.form['phoneNumber']
    thisYear = datetime.now().year
    thisMonth = datetime.now().month

    try:
        sql = "select coalesce(sum(amount), 0) as totalSales from recycup.sales where phoneNumber = %s and year(date) = %s and month(date) = %s"
        db.cursor.execute(sql, (phoneNumber, thisYear, thisMonth))
        totalSales = int(db.cursor.fetchone()['totalSales'])
       
        sql = "select coalesce(sum(amount), 0) as totalReturn from recycup.recycle where phoneNumber = %s and year(date) = %s and month(date) = %s"
        db.cursor.execute(sql, (phoneNumber, thisYear, thisMonth))
        totalReturn = int(db.cursor.fetchone()['totalReturn'])

        sql = "select point from recycup.user where phoneNumber = %s"
        db.cursor.execute(sql, (phoneNumber))
        point = db.cursor.fetchone()['point']

        db.connector.commit()

    except Exception as e:
        jsonDict = {'success' : False,
                    'error' : "server error"}
        print("error in 'customer.py > getCustomerInfo':{}\n\n".format(e))

    else:
     
        jsonDict = {'success': True,
                    'sales' : totalSales,
                    'return' : totalReturn,
                    'point' : point}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')

@customer.route('/customerInfo/edit', methods = ['GET', 'POST'])
def editCustomerInfo():

    db = dataBase()
    historicalPhoneNumber = request.form['historicalPhoneNumber']
    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    name = request.form['name']

    try:
        sql = "update recycup.user set phoneNumber = %s, password = %s, name = %s where phoneNumber = %s"
        db.cursor.execute(sql, (phoneNumber, password, name, historicalPhoneNumber))

        isSuccess = True
        
        db.connector.commit()
    except Exception as e:
        jsonDict = {'success' : False,
                    'error' : "server error"}
        print("Error in 'sp_customer.py > editCustomerInfo': {}\n\n".format(e))
        

    else:
        jsonDict = {'success' : True,
                    'phoneNumber' : phoneNumber,
                    'password' : password,
                    'name' : name}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')

@customer.route('/charge', methods = ['GET', 'POST'])
def charge():

    db = dataBase()
    phoneNumber = request.form['phoneNumber']
    amount = request.form['amount']

    try:
        # user 포인트 증가
        sql = "update recycup.user set point = point + %s where phoneNumber = %s"
        db.cursor.execute(sql, (amount, phoneNumber))

        # recycup cash(deposit) 증가
        sql = "update recycup.information set deposit = deposit + %s"
        db.cursor.execute(sql, (amount))

        sql = "select point from recycup.user where phoneNumber = %s"
        db.cursor.execute(sql, (phoneNumber))
        point = db.cursor.fetchone()['point']
        db.connector.commit()

    except Exception as e:
        jsonDict = {'success' : False,
                    'error' : "server error"}
        print("error in 'customer.py > charge':{}\n\n".format(e))
        

    else:
        jsonDict = {'success' : True,
                    'phoneNumber' : phoneNumber,
                    'point' : point}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')
