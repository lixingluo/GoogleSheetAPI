from pprint import pprint
import os
import httplib2
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

BIN = '/opt/googleapis/bin'

def getCredentials():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com.fairplay.json')
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        client_secret_dir = os.path.join(BIN, '.credentials')
        clientsecret_path = os.path.join(client_secret_dir, CLIENT_SECRET_FILE)
        flow = client.flow_from_clientsecrets(clientsecret_path, SCOPES)
        credentials = tools.run_flow(flow, store, flags)

    return credentials

def updateSheets(spreadsheetId):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http, discoveryServiceUrl=discoveryUrl)
    batch_update_spreadsheet_request_body = {
        'requests': [{
            'insertDimension': {
                'range': {
                    'sheetId': 1838004597,
                    'dimension': 'ROWS',
                    'startIndex': 3,
                    'endIndex': 4
                }
            }
        }]
    }
    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=batch_update_spreadsheet_request_body)
    response = request.execute()

    pprint(response)

def main():
    spreadsheetId = '1TcmtvfiyRDC7mjPbOZNhcIeqBJGqasBf6bA5EnCbUoI'
    updateSheets(spreadsheetId)

if __name__ == '__main__':
    main()
    
