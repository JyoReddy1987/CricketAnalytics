import requests
import pandas as pd
import datetime

from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

year = 2015
tournament = 'Waste Management Phoenix Open'


api_key = 'cd6050d9c85f335fa14af7e9996e01cf'

lat = 33.6378
lng = -111.9106

request_string = 'https://api.forecast.io/forecast/' + api_key + '/' + str(lat) + ',' + str(lng)


r = requests.get(request_string)

data = r.json()

times = []
temps = []
apparent_temps = []
precip_probabilities = []
wind_speeds = []
wind_bearings = []
humidities = []


for i in xrange(len(data['hourly']['data'])):

    time = data['hourly']['data'][i]['time']
    time = datetime.datetime.fromtimestamp(time)
    times.append(time)
    temp = data['hourly']['data'][i]['temperature']
    temps.append(temp)
    apparent_temperature = data['hourly']['data'][i]['apparentTemperature']
    apparent_temps.append(apparent_temperature)
    precip_probability = data['hourly']['data'][i]['precipProbability']
    precip_probabilities.append(precip_probability)
    wind_speed = data['hourly']['data'][i]['windSpeed']
    wind_speeds.append(wind_speed)
    wind_bearing = data['hourly']['data'][i]['windBearing']
    wind_bearings.append(wind_bearing)
    humidity = data['hourly']['data'][i]['humidity']
    humidities.append(humidity)
    

df = pd.DataFrame(temps,columns=['temperature'],index=times)
df['apparent_temperature'] = apparent_temps
df['precip_probability'] = precip_probabilities
df['wind_speed'] = wind_speeds
df['wind_bearing'] = wind_bearing
df['humidity'] = humidities



k = Key(b)
k.key = str(year) + '/' + tournament + '/currentWeather.csv'
k.set_contents_from_string(df)
k.make_public()
