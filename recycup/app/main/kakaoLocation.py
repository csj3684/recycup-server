
from common import *
import os

kakaoLocation = Blueprint('kakaoLocation', __name__)

@kakaoLocation.route('/', methods = ['GET', 'POST'])
def searchLocation():

    return render_template('kakaoLocation.html')