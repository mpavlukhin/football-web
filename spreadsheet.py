import urllib.request
from itertools import zip_longest
import xlrd


def diff_xlsx(xlsx_one, xlsx_two):
    rb1 = xlrd.open_workbook(xlsx_one)
    rb2 = xlrd.open_workbook(xlsx_two)

    for sheet1, sheet2 in zip(rb1.sheets(), rb2.sheets()):
        for rownum in range(max(sheet1.nrows, sheet2.nrows)):
            if rownum < sheet1.nrows:
                row_rb1 = sheet1.row_values(rownum)
                row_rb2 = sheet2.row_values(rownum)

                for colnum, (c1, c2) in enumerate(zip_longest(row_rb1, row_rb2)):
                    if c1 != c2:
                        # print ("Row {} Col {} - {} != {}".format(rownum + 1, colnum + 1, c1, c2))
                        return False
            else:
                # print ("Row {} missing".format(rownum + 1))
                return False

    return True


def download_sheet(url='https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=1QH-AFYHk3lXJf-dG3FzhDwt'
                       'O6iJZus7ZXWoY8aBs7ZI&exportFormat=xlsx',
                   file_name='data/spreadsheets/Football-bigdata-v0.2.xlsx'):
    urllib.request.urlretrieve(url, file_name)