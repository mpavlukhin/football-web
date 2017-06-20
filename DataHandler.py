import pandas as pd
import openpyxl as pyxl
import datetime as dt

# years_included = ('15', '14')
years_included = ['12', '13']

def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'

    preCreateStatsSheet("NewStats", filepath)
    activeSheets = findActiveSheets(filepath)
    fillPersons(activeSheets)

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
    wb = pyxl.load_workbook(filepath)

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

def fillPersons(activeSheets):
    for sheetName in activeSheets:
        print('\nThis sheet is ' + sheetName)
        temp = sheetName
        if (sheetName.__len__() == 3):
            temp = '0' + sheetName

        month = temp[0:2:1]
        year = temp[-2::1]

        print('month: ' + month + " year: " + year)

        footballDate = dt.date(2000 + int(year), int(month), 1)
        print(footballDate)

        # values = getColumnNamesRange(currentSheet)