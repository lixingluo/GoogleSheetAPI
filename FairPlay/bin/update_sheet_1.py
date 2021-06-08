from __future__ import print_function
import httplib2
import os
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, timedelta
import subprocess

BIN = '/opt/googleapis/bin'

def getCredentials():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API FairPlay'

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
        client_secret_dir = os.path.join(BIN, '.credentials')
        clientsecret_path = os.path.join(client_secret_dir, CLIENT_SECRET)
        flow = client.flow_from_clientsecrets(clientsecret_path, SCOPES)
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)

    return credentials

def updateSheets(spreadsheetId, rangeName, valueInputOption, body):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, 
                valueInputOption=valueInputOption, body=body).execute()

def getLicenseValues(dateTo):
    check_license_path = os.path.join(BIN, 'chk_fp_license.sh')
    check_license_output = subprocess.check_output([check_license_path, str(dateTo)])
    check_license_arr = check_license_output.decode().split('\n')
    return check_license_arr

def main():
    dateTo = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
    spreadsheetId = '1TcmtvfiyRDC7mjPbOZNhcIeqBJGqasBf6bA5EnCbUoI'
    rangeName = 'FairPlay!D4:D4' # fairplay 1,2  D4:D4, E4:E4
    valueInputOption = 'USER_ENTERED'
    l = getLicenseValues(dateTo)
    values = [
        [l[0]]
    ]
    body = {
        'values': values
    }
    updateSheets(spreadsheetId, rangeName, valueInputOption, body)

if __name__ == '__main__':
    main()

