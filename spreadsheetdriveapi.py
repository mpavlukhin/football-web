from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def downloadxlsx(fileTitle):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

    mimetypes = {
        # Drive Document files as MS Word files.
        #'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

        # Drive Sheets files as MS Excel files.
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        # etc.
    }

    drive = GoogleDrive(gauth)
    # Auto-iterate through all files that matches this query
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    print('All your spreadsheet files on your Google Drive')

    for file1 in file_list:
        if file1['mimeType'] in mimetypes:
            print('File: %s' % (file1['title']))

    if not fileTitle:
        fileTitle = input('Input spreadsheet name which you want to download: ')
    donwloadornot = False
    for file1 in file_list:
        download_mimetype = None
        if file1['mimeType'] in mimetypes:
            download_mimetype = mimetypes[file1['mimeType']]
            if file1['mimeType'] in mimetypes and file1['title'] == fileTitle:
                file1.GetContentFile('data/spreadsheets/' + fileTitle + '.xlsx', mimetype=download_mimetype)
                print('Successfully downloaded')
                donwloadornot = True
                return fileTitle
                break
    if donwloadornot == False:
        print('Error, wrong name')





