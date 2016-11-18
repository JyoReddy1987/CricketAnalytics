import json
import requests
from boto.s3.connection import S3Connection
from boto.s3.key import Key


#forecast_api_key = '31dcf5f9692ab702c3039c19871ce464'
wunderground_api_key = '70247ac9e8c85769'

tournament_name = 'RBC Heritage'
year = 2015

thurs_date = '16'
fri_date = '17'

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')

city = 'Hilton Head'
state = 'SC'

lat = '32.1789'
lng = '-80.7431'



request_link = 'http://api.wunderground.com/api/' + wunderground_api_key + '/hourly10day/q/' + lat + ',' + lng +'.' + 'json'


print request_link

#request_link = 'https://api.forecast.io/forecast/' + forecast_api_key + '/' + lat + ',' + lng
r = requests.get(request_link)

forecast = r.json()


hourly_forecast = forecast['hourly_forecast']

forecast_results = {}
forecast_results['year'] = 2015
forecast_results['tournament'] = tournament_name
forecast_results['lat'] = lat
forecast_results['lat'] = lng
forecast_results['location'] = city + ', ' + state 
forecast_results['forecast'] = {}
forecast_results['forecast']['Thursday'] = []
forecast_results['forecast']['Friday'] = []

for hour in hourly_forecast:
    if hour['FCTTIME']['weekday_name'] == 'Thursday' and hour['FCTTIME']['mday'] == thurs_date:
        if int(hour['FCTTIME']['hour']) > 6 and int(hour['FCTTIME']['hour']) < 21:
            hour_group = {}
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
            hour_group['day'] = hour['FCTTIME']['mday']

            forecast_results['forecast']['Thursday'].append(hour_group)

    elif hour['FCTTIME']['weekday_name'] == 'Friday' and hour['FCTTIME']['mday'] == fri_date:
        if int(hour['FCTTIME']['hour']) > 6 and int(hour['FCTTIME']['hour']) < 21:
            hour_group = {}
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
            hour_group['day'] = hour['FCTTIME']['mday']

            forecast_results['forecast']['Friday'].append(hour_group)


early_late_total_wind = 0
early_late_num_hours = 0
late_early_total_wind = 0
late_early_num_hours = 0


for hour_group in forecast_results['forecast']['Thursday']:
    if hour_group['hour'] in ['7','8','9','10','11','12','13']:
        early_late_total_wind += float(hour_group['wind_speed'])
        early_late_num_hours += 1
    if hour_group['hour'] in ['14','15','16','17','18','19','20']:
        late_early_total_wind += float(hour_group['wind_speed'])
        late_early_num_hours += 1

for hour_group in forecast_results['forecast']['Friday']:
    if hour_group['hour'] in ['7','8','9','10','11','12','13']:
        late_early_total_wind += float(hour_group['wind_speed'])
        late_early_num_hours += 1
    if hour_group['hour'] in ['14','15','16','17','18','19','20']:
        early_late_total_wind += float(hour_group['wind_speed'])
        early_late_num_hours += 1


forecast_results['early_late_average'] = early_late_total_wind / early_late_num_hours
forecast_results['late_early_average'] = late_early_total_wind / late_early_num_hours

difference = forecast_results['early_late_average'] - forecast_results['late_early_average']
percent_difference = difference * .6

forecast_results['early_late_cut_percentage'] = 50 - percent_difference 
forecast_results['late_early_cut_percentage'] = 50 + percent_difference

print forecast_results['forecast']['Thursday']
print forecast_results['early_late_cut_percentage']

forecast_results = json.dumps(forecast_results)


k = Key(b)
k.key = 'weather/forecast'
k.set_contents_from_string(forecast_results)
k.make_public()
    
k1 = Key(b)
k1.key = 'weather/' + str(year) + '/' + tournament_name + '/forecast'
k1.set_contents_from_string(forecast_results)
k1.make_public()
