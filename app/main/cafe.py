from app.main.dataBase import dateBase
from common import *

cafe = Blueprint('cafe', __name__)

@cafe.route('/CafeInfo/get', methods = ['GET', 'POST'])
def getCafeInfo():

    print("cafeInfo")

    db = dateBase()

    cafeInfos = []

    try:
        rows = db.cursor.execute("SELECT * FROM RecyCup.Cafe")
        db.connector.commit()
    except Exception as e:
        cafeInfos = None
        print(e)

    else:
        for row in rows:
            cafeInfos.append({'logoPath': row['logoPath'],
                              'cafeName': row['cafeName'],
                              'type': row['type']})
    finally:
        db.dbDisconnect()

    return json.dumps(cafeInfos).encode('utf-8')




