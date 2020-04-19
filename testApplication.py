from flask import Flask


if __name__=='__main__':
 app = Flask(__name__)
 app.run(host='localhost', port=8888, debug=True)


 @app.route('/')
 def mainPage():
     return "mainPage"