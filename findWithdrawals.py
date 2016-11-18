import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key


tournament = 'RBC Heritage'
tournament_link = 'rbc-heritage'
year = 2015

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

# get current field list
k1 = Key(b)
k1.key = 'field/' + str(year) + '/' + tournament + '/field'
old_field = k1.get_contents_as_string()
old_field = json.loads(old_field)


link = 'http://www.pgatour.com/tournaments/' + tournament_link + '/field.html'

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
        


# check if withdrawals file exists
withdrawals_key = 'withdrawals'
k2 = Key(b)
k2.key = withdrawals_key
withdrawals = k2.get_contents_as_string()
    
withdrawals = json.loads(withdrawals)
print withdrawals
if withdrawals['tournament'] != tournament:
    withdrawals = {}
    withdrawals['tournament'] = tournament
    withdrawals['players'] = []

for player in old_field:
    if player not in field:
        withdrawals['players'].append(player)
        
print withdrawals
withdrawals = json.dumps(withdrawals)

k = Key(b)
k.key = 'withdrawals'
k.set_contents_from_string(withdrawals)
k.make_public() 

k1 = Key(b)
k1.key = 'withdrawals/' + str(year) + '/' + tournament + '/withdrawals'
k1.set_contents_from_string(withdrawals)


field = json.dumps(field)
k = Key(b)
k.key = 'field'
k.set_contents_from_string(field)
k.make_public() 