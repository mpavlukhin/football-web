import pandas as pd
import spreadsheetdriveapi as drive

def getdataframefromfile(fileTitle):
    data = pd.read_excel('data/spreadsheets/' + fileTitle + '.xlsx')
    return data