from flask import Flask, render_template, redirect, request
import spreadsheetdriveapi as drive
import DBDataReader as dbr
import dbDataWriter as dbw
import urllib.request
import datetime as dt
import re
import dbconnect as db
import requests
import os
import filecmp
import spreadsheet as ss
from html5print import HTMLBeautifier
from werkzeug.contrib.fixers import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

sched = BackgroundScheduler()
sched.start()

dataSheet = None
data = None

GAUTH = None
FILELINK = 'https://docs.google.com/spreadsheets/d/1QH-AFYHk3lXJf-dG3FzhDwtO6iJZus7ZXWoY8aBs7ZI/edit?usp=sharing'


def get_default_request_string():
    now = dt.datetime.now()
    start_date = '01/{:d}'.format(now.year)
    end_date = '12/{:d}'.format(now.year)
    request_str = 'stats?start=' + start_date + '&end=' + end_date

    return request_str

def admin_form_requester():
    login = request.form['login']
    password = request.form['password']

    return login, password


def admin_form_checker(login, password):
    user_lists = db.getWebServiceUsers()

    for user in user_lists:
        if login == user[0] and password == user[1]:
            return True

        else:
            msg = 'Что-то введено не так...'
            return render_template('auth.html', message=msg)


@app.route("/update")
def login_in_update():
    return render_template('auth.html')


@app.route("/update", methods=['POST'])
def get_login_info_update():
    global data, dataSheet, GAUTH

    login, password = admin_form_requester()
    ss.download_sheet()

    if admin_form_checker(login, password):
        data = dbw.updatePlayersStats('data/spreadsheets/Football-bigdata-v0.2.xlsx')
        return redirect("/stats")


@app.route("/create")
def login_in_create():
    return render_template('auth.html')


@app.route("/create", methods=['POST'])
def get_login_info():
    global data, dataSheet, GAUTH

    login, password = admin_form_requester()
    ss.download_sheet()

    if admin_form_checker(login, password):
        data = dbw.getAllPlayersStats('data/spreadsheets/Football-bigdata-v0.2.xlsx')
        return redirect("/stats")


@app.route('/stats')
def get_stats_table():
    global FILELINK

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
    actual_date = dbr.get_actual_date_from_database()

    now = dt.datetime.now()
    years = list(range(2011, now.year + 1))
    dataDB, last_player_before_losers = dbr.get_stats(start, end)
    table_html = dataDB.to_html(classes='tablesorter" id="statistics')
    table_html = re.sub('dataframe ', '', table_html)

    if (re.match('[\d][\d]/[\d][\d][\d][\d]', start) is not None) \
            and (re.match('[\d][\d]/[\d][\d][\d][\d]', end) is not None):
        return HTMLBeautifier.beautify(render_template('table.html', table=table_html, years=years, start=start,
                                                       end=end, last_player_before_losers=last_player_before_losers,
                                                       actual_date=actual_date, source_file=FILELINK), 4)


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
    return render_template('playerstat.html', table=table_html, player_name=player_name,
                           playerachievments= player_achievments)


@app.route("/howitcalc")
def how_it_calc_page():
    return render_template('howitcalc.html')


@app.route("/refresh")
def refresh_heroku_dynos():
    return "Heroku Anti Sleep page, yeah!"


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


@app.before_first_request
def check_db_existence():
    if not db.db_existence_checker('yksc2nhvbiqhmiow'):
        db.create_db()


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

    
@sched.scheduled_job('interval', minutes=20)
def web_proc_anti_sleep_handler_and_update():
    r = requests.get('https://football-web.herokuapp.com/refresh', timeout=20)

    file_old = 'data/spreadsheets/Football-bigdata-v0.2-old.xlsx'
    file_new = 'data/spreadsheets/Football-bigdata-v0.2.xlsx'

    os.rename(file_new, file_old)
    ss.download_sheet(file_name=file_new)

    if not filecmp.cmp(file_old, file_new):
        dbw.updatePlayersStats(file_new)
        print('Statistics was updated')

    else:
        print('Nothing to update')

    os.remove(file_old)

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run()
