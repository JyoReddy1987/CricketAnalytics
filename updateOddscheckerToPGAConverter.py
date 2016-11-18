import requests
import pandas as pd
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from bs4 import BeautifulSoup


tournament_string = 'honda-classic'


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')



k2 = Key(b) 
k2.key = 'playerData/playerLookupByName'
player_list = k2.get_contents_as_string()
player_list = json.loads(player_list)
players = []
for key in player_list.keys():
    players.append(key)

# print players   


name_map = {}


# get OddsChecker data
odds_string = 'http://www.oddschecker.com/golf/' + tournament_string + '/winner'
r = requests.get(odds_string)

soup = BeautifulSoup(r.text)
odds_table = soup.find_all(class_='eventTableRow')
for row in odds_table:

    player_id = row['data-participant-id']
    player_name = row.find(class_='selTxt')['data-name']
    if player_name not in players:
        if player_name == 'J B Holmes': name_map[player_name] = 'J.B. Holmes'
        elif player_name == 'Graham Delaet': name_map[player_name] = 'Graham DeLaet'
        elif player_name == 'K J Choi': name_map[player_name] = 'K.J. Choi'
        elif player_name == 'D A Points': name_map[player_name] = 'D.A. Points'
        else: name_map[player_name] = player_name
        
name_map = json.dumps(name_map)

k2 = Key(b)
k2.key = 'playerData/oddscheckerNames'
k2.set_contents_from_string(name_map)
            
                
                    
                            
