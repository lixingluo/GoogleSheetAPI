from __future__ import print_function
import httplib2
import os
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, timedelta

BIN='/opt/googleapis/bin'

def getCredentials():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Fairplay'

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com.fairplay.json')
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        client_secret_dir = os.path.join(os.getcwd(), '.credentials')
        clientsecret_path = os.path.join(client_secret_dir, CLIENT_SECRET_FILE)
        flow = client.flow_from_clientsecrets(clientsecret_path, SCOPES)
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)

    return credentials

def updateSheets(spreadsheetId, rangeName, valueInputOption, body):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl) 
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, 
                valueInputOption=valueInputOption, body=body).execute()

def main():
    spreadsheetId = '1TcmtvfiyRDC7mjPbOZNhcIeqBJGqasBf6bA5EnCbUoI'
    rangeName = 'FairPlay!A4:A4'
    valueInputOption = 'USER_ENTERED'
    # dateFrom = datetime.strftime(datetime.now() - timedelta(8), '%Y-%m-%d')
    dateTo = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    values = [
        [dateTo]
    ]
    body = {
        "values": values
    }
    updateSheets(spreadsheetId, rangeName, valueInputOption, body)

if __name__ == '__main__':
    main()



