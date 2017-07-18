from flask import Flask, render_template, redirect, request
import spreadsheetdriveapi as drive

import DBDataReader as dbr
import dbDataWriter as dbw

import datetime as dt

import re

import dbconnect as db

from html5print import HTMLBeautifier

app = Flask(__name__)

dataSheet = None
data = None

FILELINK = ''

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
    return render_template('auth.html', message=msg)


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
    return render_template('auth.html', message=msg)


@app.route('/stats')
def get_stats_table():
    start = (request.args['start'])
    end = (request.args['end'])

    if (start == None) or (end == None):
        now = dt.datetime.now()
        start_date = '01/{:d}'.format(now.year)
        end_date = '12/{:d}'.format(now.year)
        request_str = 'stats?start=' + start_date + '&end=' + end_date

        return redirect(request_str)

    start_date_month, start_date_year = start.split('/')
    end_date_month, end_date_year = end.split('/')

    if (start_date_year > end_date_year) or \
            ((start_date_year == end_date_year) and (start_date_month > end_date_month)):
        return render_template('error.html', request_string=request_str), 400

    now = dt.datetime.now()
    if(start == None or end == None):
        start = '01/{:d}'.format(now.year)
        end = '12/{:d}'.format(now.year)

    years = list(range(2011, now.year + 1))
    dataDB, last_player_before_losers = dbr.get_stats(start, end)
    table_html = dataDB.to_html(classes='tablesorter" id="statistics')
    table_html = re.sub('dataframe ', '', table_html)

    if(re.match('[\d][\d]/[\d][\d][\d][\d]', start) != None and re.match('[\d][\d]/[\d][\d][\d][\d]', end) != None):
        return HTMLBeautifier.beautify(render_template('table.html', table=table_html, years=years, start=start, end=end,
                           last_player_before_losers=last_player_before_losers, source_file=FILELINK), 4)


@app.route("/stats", methods=['POST'])
def get_stats_table_for_selected_period():
    start_date = request.form['start']
    end_date = request.form['end']

    redirect_url = '?start=' + start_date + '&end=' + end_date
    return redirect("/stats" + redirect_url)


@app.route('/stats/')
def stats_slash_handler():
    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    request_str = 'stats?start=' + start_date + '&end=' + end_date

    return redirect(request_str)


@app.route("/playerstats")
def get_player_stats():
    player_id = (int)(request.args['id'])
    dataDB = dbr.getPlayerLastGames(player_id)
    player_name = dbr.getPlayerNameByID(player_id)
    playerachievments = dbr.getPlayerAchievements(player_id)
    table_html = dataDB.to_html(classes='playertable')
    table_html = re.sub('dataframe ', '', table_html)
    return render_template('playerstat.html', table=table_html, player_name=player_name, playerachievments= playerachievments, player_link='#')


@app.route("/howitcalc")
def how_it_calc_page():
    return render_template('howitcalc.html')


@app.errorhandler(500)
def page_not_found(e):
    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    request_str = 'stats?start=' + start_date + '&end=' + end_date

    return render_template('error.html', request_string=request_str), 500


@app.errorhandler(404)
def page_not_found(e):
    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    request_str = 'stats?start=' + start_date + '&end=' + end_date

    return render_template('error.html', request_string=request_str), 404


@app.errorhandler(410)
def page_not_found(e):
    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    request_str = 'stats?start=' + start_date + '&end=' + end_date

    return render_template('error.html', request_string=request_str), 410


@app.errorhandler(403)
def page_not_found(e):
    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    request_str = 'stats?start=' + start_date + '&end=' + end_date

    return render_template('error.html', request_string=request_str), 403


@app.route("/")
def index():
    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    request_str = 'stats?start=' + start_date + '&end=' + end_date

    return redirect(request_str)


if __name__ == '__main__':
    dataSheet, FILELINK = drive.downloadxlsx('Football-bigdata-v0.2')
    app.run(threaded=True)
    redirect("../")