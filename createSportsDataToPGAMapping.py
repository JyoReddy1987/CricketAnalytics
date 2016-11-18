import json
import difflib

from boto.s3.connection import S3Connection
from boto.s3.key import Key


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')



# get sportsData player list
k1 = Key(b)
k1.key = 'sportsData/playerList'
sd_player_list = k1.get_contents_as_string()
sd_player_list = json.loads(sd_player_list)

# get PGA player list
k2 = Key(b)
k2.key = 'playerData/playerList'
pga_player_list = k1.get_contents_as_string()
pga_player_list = json.loads(pga_player_list)


player_map = {}
player_map['asOfTournament'] = 'Valspar Championship'
player_map['asOfYear'] = 2015
player_map['players'] = {}

# create map for matching players 
for player in sd_player_list:
    if player not in pga_player_list:
        print player, difflib.get_close_matches(player,pga_player_list)
        if player == 'Davis Love': player_map['players'][player] = 'Davis Love III'
        elif player == 'Billy Hurley': player_map['players'][player] = 'Billy Hurley III'
        elif player == 'Brendon De Jonge': player_map['players'][player] = 'Brendon de Jonge'
        elif player == 'Charles Howell': player_map['players'][player] = 'Charles Howell III'
        elif player == 'Nigel Spence': player_map['players'][player] = 'Nigel P. Spence'
        elif player == 'William Lunde': player_map['players'][player] = 'Bill Lunde'
        elif player == 'Carlos Sainz': player_map['players'][player] = 'Carlos Sainz Jr'
        elif player == 'Steve Lewton': player_map['players'][player] = 'Stephen Lewton'
        elif player == 'Wen-Chong Liang': player_map['players'][player] = 'WC Liang'
        elif player == 'Fredrik Jacobson': player_map['players'][player] = 'Freddie Jacobson'
        elif player == 'Rodolfo Cazaubon': player_map['players'][player] = 'Rodolfo E. Cazaubon'
        elif player == 'Yan-wei Liu': player_map['players'][player] = 'Yan Wei Liu'
        elif player == 'Richard Johnson': player_map['players'][player] = 'Richard S. Johnson'
        elif player == 'Rafael Cabrera-Bello': player_map['players'][player] = 'Rafael Cabrera Bello'
        
    else:
        player_map['players'][player] = player
        
print player_map

# get PGA player list
player_map = json.dumps(player_map)

k3 = Key(b)
k3.key = 'playerData/sportsDataToPgaMapping'
pga_player_list = k3.set_contents_from_string(player_map)
