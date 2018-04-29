import urllib.request


def download_sheet(url='https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=1QH-AFYHk3lXJf-dG3FzhDwt'
                       'O6iJZus7ZXWoY8aBs7ZI&exportFormat=xlsx',
                   file_name='data/spreadsheets/Football-bigdata-v0.2.xlsx'):
    urllib.request.urlretrieve(url, file_name)
