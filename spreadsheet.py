import urllib.request

# Download spreadsheet from Google Drive Service
def download_sheet():
    url = 'https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=1ReoKdwH_t62mnRHEae3f8yq_gYtKH8gTjzlWDOt0TUU&exportFormat=xlsx'
    file_name = 'data/spreadsheets/football.xlsx'

    urllib.request.urlretrieve(url, file_name)

# Check this out
download_sheet()