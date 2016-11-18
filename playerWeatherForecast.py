import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import datetime

from boto.s3.connection import S3Connection
from boto.s3.key import Key


tournament = 'RBC Heritage'
tournament_string = 'rbc-heritage'
year = 2015
hours_offset = 4


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')


# get tee times

k1 = Key(b)
k1.key = 'sportsData/' + str(year) + '/' + tournament + '/rounds/1/teetimes.json'
rd1_tee_times = k1.get_contents_as_string()
rd1_tee_times = json.loads(rd1_tee_times)


k2 = Key(b)
k2.key = 'sportsData/' + str(year) + '/' + tournament + '/rounds/2/teetimes.json'
rd2_tee_times = k2.get_contents_as_string()
rd2_tee_times = json.loads(rd2_tee_times)


def find_windspeed_average(day,rd,time,forecast):
    return 1


# get field
def get_pga_tour_field(tournament_string):
    
    link = 'http://www.pgatour.com/tournaments/' + tournament_string + '/field.html'

    field = []

    r = requests.get(link) 
    soup = BeautifulSoup(r.text)
    player_table = soup.find(class_='field-table-content')
    players = player_table.find_all("p")
    
    for player in players:
        raw_name = player.text
        clean_name = raw_name.split(',')
        clean_name = clean_name[1][1:] + ' ' + clean_name[0]
        field.append(clean_name)
        
    return field



def get_pga_to_sportsdata_map():
    # get current pgatosportsdata mapping
    k1 = Key(b)
    k1.key = 'playerData/pgaToSportsDataMapping'
    current_map = k1.get_contents_as_string()
    
    pga_to_sportsdata_map = json.loads(current_map)
    
    return pga_to_sportsdata_map



field = get_pga_tour_field(tournament_string)
pga_to_sportsdata_map = get_pga_to_sportsdata_map()



player_forecast = {}
player_forecast['tournament'] = tournament
player_forecast['players'] = {}


# get forecast
k2 = Key(b)
k2.key = 'weather/forecast'
forecast = k2.get_contents_as_string()
forecast = json.loads(forecast)

print forecast

for player in field:
    
    player_forecast['players'][player] = {}
    
    for course_info in rd1_tee_times['round']['courses']:
        for pairings_info in course_info['pairings']:
            for player_info in pairings_info['players']:
                sd_name = player_info['first_name'] + ' ' + player_info['last_name']
                tee_time = datetime.datetime.strptime(pairings_info['tee_time'],"%Y-%m-%dT%H:%M:%S+00:00")
                tee_time = tee_time - datetime.timedelta(hours=hours_offset)
                
                winds = []
                
                if tee_time.minute > 30:
                    starting_hour = tee_time.hour + 1
                else:
                    starting_hour = tee_time.hour
                
                for i in xrange(5):
                    playing_time = starting_hour + i
                    lookup_time = playing_time - 7
                    winds.append(float(forecast['forecast']['Thursday'][lookup_time]['wind_speed']))    
                                        
                tee_time = tee_time.strftime("%I:%M %p")
                
                if sd_name == pga_to_sportsdata_map['players'][player]:
                    player_forecast['players'][player]['Rd1'] = tee_time
                    player_forecast['players'][player]['Rd1 Winds'] = sum(winds) / float(len(winds))
                    
    
    for course_info in rd2_tee_times['round']['courses']:
        for pairings_info in course_info['pairings']:
            for player_info in pairings_info['players']:
                sd_name = player_info['first_name'] + ' ' + player_info['last_name']
                tee_time = datetime.datetime.strptime(pairings_info['tee_time'],"%Y-%m-%dT%H:%M:%S+00:00")
                tee_time = tee_time - datetime.timedelta(hours=hours_offset)
                
                winds = []
                
                if tee_time.minute > 30:
                    starting_hour = tee_time.hour + 1
                else:
                    starting_hour = tee_time.hour
                
                for i in xrange(5):
                    playing_time = starting_hour + i
                    lookup_time = playing_time - 7
                    winds.append(float(forecast['forecast']['Friday'][lookup_time]['wind_speed']))    
                                        
                tee_time = tee_time.strftime("%I:%M %p")
                
                if sd_name == pga_to_sportsdata_map['players'][player]:
                    player_forecast['players'][player]['Rd2'] = tee_time
                    player_forecast['players'][player]['Rd2 Winds'] = sum(winds) / float(len(winds))
                    
                    player_forecast['players'][player]['Rd1+2 Winds'] = (player_forecast['players'][player]['Rd1 Winds'] + player_forecast['players'][player]['Rd2 Winds']) / 2.0
    
print player_forecast

player_forecast = json.dumps(player_forecast)

k = Key(b)
k.key = 'weather/playerForecast'
k.set_contents_from_string(player_forecast)
k.make_public()

k1 = Key(b)
k1.key = 'weather/' + str(year) + '/' + tournament + '/playerForecast'
k1.set_contents_from_string(player_forecast)
