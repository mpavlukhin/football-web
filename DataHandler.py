import pandas as pd
import openpyxl as pyxl

# years_included = ('15', '14')
years_included = ['17']

def preCreateStatsSheet(sheetname, filepath):
    wb = pyxl.load_workbook(filepath)
    # print(wb.get_sheet_names())
    stat = wb.create_sheet(sheetname, 0)
    stat.title = sheetname
    stat.append([''])
    wb.save(filename=filepath)

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

def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'
    data = pd.read_excel(filepath)
    # preCreateStatsSheet("NewStats", filepath)
    findActiveSheets(filepath=filepath)
    return data

getdataframefromfile('football')