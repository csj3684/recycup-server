from commons import *

app = Flask(__name__)

from app.main.server import server

app.register_blueprint(server, url_prefix = '/server')

