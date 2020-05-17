from app.main.dataBase import dateBase
from common import *
import os

cafe = Blueprint('cafe', __name__)

@cafe.route('/headInfo/get', methods = ['GET', 'POST'])
def getHeadInfo():
    print("headInfo")

    db = dateBase()
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

    db = dataBase()
    cafeInfos = []
    try:
        db.cursor.execute("select * from RecyCup.Cafe")
        rows = db.cursor.fetchall()
        
    except Exception as e:
        print("Error in 'getCafeInfo'", e); print("\n\n")

    else:
        for row in rows:
            cafeInfos.append({'cafeID' : row['cafeID'],
                              'location' : (row['latitude'], row['longitude'])})

    finally:
        db.dbDisconnect()

    return json.dumps(cafeInfos).encode('utf-8')

    