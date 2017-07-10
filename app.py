from flask import Flask, render_template, redirect, request
import spreadsheetdriveapi as drive

import DBDataReader as dbr
import dbDataWriter as dbw

import datetime as dt

app = Flask(__name__)

dataSheet = None
data = None


@app.route("/stats")
def get_stats_for_current_year():
    now = dt.datetime.now()
    years = list(range(2011, now.year + 1))


    dataDB, last_player_before_losers = dbr.get_stats(None, None)

    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    return render_template('table.html', table=dataDB.to_html(), years=years, start=start_date, end=end_date,
                           last_player_before_losers=last_player_before_losers)


@app.route('/stats', methods=['POST'])
def get_stats_for_selected_period():
    start = request.form['start']
    end = request.form['end']

    now = dt.datetime.now()
    years = list(range(2011, now.year + 1))

    dataDB, last_player_before_losers = dbr.get_stats(start, end)
    return render_template('table.html', table=dataDB.to_html(), years=years, start=start, end=end,
                           last_player_before_losers=last_player_before_losers)


@app.route("/update")
def get_spread_s():
    global data, dataSheet
    dataSheet = drive.downloadxlsx('Football-bigdata-v0.2')
    data = dbw.updatePlayersStats('data/spreadsheets/Football-bigdata-v0.2.xlsx')
    return redirect("/")


@app.route("/create")
def get_spread():
    global data, dataSheet
    dataSheet = drive.downloadxlsx('Football-bigdata-v0.2')
    data = dbw.getAllPlayersStats('data/spreadsheets/Football-bigdata-v0.2.xlsx')
    return redirect("/")


@app.route("/")
def index():
    return redirect("/stats")

if __name__ == '__main__':
    dataSheet = drive.downloadxlsx('Football-bigdata-v0.2')
    app.run(host='0.0.0.0', port=80)
    redirect("../")