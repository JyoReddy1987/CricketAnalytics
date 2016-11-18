import requests
import pandas as pd
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

request_string = 'https://s3.amazonaws.com/public.tenthtee/dk/contest-standings-4161803.csv' 

df = pd.read_csv(request_string)

new_player_list = []

for index, row in df.iterrows():

    if type(row['Lineup']) != float: 
        lineup_array = row['Lineup'].split(',')
    
        for i in xrange(len(lineup_array)): 
        
            player = lineup_array[i][4:]
            if player not in new_player_list:
                new_player_list.append(player)

print new_player_list
print len(new_player_list)   

new_player_list1 = json.dumps(new_player_list)

k = Key(b)
k.key = 'dk/playerList'
k.set_contents_from_string(new_player_list1)
k.make_public()

