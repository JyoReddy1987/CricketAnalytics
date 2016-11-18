import json
import time
import requests
from bs4 import BeautifulSoup

from boto.s3.connection import S3Connection
from boto.s3.key import Key

year = 2015
tournament_name = 'World Golf Championships - Cadillac Championship' 


c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
b = c.get_bucket('public.tenthtee')
k = Key(b)


#request_string = "http://www.pgatour.com/tournaments/" + tournament_string + "/field.html"
#field_text = requests.get(request_string)
#soup = BeautifulSoup(field_text.text)
#
#pgaTour_players = []
#
#field_table = soup.find(class_='field-table-content')
#for player in field_table.find_all('p'):
#    rearranged_name = (player.text).split(',')[1][1:] + ' ' + (player.text).split(',')[0]
#    pgaTour_players.append(rearranged_name)


k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(1) + '/teetimes.json'
teetimes = k.get_contents_as_string()
# get first round tee times from 

teetimes = json.loads(teetimes)


sportsData_players = []

#print teetimes['round']['courses'][0]['pairings'][0]['players'][0]

for course_index in xrange(len(teetimes['round']['courses'])):
    for pairings_index in xrange(len(teetimes['round']['courses'][course_index]['pairings'])):
         for player in teetimes['round']['courses'][course_index]['pairings'][pairings_index]['players']:
             full_name = player['first_name'] + ' ' + player['last_name']
             sportsData_players.append(full_name)

             #if full_name not in pgaTour_players: print full_name

sportsData_players = json.dumps(sportsData_players)


k1 = Key(b)
k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/field.json'
k1.set_contents_from_string(sportsData_players)

#print sportsData_players
#for player in pgaTour_players:
#    if player not in sportsData_players: print player