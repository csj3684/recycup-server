from app.main.dataBase import dateBase


@app.route('/signUp', method = ['GET', 'POST'])
def createAccount():
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

@app.route('/signIn', method = ['GET', 'POST'])
def signIn():
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

@app.route('/duplicateCheck', method = ['GET', 'POST'])
def duplicateCheck():
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


@app.route('/cupInfo/get', method = ['GET', 'POST'])
def getCupInfo():
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










