import urllib.request


def download_sheet(url='https://spreadsheets.google.com/feeds/download/'
                       'spreadsheets/Export?key=1ReoKdwH_t62mnRHEae3f8'
                       'yq_gYtKH8gTjzlWDOt0TUU&exportFormat=xlsx',
                   file_name='data/spreadsheets/Football-bigdata-v0.2.xlsx'):
    urllib.request.urlretrieve(url, file_name)