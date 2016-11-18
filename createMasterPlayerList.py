import json
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key


# get tournament schedule from AWS
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
b = c.get_bucket('public.tenthtee')
k = Key(b)
k1 = Key(b)
k2 = Key(b)


master_player_list = []

rs = b.list()
keys = []
for key in rs:
    keys.append(key.name)


for year in [2013,2014,2015]:
    k.key = 'sportsData/' + str(year) + '/schedule.json'
    schedule_string = k.get_contents_as_string()
    schedule = json.loads(schedule_string)

    # get tournament id
    for tournament in schedule['tournaments']:
        # uncomment line below to identify the tournament names
        # print tournament['name'],tournament['id']
        # if tournament['name'] == target_tournament: break
        
        tournament_name = tournament['name']
        tournament_id = tournament['id']
    
        scores = {}
        scores['tournament'] = tournament_name
        scores['id'] = tournament_id
        scores['courses'] = []
        
        k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(1) + '/scorecards.json'
        if k1.key not in keys: continue
        scorecards_string = k1.get_contents_as_string()
        scorecards = json.loads(scorecards_string)
    
        if 'round' not in scorecards: continue
        if 'players' not in scorecards['round']: continue     
        
        for player in scorecards['round']['players']:
    
            player_name = player['first_name'] + ' ' + player['last_name']
            
            if player_name not in master_player_list:
                master_player_list.append(player_name)

        print year, tournament_name                                

# save to AWS S3
master_player_list = json.dumps(master_player_list)
k2.key = 'sportsData/master_player_list.json'
k2.set_contents_from_string(master_player_list)    
