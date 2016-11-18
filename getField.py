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
        
print field
print len(field)
field = json.dumps(field)

k = Key(b)
k.key = 'field'
k.set_contents_from_string(field)
k.make_public() 

k1 = Key(b)
k1.key = 'field/' + str(year) + '/' + tournament + '/field'
k1.set_contents_from_string(field)

