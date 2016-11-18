import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

from boto.s3.connection import S3Connection
from boto.s3.key import Key



year = 2015
tournament = 'RBC Heritage'
tournament_link = 'rbc-heritage'

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

request_string = 'https://s3.amazonaws.com/public.tenthtee/vv/raw_salaries.csv'
salaries = pd.read_csv(request_string)


k = Key(b)
k.key = 'playerData/vvToPgaMapping'
player_map = k.get_contents_as_string()
player_map = json.loads(player_map)


k = Key(b)
k.key = 'playerData/playerList'
player_list = k.get_contents_as_string()


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
        
print "field:", len(field)


salaries_order = []
salaries_map = {}
salaries_map['tournament'] = tournament

for index,row in salaries.iterrows():
    pga_name = player_map['players'][row[' First Name'] + ' ' + row[' Last Name']]
    salary = row[' Salary']
    cleaned_salary = int(salary[1:])
    salaries_map[pga_name] = cleaned_salary
    if pga_name in field:
        salaries_order.append(pga_name)

salaries_map['order'] = salaries_order
salaries_map = json.dumps(salaries_map)

k2 = Key(b)
k2.key = 'vv/salaries'
k2.set_contents_from_string(salaries_map)
k2.make_public()

k3 = Key(b)
k3.key = 'vv/' + str(year) + '/' + tournament + '/salaries'
k3.set_contents_from_string(salaries_map)