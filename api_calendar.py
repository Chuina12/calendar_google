import os
import datetime
from collections import namedtuple
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    creds = None
    working_dir = os.getcwd()
    token_dir = 'token files'
    token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json'

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)
        # with open(os.path.join(working_dir, token_dir, token_file), 'rb') as token:
        #   cred = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, token_file))
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

class Acces_token():   
    CLIENT_SECRET_FILE='token.json'
    API_NAME='calendar'
    API_VERSION='v3'
    SCOPES='https://www.googleapis.com/auth/calendar'
    
class Service_g():
    service = create_service(Acces_token.CLIENT_SECRET_FILE,Acces_token.API_NAME,Acces_token.API_VERSION,Acces_token.SCOPES)
      
      
 
def create_calendar():        
    
    summary = input('enter the summary: ')
    timeZone = input('enter the timezone, example: America/Los_Angeles : ')
    
    calendar = {
    'summary': summary,
    'timeZone': timeZone
    }
    try:
        response = Service_g.service.calendars().insert(body=calendar).execute()
        print(response)
    except:
        print("invalid timeZone")


    
    
    
# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

def create_event():
    
    # this is a default dictionnary who content the datas
    event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
    'dateTime': '2023-08-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
    },
    'end': {
    'dateTime': '2023-08-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
    },
    'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
    ],
    'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
    },
    }
    
    event = Service_g.service.events().insert(calendarId='primary', body=event).execute()
    print(event)
    
def delete_event(eventId):
    
    try:
        delete=Service_g.service.events().delete(calendarId='primary', eventId=eventId).execute()
    except:
        print('eventId is not correct !')
    print('delete success ! ')
    
   
# this function takes as input the id of an event 
def update_event(eventId):
    # First retrieve the event from the API.
    event = Service_g.service.events().get(calendarId='primary', eventId=eventId).execute()
    # default edit
    event['summary'] = 'Appointment at Somewhere'
    updated_event = Service_g.service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
# Print the updated date.
    print(updated_event['updated'])
    
    
if __name__=='__main__':
    # update_event('d8bq4apgrlbc4sdd85pgdajfag')  
    
    create_calendar()
    
