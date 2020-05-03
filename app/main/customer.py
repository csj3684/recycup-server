from app.main.dataBase import dateBase
from common import *

mainPage = Blueprint('mainPage', __name__)

# User Table
    # [phoneNumber] : CHAR(13)
    # password : VARCHAR(12)
    # name : VARCHAR(10)
    # account : not yet...

# Cafe Table
    # [id] : CHAR(12)
    # password : VARCHAR(12)
    # name : 
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
    
     
@mainPage.route('/')
def showMainPage():
    return 'mainPage'

@mainPage.route('/signUp', methods = ['GET', 'POST'])
def createAccount():

    print("signUp")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    name = request.form['name']

    print("phoneNumber : {}".format(phoneNumber))
    print("password : {}".format(password))
    print("name : {}".format(name))
    
    # DB : 회원으로 저장
    sql = "INSERT INTO RecyCup.User(phoneNumber, password, name, point) VALUES({}, {}, {}, {})".format(phoneNumber, password, name, 0)

    try:
        db.cursor.execute(sql)
        db.connector.commit()

    except Exception as e:
        jsonDict = None
        print("Error %d: %s" % (e.args[0], e.args[1]))
    
    else:
        jsonDict = {'phoneNumber' : phoneNumber,
                    'password' : password,
                    'name' : name}
    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')

@mainPage.route('/signIn', methods = ['GET', 'POST'])
def signIn():

    print("signIn")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    name = request.form['name']

    # DB : 회원인지 확인
    sql = "SELECT * FROM RecyCup.User WHERE phoneNumber = {} and password = {}".format(phoneNumber, password)

    try:
        db.cursor.execute(sql)

        if db.cursor.fetchone() == None:
            isSuccess = False
        else:
            isSuccess = True

    except Exception as e:
        jsonDict = None
        print("Error %d: %s" % (e.args[0], e.args[1]))

    else:
        jsonDict = {'phoneNumber' : phoneNumber,
                    'password' : password,
                    'name' : name}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')

@mainPage.route('/duplicateCheck', methods = ['GET', 'POST'])
def duplicateCheck():

    print("duplicateCheck")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']

    print("phoneNumber : {}".format(phoneNumber))

    # DB : 중복체크
    sql = "SELECT * FROM RecyCup.User WHERE phoneNumber = {}".format(phoneNumber)
    try:
        db.cursor.execute(sql)
        if db.cursor.fetchone() == None:
            isDuplicated = False
        else:
            isDuplicated = True

    except Exception as e:
        jsonDict = None
        print("Error in dupclicateCheck :" ,e)

    else:
        jsonDict = {'duplicate': isDuplicated}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@mainPage.route('/CafeInfo/get', methods = ['GET', 'POST'])
def getCafeInfo():

    print("cupInfo")

    db = dateBase()

    jsonArray = []

    sql = "SELECT * FROM RecyCup.Cafe"
    try:
        rows = db.cursor.execute(sql)

    except Exception as e:
        jsonArray = None
        print(e)

    else:
        for row in rows:
            cafeLogo = rows['logoPath']
            jsonArray.append({'cafeLogo': cafeLogo,
                              'cafeName': row['cafeName'],
                              'cafeLoation': row['location']})
    finally:
        db.dbDisconnect()

    return json.dumps(jsonArray).encode('utf-8')


@mainPage.route('/return', methods = ['GET', 'POST'])
def cupReturn():

    print("cupReturn")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    deposit = request.form['deposit']

    sql = "UPDATE RecyCup.User SET point = point + {} WHERE phoneNumber = {}".format(deposit, phoneNumber)
    sql2 = "SELECT point FROM RecyCup.User WHERE phoneNumber = {}".format(phoneNumber)
    try:
        db.cursor.execute(sql)
        db.cursor.execute(sql2)

    except Exception as e:
        jsonDict = None
        print(e)

    else:
        point = db.cursor.fetchone()
        jsonDict = {'phoneNumber' : phoneNumber,
                    'point' : point}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')







