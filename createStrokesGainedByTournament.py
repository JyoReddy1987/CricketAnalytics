import json
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key

tournament_name = 'Northern Trust Open'


# get tournament schedule from AWS
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
b = c.get_bucket('public.tenthtee')
k = Key(b)
k1 = Key(b)
k2 = Key(b)

rs = b.list()
keys = []

for key in rs:
    keys.append(key.name)

year = 2015
k.key = 'sportsData/' + str(year) + '/schedule.json'
schedule_string = k.get_contents_as_string()
schedule = json.loads(schedule_string)

# get tournament id
for tournament in schedule['tournaments']:
    # uncomment line below to identify the tournament names
    # print tournament['name'],tournament['id']
    # if tournament['name'] == target_tournament: break
    if tournament_name == tournament['name']:
        tournament_id = tournament['id']
        
        # use tournament id to get AWS scorecards  
        k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/1/scorecards.json'
        if k1.key not in keys: continue
        scorecards_string = k1.get_contents_as_string()
        scorecards = json.loads(scorecards_string)
        
        strokes_gained = {}
        strokes_gained['tournament'] = tournament_name
        strokes_gained['id'] = tournament_id
        
        if 'players' not in scorecards['round']: continue
        
        # create courses set
        for player in scorecards['round']['players']:
            
            player_name = player['first_name'] + ' ' + player['last_name']
            strokes_gained[player_name] = {}
            strokes_gained[player_name]['tournament_strokes_gained'] = 0
            strokes_gained[player_name]['tournament_num_holes'] = 0
            
            for rd in [1,2,3,4]:
            
                # use tournament id to get AWS scorecards  
                k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/strokes_gained.json'
                if k1.key not in keys: continue
                rd_strokes_gained = k1.get_contents_as_string()
                rd_strokes_gained = json.loads(rd_strokes_gained)
                
                if player_name not in rd_strokes_gained: continue
                
                strokes_gained[player_name]['tournament_strokes_gained'] += float(rd_strokes_gained[player_name]['rd_strokes_gained'])
                strokes_gained[player_name]['tournament_num_holes'] += float(rd_strokes_gained[player_name]['num_holes'])
                
            print player_name,strokes_gained[player_name]['tournament_strokes_gained'], strokes_gained[player_name]['tournament_num_holes']
    
        # save to AWS S3
        strokes_gained = json.dumps(strokes_gained)
        k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/strokes_gained.json'
        k2.set_contents_from_string(strokes_gained)    
        
        print year, tournament_name
        break