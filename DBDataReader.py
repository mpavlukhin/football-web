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

    cmd_get_stats = 'SELECT MPSG.PlayerID, PlayerName AS \'Имя\', ' \
                    'IFNULL(WINS.Wins, 0) AS \'Победы\', ' \
                    'IFNULL(DRAWS.Draws, 0) AS \'Ничьи\', ' \
                    'IFNULL(LOSES.Loses, 0) AS \'Поражения\', ' \
                    'COUNT(GameStatus) AS \'Всего игр\', ' \
                    'CONCAT(CAST(AVG(GameStatus = \'W\') * 100 AS DECIMAL(5, 2)), \'%\') AS \'Коэф. побед\', ' \
                    'CAST((SUM(Points) / (COUNT(Points) * 3)) * 100 AS DECIMAL(5, 2)) ' \
                    'AS \'Коэф. очков\' ' \
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
    columns_names.append('Форма')
    columns_names.append('Рейтинг')
    del columns_names[0]
    players_stats = c.fetchall()
    players_stats = list(list(player_stats) for player_stats in players_stats)

    for player_stats in players_stats:
        player_stats.append(getPlayerFormfForLastTwoYears(int(player_stats[0])))
        player_stats.append(getPlayerCoefForCurrentYear(int(player_stats[0])))
        del player_stats[0]

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


def getPlayerLastGames(player_id):
    c, conn = db.connection()
    c.execute("CREATE OR REPLACE VIEW PlayerStats AS "
                "SELECT SG.SoccerGameDate AS 'Дата', MPSG.Points AS 'Очки', MPSG.GameStatus AS 'Результат' from mappingplayerssoccergames MPSG "
                "JOIN soccergames SG WHERE SG.SoccerGameID = MPSG.SoccerGameID AND PlayerID = {0} "
                "ORDER BY SG.SoccerGameDate DESC;".format(player_id))
    c.execute("SELECT * FROM PlayerStats "
                "LIMIT 10;")
    playerstat = c.fetchall()
    c.close()
    columns_names = [i[0] for i in c.description]
    conn.autocommit('Get Player Info')
    dataframe = pd.DataFrame(list(playerstat), columns=columns_names)
    dataframe.index = np.arange(1, len(dataframe) + 1)
    return dataframe


def getPlayerNameByID(player_id):
    c, conn = db.connection()
    c.execute("SELECT PlayerName From Players WHERE PlayerID = {0}".format(player_id))
    player_name = c.fetchall()
    player_name = player_name[0][0]
    return  player_name


def getPlayerFormfForLastTwoYears(player_id):
    c, conn = db.connection()
    c.execute("CREATE OR REPLACE VIEW PlayerStatsForTwoYears AS "
                "SELECT SG.SoccerGameDate AS 'Дата игры', MPSG.Points AS 'Очки' from mappingplayerssoccergames MPSG " 
                "JOIN soccergames SG Where SG.SoccerGameId = MPSG.SoccerGameID AND PlayerID = {0} AND YEAR(SG.SoccerGameDate) >= YEAR(CURDATE() - INTERVAL 1 YEAR) "
                "ORDER BY SG.SoccerGameDate DESC;".format(player_id))
    c.execute("SELECT COUNT(*) FROM  PlayerStatsForTwoYears; ")
    playercountgames = c.fetchone()
    if(playercountgames[0] >= 20):
        c.execute("SELECT * FROM PlayerStatsForTwoYears "
                  "LIMIT 20; ")
        playergames = c.fetchall()
        totalscore = 0
        totalpoints = 3 * 20
        for game in playergames:
            totalscore += game[1]
        return round(totalscore / totalpoints * 100, 2)
    return 0


def getPlayerCoefForCurrentYear(player_id):
    # Статистика расчитывается только за текущий год (!)
    c, conn = db.connection()
    c.execute("CREATE OR REPLACE VIEW PlayerStatsForTwoYears AS "
                "SELECT SG.SoccerGameDate AS 'Дата игры', MPSG.Points AS 'Очки' from mappingplayerssoccergames MPSG "
                "JOIN soccergames SG Where SG.SoccerGameId = MPSG.SoccerGameID AND PlayerID = {0} AND YEAR(SG.SoccerGameDate) >= YEAR(CURDATE()) "
                "ORDER BY SG.SoccerGameDate DESC; ".format(player_id))
    c.execute("SELECT * FROM PlayerStatsForTwoYears; ")
    playergames = c.fetchall()
    lastmonth = dt.datetime.now().month
    coef = 1 / lastmonth
    totalscore = 0
    for game in playergames:
        totalscore = totalscore + (int(game[0].month) * coef * game[1])
    totalscore = round(totalscore, 2)
    return totalscore