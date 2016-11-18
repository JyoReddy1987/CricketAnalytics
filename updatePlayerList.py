import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

k = Key(b)
k.key = 'playerData/playerList'
player_list = k.get_contents_as_string()
player_list = json.loads(player_list)
print len(player_list)

tournament_link = 'rbc-heritage'
link = 'http://www.pgatour.com/tournaments/' + tournament_link + '/field.html'

r = requests.get(link)
soup = BeautifulSoup(r.text)
player_table = soup.find(class_='field-table-content')
players = player_table.find_all("p")
for player in players:
    raw_name = player.text
    clean_name = raw_name.split(',')
    clean_name = clean_name[1][1:] + ' ' + clean_name[0]
    print clean_name
    if clean_name not in player_list:
        player_list.append(clean_name)
         
print len(player_list)
player_list = json.dumps(player_list)

k = Key(b)
k.key = 'playerData/playerList'
k.set_contents_from_string(player_list)
