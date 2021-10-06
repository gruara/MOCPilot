import json
import requests
import datetime as dt
#from sense_hat import SenseHat
from sense_hat import SenseHat

BASE_URL = "http://datapoint.metoffice.gov.uk/public/data/"
API_KEY="aae7b832-12fd-4c67-8b51-c1427c72da40"
weather_types = [
                'Clear night',
                'Sunny day',
                'Partly Cloudy(night)',
                'Partly Cloudy(day)',
                'undefined',
                'Mist',
                'Fog',
                'Cloudy',
                'Overcast',
                'Light rain Shower(night)',
                'Light rain Shower(day)',
                'Drizzle',
                'Light rain',
                'Heavy rain shower(night)',
                'Heavy rain shower(day)',
                'Heavy rain',
                'Sleet shower(night)',
                'Sleet shower (day)',
                'Sleet',
                'Hail shower(night)',
                'Hail shower (day)',
                'Hail',
                'Light snow shower (night)',
                'Light snow shower (day)',
                'Light snow',
                'Heavy snow shower (night)',
                'Heavy snow shower (day)',
                'Heavy snow',
                'Thunder shower (night)',
                'Thunder shower (day)',
                'Thunder'          
                ]

def main():
   
    getforecast()


def getdetails():
    url = BASE_URL  + 'val/wxobs/all/json/sitelist' + '?key=' + API_KEY
    headers=""
    print(url)
    try:
        r = requests.get(url,headers=headers)
    except:
        print('Commuication error')
        return
    if r.status_code == 200:
        resp = json.loads(r.text)
    else:
        print('Failed status', r.status_code)
        return
    print(resp)
    with open('MetLocations.txt', 'w') as f:
#         f.write(r.text)
        for locations in resp:
            for location in resp[locations]:
                for y in resp[locations][location]:
                    if 'unitaryAuthArea' in y.keys():
                        area=y['unitaryAuthArea']
                    else:
                        area=''
                    dets='{:<10} {:<30} {:<20}\n'.format(y['id'], y['name'],area)
                    f.write(dets)    
            
def getforecast():
    url = BASE_URL  + 'val/wxfcs/all/json/350761' + '?res=3hourly&key=' + API_KEY
    headers=""
 #   print(url)
    try:
        r = requests.get(url,headers=headers)
    except:
        print('Commuication error')
        return
#    print(r.text)
    if r.status_code == 200:
        resp = json.loads(r.text)
    else:
        print('Failed status', r.status_code)
        return
    if 'Location' in resp['SiteRep']['DV']:
        next
    else:
        print('Forecast data not available')
        return
    forecasts=resp['SiteRep']['DV']['Location']['Period']
    today=list(forecasts)[0]
    tomorrow=list(forecasts)[1]
    now=dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    now_minutes=int(dt.datetime.now().hour) * 60 + int(dt.datetime.now().minute)#
    date=''
    time=''
    wind_direction=''
    wind_speed=''
    weather_type=''
    hour=0
    minute=0
    temperature=''
    data_date=resp['SiteRep']['DV']['dataDate']

    if now_minutes > 1260:
        check=tomorrow
        now_minutes=0
    else:
        check=today

    for rep in check['Rep']:
        if int(rep['$']) >= now_minutes:
        
            forecast=rep
            
            date=check['value']
             
            hour, minute=divmod(int(forecast['$']), 60)
            wind_direction=forecast['D']
            wind_speed=forecast['F']
            weather_type=weather_types[int(forecast['W'])]
            temperature=forecast['T']
            break


#    sense = SenseHat()
# Temperature censor is iut due to proximity of cpu. Adjutment factor calculated to match Nest Thermometer    
#    room_temp = sense.get_temperature() * .61


    print('{} for {} {:02d}:{:02d} - {:30} {:>3}c  wind {}mph {:3} '.format(now, date, hour, minute, weather_type, temperature,  wind_speed, wind_direction))

         
if __name__ == "__main__":
    main()

