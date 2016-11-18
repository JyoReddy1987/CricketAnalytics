import json
import time
import requests
from bs4 import BeautifulSoup

from boto.s3.connection import S3Connection
from boto.s3.key import Key

year = 2015
tournament_string = 'at-t-pebble-beach-national-pro-am'
tournament_name = 'AT&T Pebble Beach National Pro-Am'

c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
b = c.get_bucket('public.tenthtee')
k = Key(b)
k1 = Key(b)


k.key = 'field.json'
old_field_string = k.get_contents_as_string()
old_field = json.loads(old_field_string)

rs = b.list()
keys = []

for key in rs:
    keys.append(key.name)
   
if 'withdrawals.json' in keys: 
    k1.key = 'withdrawals.json'
    old_withdrawals = k1.get_contents_as_string()
    old_withdrawals = json.loads(old_withdrawals)
else:
    old_withdrawals = []


request_string = "http://www.pgatour.com/tournaments/" + tournament_string + "/field.html"
field_text = requests.get(request_string)
soup = BeautifulSoup(field_text.text)

players = []

field_table = soup.find(class_='field-table-content')
for player in field_table.find_all('p'):
    rearranged_name = (player.text).split(',')[1][1:] + ' ' + (player.text).split(',')[0]
    players.append(rearranged_name)


field = json.dumps(players)
k.key = 'field/' + str(year) + '/' + tournament_name + '/field.json'
k.set_contents_from_string(field) 
k1.key = 'field.json'
k1.set_contents_from_string(field)       



for player in old_field:
    if player not in players:
        print player,"withdraws"
        old_withdrawals.append(player)
    


withdrawals = json.dumps(old_withdrawals)
k.key = 'field/' + str(year) + '/' + tournament_name + '/withdrawals.json'
k.set_contents_from_string(withdrawals) 
k1.key = 'withdrawals.json'
k1.set_contents_from_string(withdrawals)       
k1.make_public()

