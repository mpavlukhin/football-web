import pandas as pd
import openpyxl as pyxl
import datetime as dt

# years_included = ('15', '14')
years_included = ['12', '13']

def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'

    preCreateStatsSheet("NewStats", filepath)
    activeSheets = findActiveSheets(filepath)
    fillPersons(activeSheets, filepath)

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

def fillPersons(activeSheets, filePath):
    footballPlayers = set()

    for sheetName in activeSheets:
        print('\nThis sheet is ' + sheetName)

        temp = set(getColumnNamesRange(sheetName))

        footballPlayers.update(temp)
        print('List of football players on this sheet:')
        for playerName in footballPlayers:
            print(playerName)

    wb = pyxl.load_workbook(filePath)
    statsSheet = wb.get_sheet_by_name('NewStats')

    row = 2
    for playerName in footballPlayers:
        statsSheet.cell(row=row, column=1).value = playerName
        row += 1

    wb.save(filename=filePath)

def getColumnNamesRange(currentSheet):
    range = []
    startrow = 4000 #example max people
    rows = currentSheet.max_row
    maxrows = None
    titledata = (str)(currentSheet.title)
    titleyear = (int)(titledata[-2:])
    titlemonth = (int)(titledata.replace(' ', '')[:-2])
    # case 1 Current date - 12/13 (First column)
    if((titleyear >= 13 and titlemonth >= 12) or titleyear >= 14):
        for cell in currentSheet['A']:
            if(cell.value == 'Аренда'):
                startrow = (int)(cell.row)
            if(cell.value == '' or cell.value == None):
                break
            if((int)(cell.row) > startrow):
                range.append(cell.value)

    #Case 2 12/13 - 04/13 Second column(First column have numeration)
    elif(titleyear == 13 and (titlemonth >= 4 and titlemonth <= 12)):
        for cell in currentSheet['B']:
            if(cell.value == 'Аренда'):
                startrow = (int)(cell.row)
            if(cell.value == '' or cell.value == None):
                break
            if ((int)(cell.row) > startrow):
                range.append(cell.value)
    else:
        for cell in currentSheet['B']:
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