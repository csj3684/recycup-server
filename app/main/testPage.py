from application import app

@app.route('/')
def mainPage():
    return "mainPage"