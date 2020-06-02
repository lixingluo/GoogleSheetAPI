from __future__ import print_function
import httplib2
import os
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, timedelta

def getCredentials():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API WideWine Insert Date'

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flag = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-widewin.json')
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        CWD = os.getcwd()
        client_secret_dir = os.path.join(CWD, '.credentials')
        clientsecret_path = os.path.join(client_secret_dir, CLIENT_SECRET_FILE)
        flow = client.flow_from_clientsecrets(clientsecret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials

def main():
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    spreadsheetId = '1QqAPP7ZfOh8o-60cjKbC7AtheodBwtWY2GMCcf8wMjg'
    rangeName = 'Widevine Usage!A4:A4'
    date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    values = [
    [(date)]
    ]
    body = {
    'values': values
    }
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId,range=rangeName,
                valueInputOption='USER_ENTERED',body=body).execute()

if __name__ == '__main__':
    main()
