from common import *

app = Flask(__name__)

from app.main.mainPage import mainPage

print("__init__.py")

app.register_blueprint(mainPage, url_prefix = '/')
