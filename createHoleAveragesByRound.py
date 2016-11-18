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

sports_data_key = 'd6aw46aafm49s5xyc2bj8vwr' 


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
            scorecards_string = k1.get_contents_as_string()
            scorecards = json.loads(scorecards_string)
        
            if 'round' not in scorecards: continue
            if 'players' not in scorecards['round']: continue
            
            hole_averages = {}
            hole_averages['tournament'] = tournament_name
            hole_averages['id'] = tournament_id
            hole_averages['round'] = rd
            hole_averages['courses'] = []
            
            # create courses set
            for player in scorecards['round']['players']:
                course = player['course']['name']
                
                if course not in hole_averages['courses']:
                    hole_averages['courses'].append(player['course']['name'])
                    
            print hole_averages['courses']
            
            for course in hole_averages['courses']:
                
                hole_averages[course] = {}
                hole_averages[course]['holes'] = {}
                
                for hole_num in xrange(1,18+1):
                    hole_averages[course]['holes'][hole_num] = {}
                    hole_averages[course]['holes'][hole_num]['total_strokes'] = 0                
                    hole_averages[course]['holes'][hole_num]['num_players'] = 0
        
                for player in scorecards['round']['players']:
                    if player['course']['name'] == course:
                        for hole in player['scores']:
                            hole_number = hole['number']
                            hole_averages[course]['holes'][hole_number]['total_strokes'] += int(hole['strokes'])                
                            hole_averages[course]['holes'][hole_number]['num_players'] += 1
                
                for hole_num in xrange(1,18+1):
                    hole_averages[course]['holes'][hole_num]['average'] = float(hole_averages[course]['holes'][hole_num]['total_strokes']) / float(hole_averages[course]['holes'][hole_num]['num_players'])
            
            # save to AWS S3
            hole_averages = json.dumps(hole_averages)
            k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/hole_averages.json'
            k2.set_contents_from_string(hole_averages)    
            
            time.sleep(1)
            print year, tournament_name, rd
        break