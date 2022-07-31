import calendar
import datetime
import MOCPsettings
import mysql.connector
import requests

days=["MON","TUE","WED","THU","FRI","SAT","SUN"]
months=["","JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
days_month=[31,28,31,30,31,30,31,31,30,31,30,31]


def date_properties(date):
    properties=['EVERYDAY']
    
    properties.append(date)
    
    in_date=datetime.datetime.strptime(date, "%Y-%m-%d")
    property="DAY" + str(in_date.day)
    properties.append(property)
    
    property="MONTH" + str(in_date.month)
    properties.append(property)
    
    property=months[in_date.month]
    properties.append(property)
    
    property="{}{}".format(months[in_date.month],str(in_date.day))
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
        if days[in_date.weekday()] == 'SUN':
            if int(in_date.month) == 3:
                properties.append("BSTSTART")
            elif int(in_date.month) == 10:
                properties.append("BSTEND")
#    problems processing json for below url                
#    url = 'https://www.gov.uk/bank-holidays.json'
    
    url = 'https://date.nager.at/api/v3/publicholidays/{}/GB'.format(in_date.year) 
    try:
        r = requests.get(url)
    except:
        print('Commuication error')
    else:
        resp=[]
        resp = r.json()
        for bh in resp:
            if date == bh['date']:
                if not bh['counties']:
                    properties.extend(["BHOLEW","BHOLSC","BHOLNI"])
                else:
                    regions = bh['counties']
                    for region in regions:
                        if region == 'GB-SCT':
                            properties.append("BHOLSC")
                        elif region == 'GB-NIR':
                            properties.append("BHOLNI")
                        elif region == 'GB-ENG':
                            properties.append("BHOLEW")
 
        
    return properties
    
def get_schedule_date():

    url = 'http://pi4-1:80/api/v1.0/MOCPilot/schedule_date'

     
    try:
        r = requests.get(url)
    except:
        print('Commuication error')
    else:
        if r.status_code == 200:
            resp = r.json()
 
            schedule_date = resp[0]['schedule_date']
            return str(schedule_date)
        else:
            return 'Not defined'

"""     cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot') """
                                  
def insert_log_entry(entry, user, token):

    url='http://pi4-1:5000/api/v1.0/MOCP/log'
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

