import serial
import time
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] # Read and write permissions for program
SERVICE_ACCOUNT_FILE = 'service.json' 

#Wrapper class for creating serial connection to arduino
class SerialWrapper:

    def __init__(self, device):
        self.ser = serial.Serial(device, 115200)
        self.ser.flushInput()
    def sendData(self, data):
        self.ser.write(data.encode())

def main():
    ser = SerialWrapper('/dev/ttyACM0') # Connect to arduino
    SPREADSHEET_IDS = '1OZGMLB5fagiBeAG8-FHYKJ7YbWZvw7fJonjZjkVyDYI' # Spreadsheet ID for list of ids, names, and clubs
    SPREADSHEET_LOG = '1bpBm-T6QB6inECZl_hKLomBEZMoUAe5GaMM-yyHtoG4' # Spreadsheet ID for logging ids, names, and clubs
    RANGE_IDS = 'Form Responses 1!A2:D'
    RANGE_LOG = 'Sheet1!A2:D'

    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES) # Generate credentials object from service account file
    service = build('sheets', 'v4', credentials=creds) # Create service object
    IDS = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_IDS, range=RANGE_IDS).execute() # Get values from IDs spreadsheet
    
    values = IDS.get('values', [])
    if not values:
        print('no responses')
    else:
        while True:
            print("Ready")
            id = input()[-7:] # Get input from barcode scanner 
            if (re.search("\d{7}$", id, flags=re.M) != None): # Verify the ID scanned contains school ID
                for x in values:
                    if (any(id in j for j in x)): # Checks if any ID in IDS variable match scanned ID
                        s = "Welcome %s to %s!" % (x[1], x[3]) # Output to arduino
                        ser.sendData(s)

                        now = time.strftime(f'%m/%d/%Y %H:%M:%S', time.localtime()) # Gets current time and formats
                        resource = {
                            "majorDimension": "COLUMNS",
                            "values": [[now], [x[1]], [x[2]], [x[3]]] # Creates row object formatted as: Time, Name, ID, Club
                        }
                        
                        service.spreadsheets().values().append(
                            spreadsheetId=SPREADSHEET_LOG,
                            range=RANGE_LOG,
                            body=resource,
                            valueInputOption="RAW"
                        ).execute() # Append new line to LOG sheet

if __name__ == '__main__':
    main()
