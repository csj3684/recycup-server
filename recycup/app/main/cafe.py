from app.main.dataBase import dataBase
from common import *
import os

cafe = Blueprint('cafe', __name__)

@cafe.route('/')
def sp_cafePage():
    return "cafePage"


@cafe.route('/duplicateCheck', methods = ['GET', 'POST'])
def duplicateCheck():

    db = dataBase()
    cafeID = request.form['cafeId']
    print("cafeID : {}".format(cafeID))
    jsonDict = {}

    try:
        sql = "select cafeID from recycup.cafe where cafeID = %s"
        db.cursor.execute(sql, (cafeID))
        if db.cursor.fetchone() == None:
            jsonDict['duplicate'] = False
        else:
            jsonDict['duplicate'] = True
        jsonDict['success'] = True
        db.connector.commit()

    except Exception as e:
        jsonDict['success'] = False
        jsonDict['error'] = "server error"
        print("error in 'cafe.py > duplicateCheck' : {}\n\n".format(e))

    else:
        pass

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@cafe.route('/cafeInfo/register', methods = ['GET', 'POST'])
def registerCafe():

    db = dataBase()
    cafeID = request.form['cafeId']
    password = request.form['cafePassword']
    headName = request.form['headName']
    cafeName = request.form['cafeName']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    jsonDict = {}

    print('headName : ',headName)

    try:
        sql = "insert into recycup.cafe(cafeID, password, headName, cafeName, latitude, longitude) values(%s, %s, %s, %s, %s, %s)"
        db.cursor.execute(sql, (cafeID, password, headName, cafeName, latitude, longitude))
        
        sql = "select type from recycup.head where headName = %s"
        db.cursor.execute(sql, (headName))
        material = db.cursor.fetchone()['type']

        db.connector.commit()

    except Exception as e:
        print("Error in 'cafe.py > registerCafe' : {}\n\n".format(e))
        jsonDict['success'] = False,
        jsonDict['error'] = "server error"

    else:
        jsonDict['success'] = True
        jsonDict['headName'] = headName
        jsonDict['cafeName'] = cafeName
        jsonDict['material'] = material

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')

@cafe.route('/cafeInfo/signIn', methods = ['GET', 'POST'])
def cafeSignIn():

    db = dataBase()
    cafeID = request.form['cafeId']
    password = request.form['cafePassword']
    jsonDict = {}

    try:
        sql = "select cafe.headName as headName, cafe.cafeName as cafeName, head.type as type from recycup.cafe join recycup.head on recycup.cafe.headName = recycup.cafe.headName where cafeID = %s and password = %s"
        db.cursor.execute(sql, (cafeID, password))
        row = db.cursor.fetchone() 
        if row == None:
            jsonDict['success'] = False
            jsonDict['error'] = "No such (ID, password) exists"
        else:
            jsonDict['success'] = True
            headName = row['headName']
            cafeName = row['cafeName']
            material = row['type']



    except Exception as e:
        print("Error in 'cafe.py > cafeSignIn' : {}\n\n".format(e))
        jsonDict['success'] = False
        jsonDict['error'] = "server error"

    else:
        jsonDict['headName'] = headName
        jsonDict['cafeName'] = cafeName
        jsonDict['material'] = material

    finally:
        print(jsonDict)
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')


@cafe.route('/headInfo/get', methods = ['GET', 'POST'])
def getHeadInfo():

    db = dataBase()
    headInfos = []
    try:
        db.cursor.execute("SELECT * FROM recycup.head")
        rows = db.cursor.fetchall()
        db.connector.commit()

    except Exception as e:
        print("Error in 'cafe.py > getCafeInfo' : {}\n\n".format(e))

    else:
        for row in rows:
            print(row)
            headInfos.append({'headName': row['headName'],
                              'logoPath': row['logoPath'],
                              'type': row['type']})
    finally:
        db.dbDisconnect()

    return json.dumps(headInfos).encode('utf-8')

@cafe.route('/cafeInfo/get', methods = ['GET', 'POST'])
def getCafeInfo():

    db = dataBase()
    headName = request.form['cafeName']
    cafeInfos = []

    try:
        db.cursor.execute("select * from recycup.cafe where headName = %s", (headName))
        rows = db.cursor.fetchall()
        db.connector.commit()

    except Exception as e:
        print("Error in 'cafe.py > getCafeInfo':{}\n\n".format(e))

    else:
        for row in rows:
            cafeInfos.append({'headName' : row['headName'],
                              'cafeName': row['cafeName'],
                              'latitude': row['latitude'],
                              'longitude': row['longitude']})
    finally:
        db.dbDisconnect()

    return json.dumps(cafeInfos).encode('utf-8')


@cafe.route('/cafeInfo/edit', methods = ['GET', 'POST'])
def editCafeInfo():

    db = dataBase()
    cafeID = request.form['cafeID']
    password = request.form['password']
    headName = request.form['headName']
    cafeName = request.form['cafeName']
    location = request.form['location']

    print("cafeID : {}".format(cafeID))
    print("password : {}".format(password))
    print("headName : {}".format(headName))
    print("cafeName: {}".format(cafeName))
    print("latitude: {}".format(location[0]))
    print("longitude : {}".format(location[1]))

    try:
        sql = "update recycup.cafe set password = %s, headName = %s, cafeName = %s, latitude = %s, longitude = %s where cafeID = %s"
        db.cursor.execute(sql, (password, headName, cafeName, location[0], location[1], cafeID))
        
        db.connector.commit()
    except Exception as e:
        print("Error in 'capy.py > editCafeInfo':{}\n\n".format(e))
        jsonDict = {'success' : False,
                    'error' : "server error"}

    else:
        jsonDict = {'success' : True,
                    'cafeID' : cafeID,
                    'password' : password,
                    'headName' : headName,
                    'cafeName' : cafeName,
                    'location' : (location[0], location[1])}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')
        


@cafe.route('/head/login', methods = ['GET', 'POST'])
def headLogin():
    return render_template('/main.html')