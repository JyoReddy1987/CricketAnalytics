import requests
import json
import time
from bs4 import BeautifulSoup

from boto.s3.connection import S3Connection
from boto.s3.key import Key


tournament_string = 'rbc-heritage'
tournament = 'RBC Heritage'
year = 2015

time_string = time.time()


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


k1 = Key(b)
k1.key = 'playerData/oddsToPgaMapping'
player_map = k1.get_contents_as_string()
player_map = json.loads(player_map)


#k2 = Key(b) 
#k2.key = 'playerData/playerLookupByName'
#player_list = k2.get_contents_as_string()
#player_list = json.loads(player_list)
#players = []
#for key in player_list.keys():
#    players.append(key)


k3 = Key(b) 
k3.key = 'playerData/oddscheckerNames'
player_lookup = k3.get_contents_as_string()
player_lookup = json.loads(player_lookup)


odds_string = 'http://www.oddschecker.com/golf/' + tournament_string + '/winner'

r = requests.get(odds_string)


soup = BeautifulSoup(r.text, "html.parser")

oddsData = {}
oddsData['asOf'] = time_string
oddsData['tournament'] = tournament
oddsData['odds'] = {}

odds_table = soup.find_all(class_='eventTableRow')

total_probability = 0

max_odds = 0

for row in odds_table:

    player_id = row['data-participant-id']
    player_name = row.find(class_='selTxt')['data-name']
        
    betfair_id = player_id + '_BF'
    betfair_string = row.find('td', {"id": betfair_id}).get_text()
    
    if betfair_string == '':
        odds = 0.0
        betfair_probability = 0.0
    elif '/' in betfair_string:
        split_strings = betfair_string.split('/')
        odds = float(split_strings[0]) / float(split_strings[1])
        betfair_probability = 1 / odds
    else: 
        odds = float(betfair_string)
        betfair_probability = 1 / odds  
    
    betdaq_id = player_id + '_BD'
    betdaq_string = row.find('td', {"id": betdaq_id}).get_text()

    if betdaq_string == '':
        odds = 0.0
        betdaq_probability = 0.0
    elif '/' in betdaq_string:
        split_strings = betdaq_string.split('/')
        odds = float(split_strings[0]) / float(split_strings[1])
        betdaq_probability = 1 / odds
    else: 
        odds = float(betdaq_string)
        betdaq_probability = 1 / odds    
        
        
    if betdaq_probability == 0.0 and betfair_probability == 0.0:
        combined_probability = 0.0
    elif betdaq_probability == 0.0 and betfair_probability != 0.0:
        combined_probability = betfair_probability
    elif betdaq_probability != 0.0 and betfair_probability == 0.0:
        combined_probability = betdaq_probability
    else:
        combined_probability = (betfair_probability + betdaq_probability) / 2

    total_probability += combined_probability
    if total_probability == 0: total_probability = 1
    
    oddsData['odds'][player_map['players'][player_name]] = combined_probability
 
for player in oddsData['odds'].keys():
    oddsData['odds'][player] = oddsData['odds'][player] / total_probability
    if oddsData['odds'][player] > max_odds: max_odds = oddsData['odds'][player]

oddsData['odds']['max_odds'] = max_odds                  
print max_odds
                                                                 
if oddsData['odds'] != []:
    oddsData = json.dumps(oddsData)  
  
        
    k = Key(b)
    k.key = 'oddsData.json'
    k.set_contents_from_string(oddsData)
    k.make_public()
    #
    k2 = Key(b)
    k2.key = 'archive/' +  str(year) + '/' + tournament + '/' + str(time_string) + '/oddsData.json'
    k2.set_contents_from_string(oddsData)
    k2.make_public()
 
    