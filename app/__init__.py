from common import *

app = Flask(__name__)

from app.main.customer import mainPage
from app.main.kakaoPay import kakaoPay

print("__init__.py")

app.register_blueprint(mainPage, url_prefix = '/')
app.register_blueprint(kakaoPay)