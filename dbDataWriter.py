import pandas as pd
import openpyxl as pyxl
import numpy as np
from datetime import datetime, date, time
import dbconnect as db
import MySQLdb.connections

BLUECOLOR = 'FF0000FF'
REDCOLOR = 'FFFF0000'
WHITECOLOR = '00000000'  # or 'FFFFFFFF'
WHITECOLOR2 = 'FFFFFFFF'
YELLOWCOLOR = 'FFFFFF00'
GREENCOLOR = 'FF6AA84F'  # Draw color
GREENCOLOR2 = 'FF38761D'
GREENCOLOR3 = 'FF274E13'
PURPLECOLOR = 'FF9900FF'

GLOBAL_DATES_LIST = []
GLOBAL_PLAYERS_LIST = []

GLOBAL_PLAYER_INDEX = 1
GLOBAL_DATE_INDEX = 1


class ParserMain:
    cursor, connection = db.connection()

    def __init__(self, file_path):
        self.file = file_path
        self.wb = pyxl.load_workbook(file_path, data_only=True)

    @staticmethod
    def get_data_from_sheet(sheet):
        sheet_title_data = sheet.title
        title_year = int(sheet_title_data[-2:])
        title_month = str(sheet_title_data.replace(' ', '')[:-2])
        return title_year, title_month

    def get_player_list(self, lastpage):
        players_list = []
        column = 'B'
        for sheet in self.wb:
            if len(sheet.title) <= 4:
                title_year, title_month = self.get_data_from_sheet(sheet)
                if title_year >= 14:
                    column = 'A'
                else:
                    column = 'B'
                for cell in sheet[column]:
                    if cell.value is None or cell.value == '' or\
                            (cell.value == 'Сумма' and cell.row > 5 or
                             (cell.value == 'счет' and cell.row > 5)):
                        break
                    if cell.value != 'Имя' and cell.value != 'счет' and cell.value != 'Сумма' and\
                            cell.value != 'Аренда' and cell.value != 'Guests ' and cell.value != ''\
                            and cell.value != 'дата':
                        player_name = cell.value
                        if GLOBAL_PLAYERS_LIST.count(player_name) == 0:
                            GLOBAL_PLAYERS_LIST.append(player_name)
                            players_list.append(cell)
                            self.cursor.execute("INSERT IGNORE Players(PlayerName) VALUES('{0}')".format(cell.value))
                            self.connection.autocommit("Inserting to Players")
            if lastpage:
                break
        return players_list

    def get_all_games_dates(self):
        date_list = []
        for sheet in self.wb:
            if len(sheet.title) <= 4:
                title_year, title_month = self.get_data_from_sheet(sheet)
                if title_year >= 14 or (title_year >= 13 and title_month > 3):
                    for cell in sheet[1]:
                        if cell.value == 'Оплата':
                            break
                        if type(cell.value) is datetime and\
                            sheet[str(cell.column) + str(cell.row + 1)].value is not None and\
                                sheet[str(cell.column) + str(cell.row + 1)].value != 'нэбыло':
                            date_list.append(cell)
                            GLOBAL_DATES_LIST.append(cell.value)
                            self.cursor.execute("INSERT IGNORE INTO SoccerGames "
                                                "(SoccerGameDate) VALUES('{0}')".format(cell.value))
                            self.connection.autocommit("Add dates to SoccerGameDate")
                else:
                    for cell in sheet['B']:
                        if cell.value == "дата":
                            start_cell = cell
                            break
                    for cell in sheet[start_cell.row]:
                        if cell.value == 'Оплата':
                            break
                        if type(cell.value) is datetime and\
                                sheet[str(cell.column) + str(cell.row - 1)].value is not None:
                            date_list.append(cell)
                            GLOBAL_DATES_LIST.append(cell.value)
                            self.cursor.execute("INSERT IGNORE INTO SoccerGames "
                                           "(SoccerGameDate) VALUES('{0}')".format(cell.value))
                            self.connection.autocommit("Add dates to SoccerGameDate")
        return date_list

    def get_players_from_sheet(self, sheet):
        players_range = []
        title_year, title_month = self.get_data_from_sheet(sheet)
        if title_year >= 14:
            column = 'A'
        else:
            column = 'B'
        for cell in sheet[column]:
            if cell.value is None or cell.value == '' or\
                (cell.value == 'Сумма' and cell.row > 5) or\
                    (cell.value == 'счет' and cell.row > 5):
                break
            if cell.value != 'Имя' and cell.value != 'счет' and\
                cell.value != 'Сумма' and cell.value != 'Аренда' and\
                    cell.value != 'Guests ' and cell.value != 'дата' and cell.value != 'счет':
                players_range.append(cell)
        return players_range

    def get_player_stats(self, sheet, date_list, players_list, games_score):
        player_result = 'L'
        player_score = 0
        type_of_game = ''
        output = [[]]
        index = 0
        for player_cell in players_list:
            for date_cell in date_list:
                current_cell = sheet[str(date_cell.column) + (str)(player_cell.row)]
                current_cell_color = current_cell.fill.start_color.index
                if current_cell_color == WHITECOLOR or current_cell_color == WHITECOLOR2:
                    index += 1
                    continue
                type_of_game = games_score[index]
                current_score = (str)(type_of_game[0])
                game_color = type_of_game[1]
                current_score = current_score.split('-')
                # This cases for games with 2 teams
                if len(current_score) == 2:
                    team1_score = float(current_score[0])
                    team2_score = float(current_score[1])
                    if team1_score == team2_score:
                        player_result = 'D'
                        player_score = 1
                    elif current_cell_color == game_color:
                        player_result = 'W'
                        player_score = 3
                    else:
                        player_result = 'L'
                        player_score = 0
                # This cases for games with 3 teams
                elif len(current_score) == 3:
                    team1_score = float(current_score[0])
                    team2_score = float(current_score[1])
                    team3_score = float(current_score[2])
                    # 1 Case   # For example Game W - D - L (3 - 1 - 0)
                    if team1_score > team2_score > team3_score and\
                            team1_score is not team2_score:
                        if current_cell_color == REDCOLOR:
                            player_score = 3
                            player_result = 'W'
                        elif current_cell_color == GREENCOLOR or\
                            current_cell_color == GREENCOLOR2 or\
                                current_cell_color == GREENCOLOR3:
                            player_score = 1
                            player_result = 'D'
                        if current_cell_color == BLUECOLOR:
                            player_score = 0
                            player_result = 'L'
                    # 2 Case   # For example Game D - D - L (1 - 1 - 0)
                    elif team1_score == team2_score and team2_score > team3_score:
                        if current_cell_color == GREENCOLOR or current_cell_color == REDCOLOR:
                            player_score = 2
                            player_result = 'D'
                        else:
                            player_score = 0
                            player_result = 'L'
                    # 3 Case   # For example Game W - D - D (3 - 1 - 1)
                    elif team1_score > team2_score == team3_score:
                        if current_cell_color == REDCOLOR:
                            player_score = 3
                            player_result = 'W'
                        else:
                            player_score = 1
                            player_result = 'D'
                    # 4 Case   # For example Game D - D - D (1 - 1 - 1)
                    elif team1_score == team2_score and team2_score == team3_score:
                        player_score = 1
                        player_result = 'D'
                self.cursor.execute("SELECT PlayerID FROM Players WHERE PlayerName = '{0}';".format(player_cell.value))
                player_id = self.cursor.fetchone()
                self.cursor.execute("SELECT SoccerGameID from SoccerGames "
                                    "WHERE SoccerGameDate = '{0}';".format(date_cell.value))
                game_date_id = self.cursor.fetchone()
                self.cursor.execute("INSERT IGNORE INTO MappingPlayersSoccerGames "
                                    "VALUES ( {0}, {1}, {2}, '{3}')".format(
                                        player_id[0], game_date_id[0], player_score, player_result))
                self.connection.autocommit("Inserting to MappingPlayers")
                index += 1
            index = 0


class ParserFirstRange(ParserMain):
    def get_games_dates(self, sheet):
        date_list = []
        for cell in sheet[1]:
            if cell.value == 'Оплата':
                break
            if type(cell.value) is datetime and\
                    sheet[str(cell.column) + str(cell.row + 1)].value is not None and\
                    sheet[str(cell.column) + str(cell.row + 1)].value != 'нэбыло':
                date_list.append(cell)
                GLOBAL_DATES_LIST.append(cell.value)
                self.cursor.execute("INSERT IGNORE INTO SoccerGames (SoccerGameDate) VALUES('{0}')".format(cell.value))
                self.connection.autocommit("Add dates to SoccerGameDate")
        return date_list

    @staticmethod
    def get_games_scores(sheet):
        score_list = [[]]
        for cell in sheet[2]:
            score = str(cell.value)
            if cell.fill.start_color.index == YELLOWCOLOR:
                break
            if score is not None and  score.find('-') != -1 and\
                cell.fill.start_color.index != PURPLECOLOR and\
                    cell.column != 'A':
                score_list.append([score, cell.fill.start_color.index])
        score_list.pop(0)
        return score_list

    def delete_last_list_from_db(self, sheet):
        title_year, title_month = self.get_data_from_sheet(sheet)
        date_source = str(title_year) + '-' + title_month + '-' + '01'
        normal_date = datetime.strptime(date_source, "%y-%m-%d").date()
        self.cursor.execute("SELECT SoccerGameID FROM SoccerGames WHERE SoccerGameDate >= '{0}';".format(normal_date))
        index_list = self.cursor.fetchall()
        self.connection.autocommit('Get all indexes')
        for index in index_list:
            self.cursor.execute("DELETE FROM MappingPlayersSoccerGames WHERE SoccerGameID = {0}".format(int(index[0])))
        self.connection.autocommit('Delete from MPSG one row')

    def run(self, sheet):
        self.get_player_stats(sheet, self.get_games_dates(sheet), self.get_players_from_sheet(sheet),
                              self.get_games_scores(sheet))


class ParserSecondRange(ParserMain):
    def get_games_dates(self, sheet):
        date_list = []
        for cell in sheet['B']:
            if cell.value == "дата":
                start_cell = cell
                break
        for cell in sheet[start_cell.row]:
            if cell.value == 'Оплата':
                break
            if type(cell.value) is datetime and\
                    sheet[str(cell.column) + str(cell.row - 1)].value is not None:
                date_list.append(cell)
                GLOBAL_DATES_LIST.append(cell.value)
                self.cursor.execute("INSERT IGNORE INTO SoccerGames (SoccerGameDate) VALUES('{0}')".format(cell.value))
                self.connection.autocommit("Add dates to SoccerGameDate")
        return date_list

    def get_games_scores(self, sheet):
        score_list = [[]]
        for cell in sheet['B']:
            if cell.value == 'счет':
                score_cell = cell
                break
        for cell in sheet[score_cell.row]:
            score = str(cell.value)
            if score is not None and\
                    score.find('-') != -1 and\
                    cell.fill.start_color.index != PURPLECOLOR:
                score_list.append([score, cell.fill.start_color.index])
        score_list.pop(0)
        return score_list

    def run(self, sheet):
        self.get_player_stats(sheet, self.get_games_dates(sheet), self.get_players_from_sheet(sheet),
                              self.get_games_scores(sheet))


def get_all_players_stats(self, file_path):
    db.recreateDB()
    main_parser = ParserMain(file_path)
    main_parser.get_player_list(lastpage=False)
    main_parser.get_all_games_dates()
    for sheet in main_parser.wb:
        if len(sheet.title) <= 4:
            title_year, title_month = self.get_data_from_sheet(sheet)
            if title_year >= 14 or (title_year >= 13 and title_month > 3):
                parser = ParserFirstRange(file_path)
                parser.run(sheet)
                print("Page {0}{1} completed!".format(title_year, title_month))
            else:
                parser = ParserSecondRange(file_path)
                parser.run(sheet)
                print("Page {0}{1} completed!".format(title_year, title_month))


# This function will get info only from last list
def update_players_stats(file_path):
    main_parser = ParserMain(file_path)
    main_parser.get_player_list(lastpage=True)
    main_parser.get_all_games_dates()
    for sheet in main_parser.wb:
        if len(sheet.title) <= 4:
            parser = ParserFirstRange(file_path)
            parser.run(sheet)
            print(sheet.title + " Complete!")
            break
