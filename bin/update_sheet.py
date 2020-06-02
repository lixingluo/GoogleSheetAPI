from __future__ import print_function
import httplib2
import os
import logging
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
# Use for internal shell script
import subprocess

BIN = '/opt/googleapis/bin'

def getCredentials():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API WideWine UpdateSheet'

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    home_dir = os.path.expanduser("~")
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
        print('Sotring credentials to ' + credential_path)
    
    return credentials

def updateSheetValues(spreadsheetId,rangeName,body):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,
                valueInputOption='USER_ENTERED', body=body).execute()

def getLicenseValues():
    statistics_date = input("Please input date (e.g. 2020-05-25): ")
    logging.info(f"Checking license for date: {statistics_date}")
    check_license_path = os.path.join(BIN, 'chk_wv_license.sh')
    check_license_output = subprocess.check_output([check_license_path, str(statistics_date)])
    check_license_arr = check_license_output.decode().split('\n')
    return check_license_arr

def setLogs():
    log_dir = os.path.join(BIN, 'Logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(filename=os.path.join(log_dir, 'log.txt'), level=logging.DEBUG)

def main():
    setLogs()
    l = getLicenseValues()
    spreadsheetId = '1QqAPP7ZfOh8o-60cjKbC7AtheodBwtWY2GMCcf8wMjg'
    rangeName = 'Widevine Usage!I4:M' # For wv1,2,3,4 -- I4:M N4:R S4:W X4:AB
    values = [
    [l[0],l[1],l[2],l[3],l[4]]
    ]
    body = {
    'values': values
    }
    updateSheetValues(spreadsheetId,rangeName,body)

if __name__ == '__main__':
    main()
