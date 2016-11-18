import requests
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key



tournament_api_key = '1wbznily'



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')



api_link = 'https://www.kimonolabs.com/api/' + tournament_api_key + '?apikey=ceefe87da4a927adca3d3428bd0b49b9'


r = requests.get(api_link)

data = r.json()


oddsData = {}

oddsData['asOf'] = data['lastsuccess']

oddsData['odds'] = []

odds_total = 0

for player_data in data['results']['collection1']:
    player = player_data['Player']['text']
    
    if '/' in player_data['Betdaq']: 
        betdaq_odds = player_data['Betdaq'].split('/')
        betdaq_odds = float(betdaq_odds[0]) / float(betdaq_odds[1]) 
    elif player_data['Betdaq'] == None or player_data['Betdaq'] == '':
        betdaq_odds = 0
    else:
        betdaq_odds = float(player_data['Betdaq'])
    
    if '/' in player_data['Betfair']: 
        betfair_odds = player_data['Betfair'].split('/')
        betfair_odds = float(betfair_odds[0]) / float(betfair_odds[1]) 
    elif player_data['Betfair'] == None or player_data['Betfair'] == '':
        betfair_odds = 0
    else:
        betfair_odds = float(player_data['Betfair'])
    
    if (betfair_odds == 0) or (betdaq_odds == 0): 
        average_odds = 0
        probability = 0
    else:    
        average_odds = (betfair_odds + betdaq_odds) / 2
        probability = 1 / average_odds

        
    oddsData['odds'].append({'player': player, 'probability':probability})

    odds_total += probability

normalizing_sum = odds_total

for player_group in oddsData['odds']:
    player_group['probability'] = player_group['probability'] / normalizing_sum


oddsData = json.dumps(oddsData)


k = Key(b)
k.key = 'oddsData.json'
k.set_contents_from_string(oddsData)
k.make_public()