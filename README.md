# Barcode-Checkin

--FOR ARC EMBEDDED SYSTEMS CLUB--

Project that connects to a barcode scanner, compare scan to list of IDs on google sheets, and checks in a student. 

Working sheets: 

Current ID List: https://docs.google.com/spreadsheets/d/1OZGMLB5fagiBeAG8-FHYKJ7YbWZvw7fJonjZjkVyDYI/

Current Log: https://docs.google.com/spreadsheets/d/1bpBm-T6QB6inECZl_hKLomBEZMoUAe5GaMM-yyHtoG4/

SETUP

1. Install python3.5
2. Install pip 

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py

3. Install Google Api

    pip install --upgrade google-api-python-client oauth2client

4. Install pyserial

    pip install pyserial

