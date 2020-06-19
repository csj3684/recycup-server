from commons import *
from app import app
from app.main.dataBase import dataBase


@app.route("/")
def mainPage():                           
    return "starbucks"

if __name__=='__main__':

    # 59.187.219.187:32406
    # csj3684.ddns.net:32406

    app.run(host='0.0.0.0', port=32406, debug=True)

