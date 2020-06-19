from commons import *
from app import app
from app.main.dataBase import dataBase


@app.route("/")
def mainPage():                           
    return "cafebene"

if __name__=='__main__':

    # 59.187.219.187:52406
    # csj3684.ddns.net:52406

    app.run(host='0.0.0.0', port=52406, debug=True)

