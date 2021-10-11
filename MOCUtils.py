import calendar
import datetime
import MOCPsettings
import mysql.connector
import requests

days=["MON","TUE","WED","THU","FRI","SAT","SUN"]
days_month=[31,28,31,30,31,30,31,31,30,31,30,31]

def date_properties(date):
    properties=['EVERYDAY']
    
    in_date=datetime.datetime.strptime(date, "%Y-%m-%d")
    property="DAY" + str(in_date.day)
    properties.append(property)
    
    property="MONTH" + str(in_date.month)
    properties.append(property)
    
    property=days[in_date.weekday()]
    properties.append(property)

    if in_date.weekday() < 5:
        property="WEEKDAY"
    else:
        property="WEEKEND"
    properties.append(property)

    if in_date.day == 1:
        properties.append("FIRST")

    if in_date.day < 8:
        property="FIRST" + days[in_date.weekday()]
        properties.append(property)
        
    no_days=days_month[in_date.month-1]
    
    if calendar.isleap(in_date.year) and in_date.month==2:
        no_days=29
    if in_date.day == no_days:
        properties.append("LAST")
        
    if  in_date.day > no_days - 7 :
        property="LAST" + days[in_date.weekday()]
        properties.append(property)
        
    return properties
    
def get_schedule_date():
    url = 'http://192.168.68.133:5000/api/v1.0/MOCP/schedule_date'

    try:
        r = requests.get(url)
    except:
        print('Commuication error')
    else:
        if r.status_code == 200:
            resp = r.json()
            payload=resp[0]
            body=payload['payload']
            schedule_date = body['schedule_date']
            return str(schedule_date)
        else:
            return 'Not defined'

    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')
                                  
def insert_log_entry(entry, user, token):

    url='http://192.168.68.133:5000/api/v1.0/MOCP/log'
    headers = {'user_id' : user,
               'token' : token}

    payload = {'system' : entry['system'],
               'suite': entry['suite'],
               'job' : entry['job'],
               'job_id' : entry['job_id'],
               'action' : entry['action'],
               'schedule_date': entry['schedule_date'],
               'schedule_status' : entry['schedule_status']}
    try:
        r = requests.post(url, headers=headers, json=payload)
    except:
        print('Commuication error')
        return 500
    else:
        return 201

