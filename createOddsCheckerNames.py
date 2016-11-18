import requests
import json
import time
from bs4 import BeautifulSoup

from boto.s3.connection import S3Connection
from boto.s3.key import Key


tournament_string = 'valero-texas-open'
tournament = 'Valero Texas Open'
year = 2015

time_string = time.time()


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')



# get OddsChecker data
odds_string = 'http://www.oddschecker.com/golf/' + tournament_string + '/winner'
r = requests.get(odds_string)

soup = BeautifulSoup(r.text)
print soup


odds_table = soup.find(id='betting-odds')
odds_table_container = odds_table.find(class_='tabs')
print odds_table_container

odds_names = []

for row in odds_table:

    player_id = row['data-participant-id']
    print player_id
    player_name = row.find(class_='selTxt')['data-name']
    print player_name
    odds_names.append(player_name)
        
odds_names = json.dumps(odds_names)

k3 = Key(b) 
k3.key = 'playerData/oddscheckerNames'
k3.set_contents_from_string(odds_names)
    