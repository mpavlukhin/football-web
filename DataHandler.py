import pandas as pd
import openpyxl as pyxl




def preCreateStatsSheet(sheetname, filepath):
    wb = pyxl.load_workbook(filepath)
    # print(wb.get_sheet_names())
    stat = wb.create_sheet(sheetname, 0)
    stat.title = sheetname
    stat.append([''])
    wb.save(filename=filepath)



def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'
    data = pd.read_excel(filepath)
    preCreateStatsSheet("NewStats", filepath)
    return data

getdataframefromfile('football')