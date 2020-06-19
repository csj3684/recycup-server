from common import *

app = Flask(__name__)

from app.main.cafe import cafe
from app.main.customer import customer
from app.main.kakaoPay import kakaoPay
from app.main.server import server
from app.main.kakaoLocation import kakaoLocation
from app.main.sharedInformation import sharedInformation

app.register_blueprint(cafe, url_prefix = '/cafe')
app.register_blueprint(customer, url_prefix = '/customer')
app.register_blueprint(kakaoPay)
app.register_blueprint(server, url_prefix = '/server')
app.register_blueprint(kakaoLocation, url_prefix = '/kakaoLocation')
app.register_blueprint(sharedInformation, url_prefix = '/sharedInformation')
