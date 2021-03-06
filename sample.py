from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os
from datetime import datetime, timedelta

scopes = ['https://www.googleapis.com/auth/calendar']
calendarId='nicolealderite@gmail.com'

def login():
    print("Please login to your user.")
    try:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret_749445591810-p0b8c8k58uc8v3jfr1g964qf017mnsho.apps.googleusercontent.com.json", scopes=scopes)
        credentials = flow.run_console()
        pickle.dump(credentials, open("token.pkl", "wb"))
        print("Login finished")
        print("")
    except:
        login()

def buildCalendarService():
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar","v3",credentials=credentials)
    return service
    
    
def displayEvents(service, calendarId):
#calendar_list_entry = service.calendarList().get(calendarId='nicolealderite@gmail.com').execute()
    #print(calendar_list_entry['summary'])
    result = service.events().list(calendarId=calendarId, timeZone="Asia/Manila").execute()
    for event in result['items']:
        start = event.get('start')
        end = event.get('end')
        print("=======================================================================")
        print(" Event Title: " + str(event.get('summary')))
        print(" Location: " + str(event.get('location')))
        #print(" Description: " + str(event.get('description')))
        if start:
            print(" Start Time: " + str(start.get('dateTime')))
            print(" End Time: " + str(end.get('dateTime')))
            print(" Timezone: " + str(end.get('timeZone')))
        #print(" Link: " + str(event.get('htmlLink')))
        print("=======================================================================")
     #print(result)
    
def logout():
    os.remove("token.pkl")
    
def createEvent(service, calendarId):
    timeZone = 'Asia/Manila'
    print("Event start time: ")
    summary = input("Event Title: ")
    location = input("Event Location: ")
    description = input("Description: ")
    year = input("Year: ")
    month = input("Month: ")
    day = input("Day: ")
    hour = input("Hour: ")
    minute = input("Minute: ")
    minutes = input("How many minutes the event will be ?")
    start_time = datetime[year, month, day, hour, minute, 0]
    end_time = start_time + timedelta(minutes=minutes)
    
    event = {
        'summary': str(summary),
        'description': str(description),
        'location': str(location),
        'start': {
            'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'), 
            'timeZone': str(timeZone)
        },
        'end': {
            'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': timeZone
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24*60},
                {'method': 'popup', 'minutes': 10}
            ]
        }
    }
    
    service.events().insert(calendarId=calendarId, body=event).execute()
    
def menu(service, calendarId):
    appIsOn = True;
    while appIsOn:
        print("MENU:")
        print("1 --> List Calendar items")
        print("2 --> Insert new calendar item")
        print("3 --> Login to new user")
        print("4 --> Exit app")

        choice = input("Please select an option:")
        print("")

        if choice == "1":
            displayEvents(service, calendarId)
        elif choice == "2":
            createEvent(service, calendarId)
        elif choice == "3":
            logout()
            main()
        elif choice == "4":
            print("Exiting app...")
            appIsOn = False;
        else:
            print("Please select only a valid option.")
            
        print("")
    
def main():
    
    try:
        service = buildCalendarService()
    except:
        login()
        service = buildCalendarService()
    menu(service, calendarId)
 
main()