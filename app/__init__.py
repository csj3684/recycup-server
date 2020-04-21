from common import *

app = Flask(__name__)

from app.main.mainPage import mainPage

app.register_blueprint(mainPage, url_prefix = '/')