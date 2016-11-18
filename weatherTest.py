import forecastio
import datetime
import pandas as pd
import numpy as np
import requests

#forecast_api_key = '31dcf5f9692ab702c3039c19871ce464'
wunderground_api_key = '70247ac9e8c85769'

tournament_name = 'Shell Houston Open'

city = 'Houston'
state = 'Texas'

lat = '29.7604'
lng = '-95.3698'



request_link = 'http://api.wunderground.com/api/' + wunderground_api_key + '/hourly10day/q/' + lat + ',' + lng +'/' + 'json'

print request_link

#request_link = 'https://api.forecast.io/forecast/' + forecast_api_key + '/' + lat + ',' + lng
r = requests.get(request_link)

forecast = r.json()

hourly_forecast = forecast['hourly_forecast']
print hourly_forecast
wind_forecast = []

hour_group = {}
for hour in hourly_forecast:
    hour_group['wind_direction'] = hour['wdir']['degrees']
    hour_group['wind_direction_code'] = hour['wdir']['dir']
    hour_group['wind_speed'] = hour['wspd']['english']
    hour_group['weekday_name'] = hour['FCTTIME']['weekday_name']
    hour_group['year'] = hour['FCTTIME']['year']
    hour_group['month_name'] = hour['FCTTIME']['month_name']
    hour_group['hour'] = hour['FCTTIME']['hour']
    hour_group['time_zone'] = hour['FCTTIME']['tz']
    hour_group['temperature'] = hour['temp']['english']
    hour_group['time'] = hour['FCTTIME']['civil']
    hour_group['condition'] = hour['condition']

wind_forecast.append(hour_group)    