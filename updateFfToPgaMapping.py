import pandas as pd
import json
import difflib

from boto.s3.connection import S3Connection
from boto.s3.key import Key



year = 2015
tournament = 'RBC Heritage'

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

request_string = 'https://s3.amazonaws.com/public.tenthtee/ff/raw_salaries.csv'
df = pd.read_csv(request_string)



k = Key(b)
k.key = 'playerData/playerList'
player_list = k.get_contents_as_string()

player_list = json.loads(player_list)


# get current DK to PGA player mapping
k1 = Key(b)
k1.key = 'playerData/ffToPgaMapping'
player_map = k1.get_contents_as_string()

player_map = json.loads(player_map)


player_map['asOfTournament'] = tournament
player_map['asOfYear'] = 2015


for index,row in df.iterrows():
    player = row['PLAYER']
    if player not in player_list:
        print player, difflib.get_close_matches(player,player_list)
        if player == 'Fredrik Jacobson': player_map['players'][player] = 'Freddie Jacobson'
        if player == 'Seung-yul Noh': player_map['players'][player] = 'Seung-Yul Noh'
        if player == 'Sung-Joon Park': player_map['players'][player] = 'Sung Joon Park'
        if player == 'Gonzalo Fernandez-Castano': player_map['players'][player] = 'Gonzalo Fdez-Castano'
    elif player in player_map.keys(): continue
    else:
        player_map['players'][player] = player
        
print player_map
player_map = json.dumps(player_map)


k2 = Key(b)
k2.key = 'playerData/ffToPgaMapping'
k2.set_contents_from_string(player_map)
