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

    home_dir = os.path.expanduser('~')
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

def updateSheets(spreadsheetId, range, valueInputOption, body):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http, discoveryServiceUrl=discoveryUrl)
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=range, valueInputOption=valueInputOption, body=body)
    response = request.execute()
    
    pprint(response)

def getSheets(spreadsheetId, range):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http, discoveryServiceUrl=discoveryUrl)
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range, valueRenderOption='FORMATTED_VALUE')
    response = request.execute()
    return response
     
def main():
    spreadsheetId = '1TcmtvfiyRDC7mjPbOZNhcIeqBJGqasBf6bA5EnCbUoI'

    get_range_fairplay = 'FairPlay!B4:B4'
    getResponse = getSheets(spreadsheetId, get_range_fairplay)
    pprint(getResponse)
    total_fairplay_num = int(getResponse['values'][0][0])
    
    get_range_widevine = 'Widevine!B4:B4'
    getResponse = getSheets(spreadsheetId, get_range_widevine)
    pprint(getResponse)
    total_widevine_num = float(getResponse['values'][0][0])

    update_range = 'Total!B4:D4'
    valueInputOption = 'USER_ENTERED'
    values = [
        [total_widevine_num, total_fairplay_num, total_fairplay_num + total_widevine_num]
    ]
    body = {
        'values': values
    }
    updateSheets(spreadsheetId, update_range, valueInputOption, body)

if __name__ == '__main__':
    main()
