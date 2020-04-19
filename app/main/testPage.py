from application import app

@app.route('/', method = ['GET', 'POST'])
def mainPage():
    return "mainPage"