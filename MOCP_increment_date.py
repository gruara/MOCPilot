import MOCPsettings
import requests

import sys
from MOCUtils import get_schedule_date
from datetime import datetime, timedelta
from time import sleep


def main():
# sleep for 5 minutes before running to ensure next days schedule is not loaded until after Pilot start of day    
    sleep(300)
    schedule_date=get_schedule_date()
    if schedule_date == 'Not defined':
        print('Schedule date not defined')
        sys.exit(1)
    date = datetime.strptime(schedule_date, "%Y-%m-%d")
    date = date + timedelta(days=1)
    modified_date = datetime.strftime(date, "%Y-%m-%d")

    url='http://pi4-1/api/v1.0/MOCPilot/schedule_date'
    headers = {'user' : MOCPsettings.system_user_id,
               'token' : MOCPsettings.system_token}

    payload = {'schedule_date': modified_date}
    try:
        r = requests.put(url, headers=headers, json=payload)
    except:
        print('Commuication error')
        return False
    else:
        print(modified_date)


if __name__ == "__main__":
    main()