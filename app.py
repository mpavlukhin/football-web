from flask import Flask, render_template, redirect, request
import spreadsheetdriveapi as drive

import DBDataReader as dbr
import dbDataWriter as dbw

import datetime as dt

import re

import dbconnect as db

app = Flask(__name__)

dataSheet = None
data = None

FILELINK = ''
@app.route("/stats")
def get_stats_for_current_year():
    now = dt.datetime.now()
    years = list(range(2011, now.year + 1))


    dataDB, last_player_before_losers = dbr.get_stats(None, None)

    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)

    table_html = dataDB.to_html(classes='tablesorter" id="statistics')
    table_html = re.sub('dataframe ', '', table_html)

    return render_template('table.html', table=table_html, years=years, start=start_date, end=end_date,
                           last_player_before_losers=last_player_before_losers, source_file=FILELINK)


@app.route('/stats', methods=['POST'])
def get_stats_for_selected_period():
    start = request.form['start']
    end = request.form['end']

    now = dt.datetime.now()
    years = list(range(2011, now.year + 1))

    dataDB, last_player_before_losers = dbr.get_stats(start, end)

    table_html = dataDB.to_html(classes='tablesorter" id="statistics')
    table_html = re.sub('dataframe ', '', table_html)
    return render_template('table.html', table=table_html, years=years, start=start, end=end,
                           last_player_before_losers=last_player_before_losers, source_file=FILELINK)


@app.route("/update")
def get_spread_s():
    return render_template('auth.html')


@app.route("/update", methods=['POST'])
def get_login_info_update():
    global data, dataSheet
    login = request.form['login']
    password = request.form['password']
    userlists = db.getWebServiceUsers()
    for user in userlists:
        if login == user[0] and password == user[1]:
            dataSheet = drive.downloadxlsx('Football-bigdata-v0.2')
            data = dbw.updatePlayersStats('data/spreadsheets/Football-bigdata-v0.2.xlsx')
            return redirect("/stats")
    msg = 'Wrong login or password'
    return  render_template('auth.html', message=msg)


@app.route("/create")
def login_in():
    return render_template('auth.html')


@app.route("/create", methods=['POST'])
def get_login_info():
    global data, dataSheet
    login = request.form['login']
    password = request.form['password']
    userlists = db.getWebServiceUsers()
    for user in userlists:
        if login == user[0] and password == user[1]:
            dataSheet = drive.downloadxlsx('Football-bigdata-v0.2')
            data = dbw.getAllPlayersStats('data/spreadsheets/Football-bigdata-v0.2.xlsx')
            return redirect("/stats")
    msg = 'Wrong login or password'
    return  render_template('auth.html', message=msg)


@app.route("/")
def index():
    return redirect("/stats")

if __name__ == '__main__':
    dataSheet, FILELINK = drive.downloadxlsx('Football-bigdata-v0.2')
    app.run(host='0.0.0.0', port=5000, threaded=True)
    redirect("../")