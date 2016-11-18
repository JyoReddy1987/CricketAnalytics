import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

player_list = []


k1 = Key(b)
k1.key = 'sportsData/2015/schedule.json'
schedule = k1.get_contents_as_string()
schedule = json.loads(schedule)

for tournament in schedule['tournaments']:
    
    print tournament['name']
    if tournament['name'] == 'Arnold Palmer Invitational': break 
     
    #get first round tee times
    k2 = Key(b)
    k2.key = 'sportsData/2015/' + tournament['name'] + '/rounds/1/teetimes.json'
    teetimes = k2.get_contents_as_string()
    teetimes = json.loads(teetimes)

    for course_info in teetimes['round']['courses']:
        for pairing_info in course_info['pairings']:
            for player in pairing_info['players']:
                full_name = player['first_name'] + ' ' + player['last_name']
                if full_name not in player_list:
                    player_list.append(full_name)

print len(player_list)
player_list = json.dumps(player_list)

k = Key(b)
k.key = 'sportsData/playerList'
k.set_contents_from_string(player_list)
