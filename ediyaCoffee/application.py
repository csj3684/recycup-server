from commons import *
from app import app
from app.main.dataBase import dataBase


@app.route("/")
def mainPage():                           
    return "ediya coffee"

if __name__=='__main__':

    # 59.187.219.187:42406
    # csj3684.ddns.net:42406

    app.run(host='0.0.0.0', port=42406, debug=True)

