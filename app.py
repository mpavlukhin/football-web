from flask import Flask, render_template, redirect, request
import spreadsheetdriveapi as drive

import DBDataReader as dbr
import dbDataWriterOOP as dbw

app = Flask(__name__)

dataSheet = None
data = None


@app.route("/stats")
def get_stats_for_current_year():
    dataDB = dbr.get_stats(None, None)
    return render_template('table.html', tables=[dataDB.to_html()])


@app.route('/stats', methods=['POST'])
def get_stats_for_selected_period():
    print('POST METHOD')
    start = request.form['start']
    end = request.form['end']

    dataDB = dbr.get_stats(start, end)
    return render_template('table.html', tables=[dataDB.to_html()], startdate=start, enddate=end)


@app.route("/update")
def get_spread_s():
    global data, dataSheet
    dataSheet = drive.downloadxlsx('football')
    data = dbw.updatePlayersStats('data/spreadsheets/football.xlsx')
    return redirect("/")

@app.route("/create")
def get_spread_s():
    global data, dataSheet
    dataSheet = drive.downloadxlsx('football')
    data = dbw.getAllPlayersStats('data/spreadsheets/football.xlsx')
    return redirect("/")


@app.route("/")
def index():
    return redirect("/stats")

if __name__ == '__main__':
    dataSheet = drive.downloadxlsx('football')
    app.run()
    redirect("../")