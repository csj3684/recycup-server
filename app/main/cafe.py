from app.main.dataBase import dataBase
from common import *
import os

cafe = Blueprint('cafe', __name__)

@cafe.route('/headInfo/get', methods = ['GET', 'POST'])
def getHeadInfo():
    print("headInfo")

    db = dataBase()
    headInfos = []
    try:
        db.cursor.execute("SELECT * FROM RecyCup.Head")
        rows = db.cursor.fetchall()
        db.connector.commit()
    except Exception as e:
        headInfos = None
        print("Error in 'getCafeInfo'", e); print("\n\n")

    else:
        for row in rows:
            print(row)
            headInfos.append({'headName': row['headID'],
                              'logoPath': row['logoPath'],
                              'type': row['type']})
    finally:
        db.dbDisconnect()

    return json.dumps(headInfos).encode('utf-8')

@cafe.route('/cafeInfo/get', methods = ['GET', 'POST'])
def getCafeInfo():
    print("cafeInfo")

    headName = request.form['cafeName']

    db = dataBase()
    cafeInfos = []
    try:
        db.cursor.execute("select * from RecyCup.Cafe where headID = %s", (headName))
        rows = db.cursor.fetchall()
        db.connector.commit()
    except Exception as e:
        print("Error in 'getCafeInfo'", e); print("\n\n")

    else:
        for row in rows:
            cafeInfos.append({'headID' : row['headID'],
                              'cafeID': row['cafeID'],
                              'latitude': row['latitude'],
                              'longitude': row['longitude']})
        print(cafeInfos)
    finally:
        db.dbDisconnect()

    return json.dumps(cafeInfos).encode('utf-8')


@cafe.route('/cafeInfo/edit', methods = ['GET', 'POST'])
def editCafeInfo():
    print("editCafeInfo")

    db = dataBase()
    cafeID = request.form['cafeID']
    password = request.form['password']
    headName = request.form['headName']
    location = request.form['location']


    try:
        sql = "update RecyCup.Cafe set password = %s, headID = %s, latitude = %s, longitude = %s where cafeID = %s"
        db.cursor.execute(sql, (password, headName, location[0], location[1], cafeID))

        isSuccess = True
        
        db.connector.commit()
    except Exception as e:
        print("Error in 'editCafeInfo'", e); print("\n\n")
        jsonDict = None

    else:
        jsonDict = {'cafeID' : cafeID,
                    'password' : password,
                    'headName' : headName,
                    'location' : (location[0], location[1])}

    finally:
        db.dbDisconnect()

    return json.dumps(jsonDict).encode('utf-8')
        
