from __future__ import print_function
import httplib2
import os
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

BIN = '/opt/googleapis/bin'

def getCredentials():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API WideWine Sum Total'

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-widewin.json')
    store = Storage(credential_path)
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        client_secret_dir = os.path.join(BIN, '.credentials')
        clientsecret_path = os.path.join(client_secret_dir, CLIENT_SECRET_FILE)
        flow = client.flow_from_clientsecrets(clientsecret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)

    return credentials

def updateSheetValues(spreadsheetId,rangeName,body):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,
                valueInputOption='USER_ENTERED', body=body).execute()

def main():
    spreadsheetId = '1QqAPP7ZfOh8o-60cjKbC7AtheodBwtWY2GMCcf8wMjg'
    rangeName = 'Widevine Usage!B4:F'
    values = [
    ['=I4+N4+S4+X4','=J4+O4+T4+Y4','=K4+P4+U4+Z4','=L4+Q4+V4+AA4','=M4+R4+W4+AB4']
    ]
    body = {
    'values': values
    }
    updateSheetValues(spreadsheetId,rangeName,body)

if __name__ == '__main__':
    main()
