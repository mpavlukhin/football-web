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

FILELINK = 'https://docs.google.com/spreadsheets/d/1QH-AFYHk3lXJf-dG3FzhDwtO6iJZus7ZXWoY8aBs7ZI/edit#gid=1350957595'
GAUTH = None


def get_default_request_string():
    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    request_str = 'stats?start=' + start_date + '&end=' + end_date

    return request_str


def google_authentication_init():
    global GAUTH
    GAUTH = drive.google_auth_init()


def admin_form_requester():
    login = request.form['login']
    password = request.form['password']
    code = request.form['code']

    return login, password, code


def admin_form_checker(login, password, code):
    user_lists = db.getWebServiceUsers()

    for user in user_lists:
        if login == user[0] and password == user[1]:
            return True

        else:
            msg = 'Что-то введено не так...'
            return render_template('auth.html', message=msg)


@app.route("/update")
def login_in_update():
    google_authentication_init()
    google_authentication_redirect = GAUTH.GetAuthUrl()
    return render_template('auth.html', google_auth_link=google_authentication_redirect)


@app.route("/update", methods=['POST'])
def get_login_info_update():
    global data, dataSheet, GAUTH

    login, password, code = admin_form_requester()
    drive.oauth_authenticate(GAUTH, code)

    if admin_form_checker(login, password, code):
        dataSheet = drive.downloadxlsx('Football-bigdata-v0.2', GAUTH)
        data = dbw.updatePlayersStats('data/spreadsheets/Football-bigdata-v0.2.xlsx')
        return redirect("/stats")


@app.route("/create")
def login_in_create():
    google_authentication_init()
    google_authentication_redirect = GAUTH.GetAuthUrl()
    return render_template('auth.html', google_auth_link=google_authentication_redirect)


@app.route("/create", methods=['POST'])
def get_login_info():
    global data, dataSheet, GAUTH

    login, password, code = admin_form_requester()
    drive.oauth_authenticate(GAUTH, code)

    if admin_form_checker(login, password, code):
        dataSheet = drive.downloadxlsx('Football-bigdata-v0.2', GAUTH)
        data = dbw.getAllPlayersStats('data/spreadsheets/Football-bigdata-v0.2.xlsx')
        return redirect("/stats")


@app.route('/stats')
def get_stats_table():
    try:
        start = (request.args['start'])
        end = (request.args['end'])

    except:
        request_str = get_default_request_string()
        return redirect(request_str)

    start_date_month, start_date_year = start.split('/')
    end_date_month, end_date_year = end.split('/')

    if (start_date_year > end_date_year) or \
            ((start_date_year == end_date_year) and (start_date_month > end_date_month)):
        request_str = get_default_request_string()
        return render_template('error.html', request_string=request_str), 400

    now = dt.datetime.now()
    years = list(range(2011, now.year + 1))
    dataDB, last_player_before_losers = dbr.get_stats(start, end)
    table_html = dataDB.to_html(classes='tablesorter" id="statistics')
    table_html = re.sub('dataframe ', '', table_html)

    if (re.match('[\d][\d]/[\d][\d][\d][\d]', start) is not None) \
            and (re.match('[\d][\d]/[\d][\d][\d][\d]', end) is not None):
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
    request_str = get_default_request_string()
    return redirect(request_str)


@app.route("/playerstats")
def get_player_stats():
    player_name = request.args['name']

    player_id = dbr.get_player_id_by_name(player_name)

    if player_id is None:
        request_str = get_default_request_string()
        return render_template('error.html', request_string=request_str), 400

    dataDB = dbr.getPlayerLastGames(player_id)
    player_achievments = dbr.getPlayerAchievements(player_id)
    table_html = dataDB.to_html(classes='playertable')
    table_html = re.sub('dataframe ', '', table_html)
    return render_template('playerstat.html', table=table_html, player_name=player_name, playerachievments= player_achievments)


@app.route("/howitcalc")
def how_it_calc_page():
    return render_template('howitcalc.html')


@app.errorhandler(500)
def page_not_found(e):
    request_str = get_default_request_string()
    return render_template('error.html', request_string=request_str), 500


@app.errorhandler(404)
def page_not_found(e):
    request_str = get_default_request_string()
    return render_template('error.html', request_string=request_str), 404


@app.errorhandler(410)
def page_not_found(e):
    request_str = get_default_request_string()
    return render_template('error.html', request_string=request_str), 410


@app.errorhandler(403)
def page_not_found(e):
    request_str = get_default_request_string()
    return render_template('error.html', request_string=request_str), 403


@app.route("/")
def index():
    request_str = get_default_request_string()
    return redirect(request_str)


if __name__ == '__main__':
    db.create_db()
    app.run()