import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('football').sheet1

pp = pprint.PrettyPrinter()

# result = sheet.col_values(6)
# pp.pprint(result)

#values_list = sheet.col_values(1)
#pp.pprint(values_list)
#footballs = sheet.get_all_records()
#pp.pprint(footballs)

# i = 1
# while (sheet.cell(i, 0)):
#     result = sheet.row_values(6)
#     # pp.pprint(result))


def getStatsArray():
    i = 2
    result = sheet.cell(i, 1).value
    listOfNames = list()

    while not ('-' in result):
        result = sheet.cell(i, 1).value
        # listOfNames.append(listOfNames, result)
        print(result)
        i += 1

    return listOfNames


getStatsArray()