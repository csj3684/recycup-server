from commons import *
from app import app
from app.main.dataBase import dataBase


@app.route("/")
def mainPage():                           
    return "tom and toms"

if __name__=='__main__':

    # 59.187.219.187:62406
    # csj3684.ddns.net:62406

    app.run(host='0.0.0.0', port=62406, debug=True)

