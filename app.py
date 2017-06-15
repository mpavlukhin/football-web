from flask import Flask
import spreadsheet as ss

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/test")
def spreadsheet():
    return ss.getStatsArray()

if __name__ == '__main__':
    app.debug = True
    app.run()