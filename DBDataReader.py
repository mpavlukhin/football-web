import dbconnect as db
import pandas as pd
import datetime as dt
import calendar as cal
import numpy as np

def normalize_date_for_db(date, is_end_date=True):
    date_month, date_year = date.split('/')

    if(is_end_date):
        date_day = str(cal.monthrange(int(date_year), int(date_month))[1])
    else:
        date_day = '01'

    normalized_date = date_year + date_month + date_day

    return normalized_date


def get_stats(start_date, end_date):
    c, conn = db.connection()

    cmd_drop_view = 'DROP VIEW IF EXISTS MPSG'
    c.execute(cmd_drop_view)

    if start_date is None and end_date is None:
        now = dt.datetime.now()
        start_date = '01/{:d}'.format(now.year)
        end_date = '12/{:d}'.format(now.year)

    normalized_start_date_for_db = normalize_date_for_db(start_date, False)
    normalized_end_date_for_db = normalize_date_for_db(end_date)

    cmd_create_date_sort_view = 'CREATE VIEW MPSG AS SELECT PlayerID, Points, GameStatus, SoccerGameDate ' \
                                'FROM MappingPlayersSoccerGames MPSG ' \
                                'JOIN SoccerGames SG ON MPSG.SoccerGameID = SG.SoccerGameID ' \
                                'AND SG.SoccerGameDate >= \'{:s}\' ' \
                                'AND SG.SoccerGameDate <= \'{:s}\''.format(normalized_start_date_for_db, normalized_end_date_for_db)

    c.execute(cmd_create_date_sort_view)

    cmd_get_stats = 'SELECT PlayerName AS \'Name\', ' \
                    'IFNULL(WINS.Wins, 0) AS \'Wins\', ' \
                    'IFNULL(DRAWS.Draws, 0) AS \'Draws\', ' \
                    'IFNULL(LOSES.Loses, 0) AS \'Loses\', ' \
                    'COUNT(GameStatus) AS \'Total Games\', ' \
                    'CONCAT(CAST(AVG(GameStatus = \'W\') * 100 AS DECIMAL(5, 2)), \'%\') AS \'Victory Rate\', ' \
                    'CAST((SUM(Points) / (COUNT(Points) * 3)) * 100 AS DECIMAL(5, 2)) ' \
                    'AS \'Score Rate\' ' \
                    'FROM MPSG ' \
                    'JOIN Players P ' \
                    'ON MPSG.PlayerID = P.PlayerID ' \
                    'LEFT JOIN (SELECT PlayerID, COUNT(GameStatus) AS Wins FROM MPSG WHERE GameStatus = \'W\' ' \
                    'GROUP BY PlayerID) WINS ' \
                    'ON MPSG.PlayerID = WINS.PlayerID ' \
                    'LEFT JOIN (SELECT PlayerID, COUNT(GameStatus) AS Draws FROM MPSG WHERE GameStatus = \'D\' ' \
                    'GROUP BY PlayerID) DRAWS ' \
                    'ON MPSG.PlayerID = DRAWS.PlayerID ' \
                    'LEFT JOIN (SELECT PlayerID, COUNT(GameStatus) AS Loses FROM MPSG WHERE GameStatus = \'L\' ' \
                    'GROUP BY PlayerID) LOSES ' \
                    'ON MPSG.PlayerID = LOSES.PlayerID ' \
                    'GROUP BY MPSG.PlayerID'

    c.execute(cmd_get_stats)
    columns_names = [i[0] for i in c.description]
    players_stats = c.fetchall()
    players_stats = list(players_stats)
    players_stats_lists = [[]]
    players_with_less_ten_games = [[]]
    for player in players_stats:
        if (int)(player[4]) >= 10:
            players_stats_lists.append(player)
        else:
            players_with_less_ten_games.append(player)
    players_stats_lists.pop(0)
    players_with_less_ten_games.pop(0)
    players_stats_lists.sort(key=lambda tup:tup[6], reverse=True)
    last_player_before_losers = len(players_stats_lists) - 1
    players_with_less_ten_games.sort(key=lambda tup: tup[6], reverse=True)

    maxlen = len(players_stats_lists)
    index = maxlen
    for player in players_with_less_ten_games:
        players_stats_lists.append(player)

    index = 0

    for player in players_stats_lists:
        tempstr = (list)(player)
        tempstr[6] = (str)(player[6]) + '%'
        players_stats_lists.remove(player)
        players_stats_lists.insert(index, tempstr)
        index += 1

    dataframe = pd.DataFrame(players_stats_lists, columns=columns_names)
    dataframe.index = np.arange(1, len(dataframe) + 1)
    return dataframe, last_player_before_losers