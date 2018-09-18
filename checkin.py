import serial
import time
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service.json'

class SerialWrapper:

    def __init__(self, device):
        self.ser = serial.Serial(device, 115200)
        self.ser.flushInput()
    def sendData(self, data):
        self.ser.write(data.encode())

def main():
    ser = SerialWrapper('/dev/ttyACM0')
    SPREADSHEET_IDS = '1OZGMLB5fagiBeAG8-FHYKJ7YbWZvw7fJonjZjkVyDYI'
    SPREADSHEET_LOG = '1bpBm-T6QB6inECZl_hKLomBEZMoUAe5GaMM-yyHtoG4'
    RANGE_IDS = 'Form Responses 1!A2:D'
    RANGE_LOG = 'Sheet1!A2:D'

    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    IDS = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_IDS, range=RANGE_IDS).execute()
    
    values = IDS.get('values', [])
    if not values:
        print('no responses')
    else:
        while True:
            print("Ready")
            id = input()[-7:]
            if (re.search("\d{7}$", id, flags=re.M) != None):
                for x in values:
                    if (any(id in j for j in x)):
                        s = "Welcome %s to %s!" % (x[1], x[3])
                        ser.sendData(s)

                        now = time.strftime(f'%m/%d/%Y %H:%M:%S', time.localtime())
                        resource = {
                            "majorDimension": "COLUMNS",
                            "values": [[now], [x[1]], [x[2]], [x[3]]]
                        }
                        
                        service.spreadsheets().values().append(
                            spreadsheetId=SPREADSHEET_LOG,
                            range=RANGE_LOG,
                            body=resource,
                            valueInputOption="RAW"
                        ).execute()

if __name__ == '__main__':
    main()
