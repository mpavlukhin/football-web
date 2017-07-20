from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import webbrowser


def google_auth_init():
    return GoogleAuth()


def oauth_redirect_handler(gauth):
    return webbrowser.open_new_tab(gauth.GetAuthUrl())


def oauth_authenticate(gauth, code):
    gauth.Authenticate(code)


def downloadxlsx(fileTitle, gauth):
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    if not fileTitle:
        fileTitle = input('Input spreadsheet name which you want to download: ')

    for file1 in file_list:
        if (file1['title'] == fileTitle) and (file1['mimeType'] == 'application/vnd.google-apps.spreadsheet'):
            download_mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            file1.GetContentFile('data/spreadsheets/' + fileTitle + '.xlsx', mimetype=download_mimetype)
            fileLink = file1['alternateLink']
            return fileTitle, fileLink

    print('Error, wrong name')
