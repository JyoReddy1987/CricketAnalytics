import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key


request_string = 'http://www.pgatour.com/tournaments/schedule.html'

r = requests.get(request_string)
soup = BeautifulSoup(r.text)

tournaments = soup.find_all(class_='tournament-name')

links = []

for tournament in tournaments:
    link = tournament.find('a')
    raw_link = link['href']
    cleaned_link = raw_link[:-5]
    if cleaned_link[0] != 'h':
        links.append('http://pgatour.com' + cleaned_link + '/field.html')


player_list = []


#test_link = 'http://pgatour.com/tournaments/frys-com-open/field.html'
#
#
#r = requests.get(test_link)
#soup = BeautifulSoup(r.text)
#player_table = soup.find(class_='field-table-content')
#players = player_table.find_all("p")
#for player in players:
#    raw_name = player.text
#    clean_name = raw_name.split(',')
#    clean_name = clean_name[1][1:] + ' ' + clean_name[0]
#    player_list.append(clean_name)


for link in links[:19]:
    print link
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    player_table = soup.find(class_='field-table-content')
    players = player_table.find_all("p")
    for player in players:
        raw_name = player.text
        clean_name = raw_name.split(',')
        clean_name = clean_name[1][1:] + ' ' + clean_name[0]
        if clean_name not in player_list:
            player_list.append(clean_name)
    time.sleep(1)
    
print len(player_list)

player_list = json.dumps(player_list)

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

k = Key(b)
k.key = 'playerData/playerList'
k.set_contents_from_string(player_list)
