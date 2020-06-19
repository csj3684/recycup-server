import requests
from flask import Blueprint, request

APIHOST = 'https://kapi.kakao.com'
headers = {}
kakaoPay = Blueprint('kakaoPay', __name__, url_prefix='/kakaoPay')


def req(path, query, method, data):
    url = APIHOST + path

    if method == 'GET':
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, headers=headers, data=data)

@kakaoPay.route('/ready', methods=['GET', 'POST'])
def paymentReday():
    
    print('payment ready is called')

    path = '/v1/payment/ready'
    

    cid = request.form['cid']
    partner_order_id = request.form['partner_order_id']
    item_name = request.form['item_name']
    quantity = request.form['quantity']
    total_amount = request.form['total_amount']
    tax_free_amount = request.form['tax_free_amount']
    approval_url = request.form['approval_url']
    cancel_url = request.form['cancel_url']
    fail_url = request.form['fail_url']

    params = {
        "cid": {cid},
        "partner_order_id": {partner_order_id},
        "item_name": {item_name},
        "quantity": {quantity},
        "total_amount": {total_amount},
        "tax_free_amount": {tax_free_amount},
        "approval_url": {approval_url},
        "cancel_url": {cancel_url},
        "fail_url": {fail_url},
    }

    resp = req(path,'', 'POST', params)
    print("response status:\n%d" % resp.status_code)
    print("response headers:\n%s" % resp.headers)
    print("response body:\n%s" % resp.text)

@kakaoPay.route('/success', methods=['GET', 'POST'])
def paymentSuccess():

    print('sucesss')
    return '<h1>충전이 완료되었습니다.</h1>'