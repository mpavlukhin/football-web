import pandas as pd
import openpyxl as pyxl
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, Alignment
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def as_text(value):
    if value is None:
        return ""
    return str(value)

def preCreateStatsSheet(sheetname, filepath): #realized
    wb = pyxl.load_workbook(filepath)
    # print(wb.get_sheet_names())
    statsSheet = wb.create_sheet(sheetname, 0)
    # statsSheet = wb.active
    statsSheet.title = sheetname
    statsSheet.append(["Имя", "Победы", "Ничьи", "Поражения", "Всего Игр", "Коэффициент побед", "Коэффициент очков"])
    # print(statsSheet.max_column)
    # for column_cells in statsSheet.columns:
    #     length = max(len(as_text(cell.value)) for cell in column_cells)
    #     statsSheet.column_dimensions[column_cells[0].column].width = length + 4
    # first_row = statsSheet[1]
    # for cell in first_row:
    #     alignment_obj = cell.alignment.copy(horizontal='center', vertical='center')
    #     font_obj = cell.font.copy(bold=True)
    #     cell.alignment = alignment_obj
    #     cell.font = font_obj
    wb.save(filename=filepath)

def getdataframefromfile(fileTitle):
    filepath = 'data/spreadsheets/' + fileTitle + '.xlsx'
    preCreateStatsSheet("NewStats", filepath)
    input()
    data = pd.read_excel(filepath)
    return data

