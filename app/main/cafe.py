from app.main.dataBase import dateBase
from common import *

cafe = Blueprint('cafe', __name__)

@cafe.route('/cafeInfo', methods = ['GET', 'POST'])
def getCafeInfo():

    print("cafeInfo")

    db = dateBase()

    cafeInfos = []

    try:
        db.cursor.execute("SELECT * FROM RecyCup.Cafe")
        rows = db.cursor.fetchall()
        db.connector.commit()
    except Exception as e:
        cafeInfos = None
        print("Error in 'getCafeInfo'", e)

    else:
        for row in rows:
            cafeInfos.append({'logoPath': row['logoPath'],
                              'cafeName': row['name'],
                              'type': row['type']})
    finally:
        db.dbDisconnect()

    return json.dumps(cafeInfos).encode('utf-8')




