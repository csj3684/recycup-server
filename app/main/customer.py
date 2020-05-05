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

    except Exception as e:
        jsonDict = None
        print("error in 'duplicateCheck'", e)

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
        db.cursor.execute("insert into RecyCup.User(phoneNumber, password, name, point) values({}, {}, {}, {})".format(phoneNumber, password, name, 0))
        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("error in 'createAcount'", e)
    
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
    name = request.form['name']

    try:
        db.cursor.execute("select * from RecyCup.User where phoneNumber = {} and password = {}".format(phoneNumber, password))

        if db.cursor.fetchone() == None:
            isSuccess = False
        else:
            isSuccess = True

    except Exception as e:
        jsonDict = None
        print("error in 'signIn'", e)

    else:
        jsonDict = {'phoneNumber' : phoneNumber,
                    'password' : password,
                    'name' : name}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')



@customer.route('/customerInfo', methods = ['GET', 'POST'])
def getCustomerInfo():

    print("customerInfo")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']

    try:
        db.cursor.execute("select sum(amount) from RecyCup.Sales where phoneNumber = {}".format(phoneNumber))
        totalSales = db.cursor.fetchone()

        db.cursor.execute("select sum(amount) from RecyCup.Back where phoneNumber = {}".format(phoneNumber))
        totalReturn = db.cursor.fetchone()
        

    except Exception as e:
        jsonDict = None
        print("error in 'getCustomerInfo'", e)

    else:
        jsonDict = {'sales' : totalSales,
                    'return' : totalReturn}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')




