import requests
import pandas as pd
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


request_string = 'http://pgatour.com/data/r/stats/current/02671.json'

r = requests.get(request_string)
data = r.json()

asOf = data['tours'][0]['years'][0]['lastTrnProc']['endDate']

playerIds = {}
playerIds['asOf'] = asOf

for player in data['tours'][0]['years'][0]['stats'][0]['details']:
    playerIds[player['plrNum']] = {} 
    playerIds[player['plrNum']]['firstName'] = player['plrName']['first']
    playerIds[player['plrNum']]['middleName'] = player['plrName']['middle']
    playerIds[player['plrNum']]['lastName'] = player['plrName']['last']
    
    

playerNames = {}
playerNames['asOf'] = asOf

for player in data['tours'][0]['years'][0]['stats'][0]['details']:
    playerNames[player['plrName']['first'] + ' ' + player['plrName']['last']] = player['plrNum']
     

player_list = []
for player in data['tours'][0]['years'][0]['stats'][0]['details']:
    player_list.append(player['plrName']['first'] + ' ' + player['plrName']['last'])


player_list = json.dumps(player_list)

k = Key(b)
k.key = 'playerData/playerList'
k.set_contents_from_string(player_list)


playerIds = json.dumps(playerIds)

k1 = Key(b)
k1.key = 'playerData/playerLookupById'
k1.set_contents_from_string(playerIds)

print player_list, len(player_list)
playerNames = json.dumps(playerNames)

k2 = Key(b)
k2.key = 'playerData/playerLookupByName'
k2.set_contents_from_string(playerNames)


