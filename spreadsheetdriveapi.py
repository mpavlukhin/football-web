from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def download_spreadsheet(export_file):
    gauth = GoogleAuth(settings_file='settings.yaml')
    try:
        gauth.LoadCredentialsFile('client-creds.json')
    except Exception:
        pass
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile('client-creds.json')
    drive = GoogleDrive(gauth)


    fileTitle = 'Football-bigdata-v0.2'
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    if not fileTitle:
        fileTitle = input('Input spreadsheet name with full path which you want to download: ')

    for file1 in file_list:
        if (file1['title'] == fileTitle) and (file1['mimeType'] == 'application/vnd.google-apps.spreadsheet'):
            download_mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            open(export_file, 'w+').close()
            file1.GetContentFile(export_file, mimetype=download_mimetype)
            fileLink = file1['alternateLink']
            return fileTitle, fileLink

    print('Error, wrong name')
