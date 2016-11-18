import json
import difflib
import requests
from bs4 import BeautifulSoup

from boto.s3.connection import S3Connection
from boto.s3.key import Key


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


tournament_string = 'houston-open'
year = 2015
tournament = 'Shell Houston Open'



k = Key(b)
k.key = 'playerData/playerList'
player_list = k.get_contents_as_string()
player_list = json.loads(player_list)


player_map = {}
player_map['asOfTournament'] = tournament
player_map['asOfYear'] = 2015
player_map['players'] = {}


odds_string = 'http://www.oddschecker.com/golf/' + tournament_string + '/winner'
r = requests.get(odds_string)

#soup = BeautifulSoup(r.text)
soup = BeautifulSoup(r.text, "html.parser")


odds_table = soup.find_all(class_='eventTableRow')

for row in odds_table:

    player_id = row['data-participant-id']
    player_name = row.find(class_='selTxt')['data-name']
    if player_name not in player_list: 
        # player_name = player_lookup[player_name]
        print player_name, difflib.get_close_matches(player_name,player_list)
        if player_name == 'J B Holmes': player_map['players'][player_name] = 'J.B. Holmes'
        elif player_name == 'Graham Delaet': player_map['players'][player_name] = 'Graham DeLaet'
        elif player_name == 'Fredrik Jacobson': player_map['players'][player_name] = 'Freddie Jacobson'
        elif player_name == 'K J Choi': player_map['players'][player_name] = 'K.J. Choi'
        elif player_name == 'D A Points': player_map['players'][player_name] = 'D.A. Points'
        elif player_name == 'Andrew Landry': player_map['players'][player_name] = 'Andrew Landry'
        elif player_name == 'J J Henry': player_map['players'][player_name] = 'J.J. Henry'
        elif player_name == 'SK Park': player_map['players'][player_name] = 'S.J. Park'
    else:
        player_map['players'][player_name] = player_name


player_map = json.dumps(player_map)

k2 = Key(b)
k2.key = 'playerData/oddsToPgaMapping'
k2.set_contents_from_string(player_map)