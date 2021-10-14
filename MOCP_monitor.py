
import logging
import requests
import json
from time import sleep


#schedule_date=datetime.datetime.now().strftime("%Y-%m-%d")

schedule_date=''
token=''
url=''
headers=''
payload=''
user_id='andrew@gruar.co.uk'
password='dogs are best'

def main():
    global token, url, headers, payload, schedule_date

    initialise()


    while True:
        process()
        for sec in range(10):
            print(sec)
            sleep(1)


def initialise():
    global token, url, headers, payload, schedule_date
    url = 'http://192.168.68.133:80/api/v1.0/MOCPilot/schedule_date'

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
            print('Schedule date = {}'.format(schedule_date))
        else:
            print('Failed status', r.status_code)
            sys.exit(1)

    logged_in = False
    url = 'http://192.168.68.133:80/api/v1.0/MOCPilot/user'
    payload = {'user_id' : 'andrew@gruar.co.uk',
               'password': 'dogs are best'}
    try:
        r = requests.get(url, json=payload)
    except:
        print('Commuication error')
    else:
        if r.status_code == 200:
            resp = r.json()
            payload=resp[0]
            body=payload['payload']
            token = body['token']
            print('Logged in')
        else:
            print('Failed status', r.status_code)
            sys.exit(1)



def process():
    global token, url, headers, payload

# for some reason the following lines do not work if done prior to process interation

    url='http://192.168.68.133:80/api/v1.0/MOCPilot/schedule_job'
    headers = {'user' : user_id,
               'token' : token}

    payload = {'schedule_date': schedule_date}
    try:
        r = requests.get(url, headers=headers, json=payload)
    except:
        print('Commuication error')
        return False
    else:
        if r.status_code == 200:
            resp = r.json()
            payload=resp[0]
            for i in payload:
                print('{}{}{} - {}'.format(i['system'], i['suite'], i['job'], i['status']))
                sleep(1)
        else:
            print('Failed status', r.status_code)


    return
    
if __name__ == "__main__":
    main()