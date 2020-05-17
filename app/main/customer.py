from app.main.dataBase import dateBase
from common import *

customer = Blueprint('customer', __name__)

@customer.route('/duplicateCheck', methods = ['GET', 'POST'])
def duplicateCheck():

    print("duplicateCheck")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']

    print("phoneNumber : {}".format(phoneNumber))

    try:
        db.cursor.execute("select * from RecyCup.User where phoneNumber = {}".format(phoneNumber))
        if db.cursor.fetchone() == None:
            isDuplicated = False
        else:
            isDuplicated = True

        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'duplicateCheck'", e)
        print("\n\n\n")

    else:
        jsonDict = {'duplicate': isDuplicated}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@customer.route('/signUp', methods = ['GET', 'POST'])
def createAccount():

    print("signUp")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    name = request.form['name']

    print("phoneNumber : {}".format(phoneNumber))
    print("password : {}".format(password))
    print("name : {}".format(name))

    try:
        sql = "insert into RecyCup.User(phoneNumber, password, name, point) values(%s, %s, %s, %s)"
        print(sql)
        db.cursor.execute(sql,(phoneNumber, password,name,0))
        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'createAcount'", e)
        print("\n\n\n")
    
    else:
        jsonDict = {'phoneNumber' : phoneNumber,
                    'password' : password,
                    'name' : name}
    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@customer.route('/signIn', methods = ['GET', 'POST'])
def signIn():

    print("signIn")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    name = None

    try:
        sql = "select * from RecyCup.User where phoneNumber = %s and password = %s"
        print(sql)
        db.cursor.execute(sql,(phoneNumber, password))
        row = db.cursor.fetchone() 

        if row == None:
            isSuccess = False
        else:
            isSuccess = True
            print(row)
            name = row['name']

        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'signIn'", e)
        print("\n\n\n")

    else:
        jsonDict = {'phoneNumber' : phoneNumber,
                    'password' : password,
                    'name' : name}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')



@customer.route('/customerInfo/get', methods = ['GET', 'POST'])
def getCustomerInfo():

    print("customerInfo")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']

    try:
        db.cursor.execute("select sum(amount) as totalSales from RecyCup.Sales where phoneNumber = {}".format(phoneNumber))
        totalSales = db.cursor.fetchone()['totalSales']
        totalSales = 0 if totalSales == None else int(totalSales)
       
    
        db.cursor.execute("select sum(amount) as totalReturn from RecyCup.Recycle where phoneNumber = {}".format(phoneNumber))
        totalReturn = db.cursor.fetchone()['totalReturn']
        totalReturn = 0 if totalReturn == None else int(totalReturn)


        db.cursor.execute("select point from RecyCup.User where phoneNumber = {}".format(phoneNumber))
        point = db.cursor.fetchone()['point']


        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'getCustomerInfo'", e)
        print("\n\n\n")

    else:
     
        jsonDict = {'sales' : totalSales,
                    'return' : totalReturn,
                    'point' : point}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@customer.route('/charge', methods = ['GET', 'POST'])
def charge():
    print("charge")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    amount = request.form['amount']

    try:
        db.cursor.execute("update RecyCup.User set point = point + {} where phoneNumber = {}".format(amount, phoneNumber))
        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'charge'", e)
        print("\n\n\n")

    else:
        jsonDict = {"isSuccess" : True}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')
