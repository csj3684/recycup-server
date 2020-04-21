from app.main.dataBase import dateBase
from common import *

mainPage = Blueprint('mainPage', __name__)

@mainPage.route('/')
def showMainPage():
    return render_template('/mainPage.html')

@mainPage.route('/signUp', methods = ['GET', 'POST'])
def createAccount():

    print("회원가입")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    name = request.form['name']

    # DB : 회원으로 저장
    sql = "INSERT INTO User(phoneNumber, password, name) VALUES(%s,%s,%s)"

    try:
        db.cursor.execute(sql, (phoneNumber, password, name))
        db.connector.commit()

    except mysql.connector.Error as e:
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

    print("로그인")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    password = request.form['password']

    # DB : 회원인지 확인
    sql = "SELECT * FROM User WHERE phoneNumber = %s and password = %s"

    try:
        db.cursor.execute(sql, (phoneNumber, password))

        if db.cursor.fetchone() == None:
            isSuccess = False
        else:
            isSuccess = True

    except mysql.connector.Error as e:
        jsonDict = None
        print("Error %d: %s" % (e.args[0], e.args[1]))

    else:
        jsonDict = {'success' : isSuccess}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')

@mainPage.route('/duplicateCheck', methods = ['GET', 'POST'])
def duplicateCheck():

    print("중복 체크")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']

    # DB : 중복체크
    sql = "SELECT * FROM User WHERE phoneNumber = %s"
    try:
        db.cursor.execute(sql, (phoneNumber))
        if db.curs.fetchone() == None:
            isDuplicated = False
        else:
            isDuplicated = True

    except Exception as e:
        jsonDict = None
        print(e)

    else:
        jsonDict = {'duplicate': isDuplicated}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@mainPage.route('/cupInfo/get', methods = ['GET', 'POST'])
def getCupInfo():

    print("사용자 컵 정보")

    db = dateBase()

    phoneNumber = request.form['phoneNumber']
    jsonArray = []

    sql = "SELECT * FROM User WHERE phoneNumber = %s"
    try:
        rows = db.cursor.execute(sql, (phoneNumber))

    except Exception as e:
        jsonArray = None
        print(e)

    else:
        for row in rows:
            jsonArray.append({'cafeID': row['cafeID'],
                              'cafeName': row['cafeName'],
                              'cumNumber': row['cupNumber'],
                              'cafeLogo': row['cafeLogo'],
                              'dueDate': row['dueDate']})

    finally:
        db.dbDisconnect()

    return json.dumps(jsonArray).encode('utf-8')










