from flask import Flask

if __name__=='__main__':
 app = Flask(__name__)
 app.run(host='0.0.0.0', port=8888, debug=True)