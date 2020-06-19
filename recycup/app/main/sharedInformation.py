from app.main.dataBase import dataBase
from common import *

sharedInformation = Blueprint('sharedInformation', __name__)

@sharedInformation.route('/', methods = ['GET', 'POST'])
def main():
    db = dataBase()

    headNames = []

    sql = 'select headName from recycup.head'
    db.cursor.execute(sql)

    rows = db.cursor.fetchall()
    for row in rows:
        headNames.append(row['headName'])
    return render_template('/sharedInformation/main.html', headNames = json.dumps(headNames, default = json_default))


@sharedInformation.route('/login', methods = ['GET', 'POST'])
def login():
    db = dataBase()
    headName = request.form['headName']
    
    # headName 이 유효한지 검사
    sql = 'select headName from recycup.head where headName = %s'
    db.cursor.execute(sql, (headName))

    if db.cursor.fetchone() == None:
        return render_template('/sharedInformation/main.html')
    
    lst = []
    frame = pd.DataFrame(columns = ['date', 'phoneNumber', 'amount', 'status'])

    sql = 'select * from recycup.sales where headName = %s'
    db.cursor.execute(sql, (headName))
    rows = db.cursor.fetchall()
    for row in rows:
        frame.loc[len(frame)] = {'date' : row['date'],
                                 'phoneNumber' : row['phoneNumber'],
                                 'amount' : row['amount'],
                                 'status' : 'sales'}
        

    sql = 'select * from recycup.recycle where headName = %s'
    db.cursor.execute(sql, (headName))
    rows = db.cursor.fetchall()
    for row in rows:
        frame.loc[len(frame)] = {'date' : row['date'],
                                 'phoneNumber' : row['phoneNumber'],
                                 'amount' : row['amount'],
                                 'status' : 'recycle'}
    
    frame.sort_values(by = "date", ascending = False, inplace = True)
    for i in frame.index:
        lst.append({'date' : frame.loc[i, 'date'],
                    'phoneNumber' : frame.loc[i, 'phoneNumber'],
                    'amount' : frame.loc[i, 'amount'],
                    'status' : frame.loc[i, 'status']})
    
    return render_template('/sharedInformation/information.html', headName = headName, lst = json.dumps(lst, default = json_default))

def json_default(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))



@sharedInformation.route('/test', methods = ['GET', 'POST   '])
def test():
    return render_template('/sharedInformation/test.html')