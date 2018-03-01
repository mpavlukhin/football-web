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

DATESLIST = []
PLAYERSLIST = []

GLOBALPLAYERINDEX = 1
GLOBALDATEINDEX = 1

# CURSOR, CONNECTION = db.connection()
# Заинсертить все имена и все даты как-то, после чего брать из списков DATELIST и PLAYERLIST по id (index + 1)
# Понять как сделать обшую функцию для расчета статистики на текущей странице
#
class ParserMain():
    def getPlayersList(self, lastpage):
        CURSOR, CONNECTION = db.connection()
        playersList = []
        column = 'B'
        for sheet in self.wb:
            if((len)(sheet.title) <= 4):
                titledata = sheet.title
                titleyear = (int)(titledata[-2:])
                if(titleyear >= 14):
                    column = 'A'
                else:
                    column = 'B'
                for cell in sheet[column]:
                    if (cell.value == None or cell.value == '' or (cell.value == 'Сумма' and cell.row > 5)
                        or (cell.value == 'счет' and cell.row > 5)):
                        break
                    if(cell.value != 'Имя' and cell.value != 'счет' and cell.value != 'Сумма' and cell.value != 'Аренда'
                         and cell.value != 'Guests ' and cell.value != '' and cell.value != 'дата'):
                        playername = cell.value
                        if(PLAYERSLIST.count(playername) == 0):
                            PLAYERSLIST.append(playername)
                            playersList.append(cell)
                            CURSOR.execute("INSERT IGNORE Players(PlayerName) VALUES('{0}')".format(cell.value))
                            CONNECTION.autocommit("Inserting to Players")
            if lastpage:
                break
        return playersList


    def getAllGamesDates(self, lastpage):
        CURSOR, CONNECTION = db.connection()
        datelist = []

        for sheet in self.wb:
            if ((len)(sheet.title) <= 4):
                titledata = sheet.title
                titleyear = (int)(titledata[-2:])
                titlemonth = (int)(titledata.replace(' ', '')[:-2])
                if (titleyear >= 14 or (titleyear >= 13 and titlemonth > 3)):
                    for cell in sheet[1]:
                        if(cell.value == 'Оплата'):
                            break
                        if(type(cell.value) is datetime and sheet[(str)(cell.column) + (str)(cell.row + 1)].value != None
                           and sheet[(str)(cell.column) + (str)(cell.row + 1)].value != 'нэбыло'):
                            datelist.append(cell)
                            DATESLIST.append(cell.value)
                            CURSOR.execute("INSERT IGNORE INTO SoccerGames (SoccerGameDate) VALUES('{0}')".format(cell.value))
                            CONNECTION.autocommit("Add dates to SoccerGameDate")
                else:
                    for cell in sheet['B']:
                        if(cell.value == "дата"):
                            startcell = cell
                            break
                    for cell in sheet[startcell.row]:
                        if(cell.value == 'Оплата'):
                            break
                        if (type(cell.value) is datetime and sheet[(str)(cell.column) + (str)(cell.row - 1)].value != None):
                            datelist.append(cell)
                            DATESLIST.append(cell.value)
                            CURSOR.execute("INSERT IGNORE INTO SoccerGames (SoccerGameDate) VALUES('{0}')".format(cell.value))
                            CONNECTION.autocommit("Add dates to SoccerGameDate")
        return datelist


    def getPlayersFromSheet(self, sheet):
        playersRange = []
        titledata = sheet.title
        titleyear = (int)(titledata[-2:])
        if (titleyear >= 14):
            column = 'A'
        else:
            column = 'B'
        for cell in sheet[column]:
            if (cell.value == None or cell.value == '' or (cell.value == 'Сумма' and cell.row > 5)
                or (cell.value == 'счет' and cell.row > 5)):
                break
            if (cell.value != 'Имя' and cell.value != 'счет' and cell.value != 'Сумма' and cell.value != 'Аренда'
                and cell.value != 'Guests ' and cell.value != 'дата' and cell.value != 'счет'):
                playersRange.append(cell)
        return playersRange


    def getPlayersStats(self, sheet, datelist, playerslist, gamesscore):
        CURSOR, CONNECTION = db.connection()

        playerresult = 'L'
        playerscore = 0
        typeofgame = ''
        output = [[]]
        index = 0
        for playercell in playerslist:
            for datecell in datelist:
                currentcell = sheet[(str)(datecell.column) + (str)(playercell.row)]
                currentcellcolor = currentcell.fill.start_color.index
                if(currentcellcolor == WHITECOLOR or currentcellcolor == WHITECOLOR2):
                    index += 1
                    continue
                typeofgame = gamesscore[index]
                currentscore = (str)(typeofgame[0])
                gamecolor = typeofgame[1]
                currentscore = currentscore.split('-')
                # This cases for games with 2 teams
                if(len(currentscore) == 2):
                    team1score = (float)(currentscore[0])
                    team2score = (float)(currentscore[1])
                    if(team1score == team2score):
                        playerresult = 'D'
                        playerscore = 1
                    elif(currentcellcolor == gamecolor):
                        playerresult = 'W'
                        playerscore = 3
                    else:
                        playerresult = 'L'
                        playerscore = 0
                # This cases for games with 3 teams
                elif(len(currentscore) == 3):
                    team1score = (float)(currentscore[0])
                    team2score = (float)(currentscore[1])
                    team3score = (float)(currentscore[2])
                    # 1 Case   # For example Game W - D - L (3 - 1 - 0)
                    if (team1score > team2score and team2score > team3score and team1score != team2score):
                        if (currentcellcolor == REDCOLOR):
                            playerscore = 3
                            playerresult = 'W'
                        elif (currentcellcolor == GREENCOLOR or currentcellcolor == GREENCOLOR2
                              or currentcellcolor == GREENCOLOR3):
                            playerscore = 1
                            playerresult = 'D'
                        if (currentcellcolor == BLUECOLOR):
                            playerscore = 0
                            playerresult = 'L'
                    # 2 Case   # For example Game D - D - L (1 - 1 - 0)
                    elif (team1score == team2score and team2score > team3score):
                        if (currentcellcolor == GREENCOLOR or currentcellcolor == REDCOLOR):
                            playerscore = 2
                            playerresult = 'D'
                        else:
                            playerscore = 0
                            playerresult = 'L'
                    # 3 Case   # For example Game W - D - D (3 - 1 - 1)
                    elif (team1score > team2score and team2score == team3score):
                        if (currentcellcolor == REDCOLOR):
                            playerscore = 3
                            playerresult = 'W'
                        else:
                            playerscore = 1
                            playerresult = 'D'
                    # 4 Case   # For example Game D - D - D (1 - 1 - 1)
                    elif (team1score == team2score and team2score == team3score):
                        playerscore = 1
                        playerresult = 'D'
                # playerindex = PLAYERSLIST.index(playercell.value) + 1
                # gamedateindex = DATESLIST.index(datecell.value) + 1
                CURSOR.execute("SELECT PlayerID FROM Players WHERE PlayerName = '{0}';".format(playercell.value))
                player_id = CURSOR.fetchone()
                CURSOR.execute("SELECT SoccerGameID from soccergames WHERE SoccerGameDate = '{0}';".format(datecell.value))
                game_date_id = CURSOR.fetchone()
                CURSOR.execute(
                    "INSERT IGNORE INTO MappingPlayersSoccerGames VALUES ( {0}, {1}, {2}, '{3}')".format(
                        player_id[0], game_date_id[0],
                        playerscore
                        , playerresult))
                CONNECTION.autocommit("Inserting to MappingPlayers")
                index += 1
    #         Making INSERT for DB
            index = 0

    def __init__(self, filepath):
        self.file = filepath
        self.wb = pyxl.load_workbook(filepath, data_only=True)


# Correct Name
class ParserFirstRange(ParserMain):

    def getGamesDates(self, sheet):
        CURSOR, CONNECTION = db.connection()

        c, conn = db.connection()
        datelist = []
        for cell in sheet[1]:
            if(cell.value == 'Оплата'):
                break
            if(type(cell.value) is datetime and sheet[(str)(cell.column) + (str)(cell.row + 1)].value != None
               and sheet[(str)(cell.column) + (str)(cell.row + 1)].value != 'нэбыло'):
                datelist.append(cell)
                DATESLIST.append(cell.value)
                CURSOR.execute("INSERT IGNORE INTO SoccerGames (SoccerGameDate) VALUES('{0}')".format(cell.value))
                CONNECTION.autocommit("Add dates to SoccerGameDate")
        return datelist



    def getGamesScores(self, sheet):
        scorelist = [[]]
        for cell in sheet[2]:
            score = (str)(cell.value)
            if(cell.fill.start_color.index == YELLOWCOLOR):
                break
            if(score != None and  score.find('-') != -1 and cell.fill.start_color.index != PURPLECOLOR
               and cell.column != 'A'):
                scorelist.append([score, cell.fill.start_color.index])
        scorelist.pop(0)
        return scorelist


    def deletelastlistfromDB(self, sheet):
        CURSOR, CONNECTION = db.connection()

        titledata = sheet.title
        titleyear = (str)(titledata[-2:])
        titlemonth = (str)(titledata.replace(' ', '')[:-2])
        datesrc = titleyear + '-' + titlemonth + '-' + '01'
        normal_date = datetime.strptime(datesrc, "%y-%m-%d").date()
        CURSOR.execute("SELECT SoccerGameID FROM SoccerGames WHERE SoccerGameDate >= '{0}';".format(normal_date))
        indexlist = CURSOR.fetchall()
        CONNECTION.autocommit('Get all indexes')
        for index in indexlist:
            CURSOR.execute("DELETE FROM MappingPlayersSoccerGames WHERE SoccerGameID = {0}".format((int)(index[0])))
        CONNECTION.autocommit('Delete ofrom MPSG one row')


    def run(self, sheet, lastpage):
        self.getPlayersStats(sheet, self.getGamesDates(sheet), self.getPlayersFromSheet(sheet),
                             self.getGamesScores(sheet))


class ParserSecondRange(ParserMain):
    def getGamesDates(self, sheet):
        CURSOR, CONNECTION = db.connection()
        datelist = []
        for cell in sheet['B']:
            if(cell.value == "дата"):
                startcell = cell
                break
        for cell in sheet[startcell.row]:
            if(cell.value == 'Оплата'):
                break
            if (type(cell.value) is datetime and sheet[(str)(cell.column) + (str)(cell.row - 1)].value != None):
                datelist.append(cell)
                DATESLIST.append(cell.value)
                CURSOR.execute("INSERT IGNORE INTO SoccerGames (SoccerGameDate) VALUES('{0}')".format(cell.value))
                CONNECTION.autocommit("Add dates to SoccerGameDate")
        return datelist


    def getGamesScores(self, sheet):
        scorelist = [[]]
        for cell in sheet['B']:
            if cell.value == 'счет':
                scorecell = cell
                break
        for cell in sheet[scorecell.row]:
            score = (str)(cell.value)
            if(score != None and score.find('-') != -1 and  cell.fill.start_color.index != PURPLECOLOR):
                scorelist.append([score, cell.fill.start_color.index])
        scorelist.pop(0)
        return scorelist


    def run(self, sheet):
        self.getPlayersStats(sheet, self.getGamesDates(sheet), self.getPlayersFromSheet(sheet),
                             self.getGamesScores(sheet))


def getAllPlayersStats(filepath):
    db.recreateDB()
    P = ParserMain(filepath)
    P.getPlayersList(lastpage=False)
    P.getAllGamesDates(lastpage=False)
    for sheet in P.wb:
        if ((len)(sheet.title) <= 4):
            titledata = sheet.title
            titleyear = (int)(titledata[-2:])
            titlemonth = (int)(titledata.replace(' ', '')[:-2])
            if (titleyear >= 14 or (titleyear >= 13 and titlemonth > 3)):
                Parser = ParserFirstRange(filepath)
                Parser.run(sheet, lastpage=False)
                print(titledata + ' Complete!')
            else:
                Parser = ParserSecondRange(filepath)
                Parser.run(sheet)
                print(titledata + ' Complete!')


# This function will get info only from last list
def updatePlayersStats(filepath):
    P = ParserMain(filepath)
    P.getPlayersList(lastpage=True)
    P.getAllGamesDates(lastpage=True)
    for sheet in P.wb:
        if ((len)(sheet.title) <= 4):
            Parser = ParserFirstRange(filepath)
            Parser.run(sheet, lastpage=True)
            print(sheet.title + " Complete!")
            break
