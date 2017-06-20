import pandas as pd
import openpyxl as pyxl

# years_included = ('15', '14')
years_included = ['12', '13']

def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'

    preCreateStatsSheet("NewStats", filepath)
    activeSheets = findActiveSheets(filepath)
    fillPersons(activeSheets)

    data = pd.read_excel(filepath)
    return data

def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'

    preCreateStatsSheet("NewStats", filepath)
    findActiveSheets(filepath)

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

def getColumnNamesRange(currentSheet):
    range = []
    startrow = 4000 #example max people
    rows = currentSheet.max_row
    maxrows = None
    titledata = (str)(currentSheet.title)
    titleyear = (int)(titledata[-2:])
    titlemonth = (int)(titledata.replace(titledata,titledata[-2:]))
    print("titlemonth =", titlemonth, "titleyear=",titleyear)
    # case 1 Current date - 12/13 (First column)
    if((titleyear >= 13 and titlemonth >= 12) or titleyear >= 14):
        for cell in currentSheet['A']:
            if(cell.value == 'Аренда'):
                startrow = (int)(cell.row)
            if(cell.value == '' or cell.value == None):
                break
            if((int)(cell.row) > startrow):
                range.append(cell.value)

        return range
    #Case 2 12/13 - 04/13 Second column(First column have numeration)
    elif(titleyear == 13 and (titlemonth >= 4 and titlemonth <= 12)):
        for cell in currentSheet['B']:
            if(cell.value == 'Аренда'):
                startrow = (int)(cell.row)
            if(cell.value == '' or cell.value == None):
                maxrows = (int)(cell.row)
                break
        range = maxrows - startrow
        return range
    else:
        for cell in currentSheet['B']:
            if(cell.value == "счет" or cell.value == "Сумма"):
                break
            else:
                range.append(cell.value)

        return range
