from flask import Flask
import spreadsheet
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.debug = True
    app.run()