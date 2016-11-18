import json
import math

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
    
        for rd in [1,2,3,4]:
            
            # use tournament id to get AWS scorecards  
            k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/scorecards.json'
            if k1.key not in keys: continue
            scorecards_string = k1.get_contents_as_string()
            scorecards = json.loads(scorecards_string)
    
            # use tournament id to get AWS scorecards
            k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/hole_averages.json'
            if k2.key not in keys: continue
            hole_averages_string = k2.get_contents_as_string()
            hole_averages = json.loads(hole_averages_string)
            
            if 'round' not in scorecards: continue
            if 'players' not in scorecards['round']: continue
                                                            
            variances = {}
            variances['tournament'] = tournament_name
            variances['id'] = tournament_id
            variances['round'] = rd    
            
            # create courses set
            for player in scorecards['round']['players']:
                player_name = player['first_name'] + ' ' + player['last_name']
                variances[player_name] = {}
                
                course = player['course']['name']
                variances[player_name]['course'] = course
                variances[player_name]['rd_variance'] = 0
                variances[player_name]['num_holes'] = 0
    
                for score in player['scores']:    
                    hole_num = score['number'] 
                    variances[player_name][hole_num] = {}
                    variances[player_name][hole_num]['strokes'] = score['strokes']
                    if variances[player_name][hole_num]['strokes'] == 0: continue
                    variances[player_name][hole_num]['average'] = hole_averages[course]['holes'][str(hole_num)]['average']
                    variances[player_name][hole_num]['variance'] = math.pow((float(hole_averages[course]['holes'][str(hole_num)]['average']) - float(score['strokes'])),2)
                    variances[player_name]['rd_variance'] += float(variances[player_name][hole_num]['variance'])
                    variances[player_name]['num_holes'] += 1
                    
            # save to AWS S3
            strokes_gained = json.dumps(variances)
            k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/variances.json'
            k2.set_contents_from_string(strokes_gained)    
            
            print year, tournament_name, rd
        
        break