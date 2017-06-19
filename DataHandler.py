import pandas as pd
import openpyxl as pyxl

# years_included = ('15', '14')
years_included = ['17']

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

def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'

    preCreateStatsSheet("NewStats", filepath)
    findActiveSheets(filepath)

    data = pd.read_excel(filepath)
    return data

def findActiveSheets(filepath):
    wb = pyxl.load_workbook(filepath)

    ws = wb.get_sheet_names()

    activeSheets = list()
    for sheet in ws:
        if(isYearOK(sheet)):
            activeSheets.append(sheet)
    print("Total number of all sheets = " + str(activeSheets.__len__()))

    print("This is pages:")
    for sheetName in activeSheets:
        print (sheetName)

    return sheetName

def isYearOK(year):
    if (years_included == None):
        raise 'No selected years Error'

    for years in years_included:
        if (year.rfind(years) != -1):
            return True

    return False