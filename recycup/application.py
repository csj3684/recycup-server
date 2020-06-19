from common import *
from app import app
from app.main.dataBase import dataBase
from app.main.server import update


"""

<customer>
1. 중복검사 : csj3684.ddns.net:22406/customer/duplicateCheck
2. 회원가입 : csj3684.ddns.net:22406/customer/signUp
3. 로그인 : csj3684.ddns.net:22406/customer/signIn
4. 회원정보 : csj3684.ddns.net:22406/customer/customerInfo/get
5. 회원정보 수정 : csj3684.ddns.net:22406/customer/customerInfo/edit
6. 포인트 충전 : csj3684.ddns.net:22406/customer/charge

<cafe>
1. 중복검사 : csj3684.ddns.net:22406/cafe/duplicateCheck
2. 회원가입 : csj3684.ddns.net:22406/cafe/cafeInfo/register
3. 로그인 : csj3684.ddns.net:22406/cafe/cafeInfo/signIn
3. 본사정보 : csj3684.ddns.net:22406/cafe/headInfo/get
4. 카페정보 : csj3684.ddns.net:22406/cafe/cafeInfo/get
5. 카페정보 수정 : csj3684.ddns.net:22406/cafe/cafeInfo/edit

<server>
1. 판매 : csj3684.ddns.net:22406/server/sales
2. 회수 : csj3684.ddns.net:22406/server/recycle
3. 업데이트 : csj3684.ddns.net:22406/server/update

"""

@app.route("/")
def mainPage():                           
    return "recycup"

if __name__=='__main__':

    # 59.187.219.187:22406
    # csj3684.ddns.net:22406

    # starbucks : 32406
    # ediyaCoffee : 42406
    # cafeBene : 52406
    # tomAndToms : 62406

    threading.Thread(target = update, daemon = True).start()
    app.run(host='0.0.0.0', port=22406, debug=True)
    


