from flask import Flask, render_template
import spreadsheet as ss
import spreadsheetdriveapi as drive
import DataHandler as dh

# import pandas as pd

app = Flask(__name__)

dataSheet = None


@app.route("/")
def hello():
    data = dh.getdataframefromfile(dataSheet)
    # data = pd.read_excel(filepath)
    return render_template('tables.html', tables=[data.to_html()], titles=[])


@app.route("/test")
def spreadsheet():
    return ss.getStatsArray()

if __name__ == '__main__':
    dataSheet = drive.downloadxlsx()
    app.run()