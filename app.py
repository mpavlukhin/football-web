from flask import Flask, render_template, redirect, request
import spreadsheetdriveapi as drive

import DBDataReader as dbr
import dbDataWriterOOP as dbw

import datetime as dt

app = Flask(__name__)

dataSheet = None
data = None


@app.route("/stats")
def get_stats_for_current_year():
    now = dt.datetime.now()
    years = list(range(2011, now.year + 1))

    dataDB = dbr.get_stats(None, None)
    return render_template('table.html', table=dataDB.to_html(), years=years)


@app.route('/stats', methods=['POST'])
def get_stats_for_selected_period():
    start = request.form['start']
    end = request.form['end']

    now = dt.datetime.now()
    years = list(range(2011, now.year + 1))

    dataDB = dbr.get_stats(start, end)
    return render_template('table.html', table=dataDB.to_html(), years=years)


@app.route("/update")
def get_spread_s():
    global data, dataSheet
    dataSheet = drive.downloadxlsx('football')
    data = dbw.updatePlayersStats('data/spreadsheets/football.xlsx')
    return redirect("/")


@app.route("/create")
def get_spread():
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