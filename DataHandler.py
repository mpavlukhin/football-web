import pandas as pd
import openpyxl as pyxl
import numpy as np

years_included = ['13']
newStats = 'NewStats'

def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'

    rangevalues = np.array([])

    preCreateStatsSheet(newStats, filepath)
    activeSheets = findActiveSheets(filepath)
    persons = fillPersons(activeSheets, filepath, rangevalues)

    analyzePersons(persons, filepath)

    data = pd.read_excel(filepath)
    return data

def as_text(value):
    if value is None:
        return ""
    return str(value)

def preCreateStatsSheet(sheetname, filepath): #realized
    wb = pyxl.load_workbook(filepath)

    statsSheet = wb.create_sheet(sheetname, 0)
    statsSheet.title = sheetname
    statsSheet.append(["Имя", "Победы", "Ничьи", "Поражения", "Всего Игр", "Коэффициент побед", "Коэффициент очков"])

    wb.save(filename=filepath)

def findActiveSheets(filepath):
    wb = pyxl.load_workbook(filepath, data_only=True)

    ws = wb.get_sheet_names()

    activeSheets = list()
    for sheet in ws:
        if (isYearOK(sheet)) and sheet.find('Stats') == -1 and sheet.find('год') == -1:
            activeSheets.append(sheet)
    print("Total number of all sheets = " + str(activeSheets.__len__()))

    print("This is pages:")
    for sheetName in activeSheets:
        print (sheetName)

    return activeSheets

def isYearOK(year):
    if (years_included == None):
        raise 'No selected years Error'

    for years in years_included:
        if (year[-2::1].rfind(years) != -1):
            return True

    return False

def fillPersons(activeSheets, filePath, rangevalues):
    footballPlayers = set()

    for sheetName in activeSheets:
        # print('\nThis sheet is ' + sheetName)

        temp = set(getColumnNamesRange(sheetName, filePath, rangevalues))

        # if temp.__contains__(None):
        #     print('NONE NONE NONE NONE NONE NONE NONE NONE NONE NONE NONE')

        footballPlayers.update(temp)
        # print('List of football players on this sheet:')
        # for playerName in footballPlayers:
        #     print(playerName)

    wb = pyxl.load_workbook(filePath)
    statsSheet = wb.get_sheet_by_name(newStats)

    row = 2
    for playerName in footballPlayers:
        statsSheet.cell(row=row, column=1).value = playerName
        row += 1

    wb.save(filename=filePath)

    return footballPlayers

def getColumnNamesRange(currentSheet, filepath, rangevalues):
    wb = pyxl.load_workbook(filepath, data_only=True)
    ws = wb.get_sheet_by_name(currentSheet)

    range = []
    startrow = 4000 #example max people
    rows = ws.max_row
    maxrows = None
    titledata = ws.title
    titleyear = (int)(titledata[-2:])
    titlemonth = (int)(titledata.replace(' ', '')[:-2])

    # case 1 Current date - 12/13 (First column)
    if((titleyear >= 13 and titlemonth >= 12) or titleyear >= 14):
        for cell in ws['A']:
            if(cell.value == 'Аренда'):
                startrow = (int)(cell.row)
            if(cell.value == '' or cell.value == None):
                break
            if((int)(cell.row) > startrow):
                range.append(cell.value)

    #Case 2 12/13 - 04/13 Second column(First column have numeration)
    elif(titleyear == 13 and (titlemonth >= 4 and titlemonth <= 12)):
        for cell in ws['B']:
            if(cell.value == 'Аренда'):
                startrow = (int)(cell.row)
            if(cell.value == '' or cell.value == None):
                break
            if ((int)(cell.row) > startrow):
                range.append(cell.value)
    else:
        for cell in ws['B']:
            if(cell.value == "счет" or cell.value == "Сумма"):
                break
            else:
                range.append(cell.value)

    for people in range:
        if people == "Guests":
            range.remove("Guests")
        elif people == "Guests ":
            range.remove("Guests ")
    return range

def analyzePersons(persons, filePath):
    # TEST DATA ARRAY
    persons = np.array([
        ['name1', 10, 1, 12],
        ['name2', 5, 3, 10],
        ['name3', 3, 1, 11],
        ['name4', 2, 1, 4],
        ['name1', 7, 1, 10],
        ['name5', 5, 2, 10],
        ['name1', 3, 2, 5],
        ['name2', 3, 5, 10],
        ['name1', 5, 1, 7],

        ['Clenov', 1, 0, 4], # 12/13
        ['Clenov', 2, 1, 3], # 11/13
                             # 10/13
        ['Clenov', 2, 1, 4], # 09/13
        ['Clenov', 2, 0, 4], # 08/13
                             # 07/13
        ['Clenov', 3, 0, 7], # 06/13
        ['Clenov', 0, 0, 2], # 05/13
                             # 04/13
        ['Clenov', 0, 0, 2], # 03/13
        ['Clenov', 1, 0, 2], # 02/13
        ['Clenov', 2, 0, 5]  # 01/13
    ])
    # END TEST DATA ARRAY

    wb = pyxl.load_workbook(filePath)
    statsSheet = wb.get_sheet_by_name(newStats)

    # Process the list of persons
    i = 0
    k = 0

    # for person in persons:
    while (k < persons.shape[0]):
        # One sheet info
        footballplayername = persons[k,0]

        # Sum player's stat and delete useless info
        deletingindexes = list()
        for j in range(i + 1, persons.shape[0]):
            if (footballplayername == persons[j, 0]):
                persons[i, 1] = int(persons[i, 1]) + int(persons[j, 1])
                persons[i, 2] = int(persons[i, 2]) + int(persons[j, 2])
                persons[i, 3] = int(persons[i, 3]) + int(persons[j, 3])
                deletingindexes.append(j)

        persons = np.delete(persons, deletingindexes, 0)

        footballplayerwins = int(persons[k,1])
        footballplayerdraws = int(persons[k,2])
        footballplayernumofgames = int(persons[k,3])

        footballplayervictoryrate = str(int((footballplayerwins / footballplayernumofgames) * 100)) + '%'
        footballplayerscorerate = str(
            int(((footballplayerwins * 3 + footballplayerdraws * 1.5) / (footballplayernumofgames * 3)) * 100)) + '%'

        # Set info to the stats
        row = i + 2
        statsSheet.cell(row=row, column=2).value = footballplayerwins
        statsSheet.cell(row=row, column=3).value = footballplayerdraws
        statsSheet.cell(row=row, column=4).value = footballplayernumofgames - footballplayerwins - footballplayerdraws
        statsSheet.cell(row=row, column=5).value = footballplayernumofgames
        statsSheet.cell(row=row, column=6).value = footballplayervictoryrate
        statsSheet.cell(row=row, column=7).value = footballplayerscorerate

        i += 1
        k += 1

    wb.save(filename=filePath)