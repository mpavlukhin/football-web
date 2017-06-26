from flask import Flask, render_template, redirect
import spreadsheet as ss
import spreadsheetdriveapi as drive
import DataHandler as dh

from nocache import nocache

# import pandas as pd

app = Flask(__name__)

dataSheet = None
data = None


@app.route("/testdb")
def testdatabase():
    dataDB = dh.testdb()
    # return str(data)
    return render_template('table.html', tables=[dataDB.to_html()], titles=[])

@app.route("/update")
def gettables():
    global data, dataSheet
    data = dh.getdataframefromfile(dataSheet)
    # data = pd.read_excel(filepath)
    # return render_template('table.html', tables=[data.to_html()], titles=[])
    return redirect("../")


@app.route("/table")
def viewstats():
    global data
    # data = dh.getdataframefromfile(dataSheet)
    # data = pd.read_excel(filepath)
    return render_template('table.html', tables=[data.to_html()], titles=[])


@app.route("/test")
def spreadsheet():
    return ss.getStatsArray()


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    dataSheet = drive.downloadxlsx('football')
    app.run()
    redirect("../")