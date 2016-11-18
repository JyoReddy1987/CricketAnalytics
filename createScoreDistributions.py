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

year = 2015

k.key = 'sportsData/' + str(year) + '/schedule.json'
schedule_string = k.get_contents_as_string()
schedule = json.loads(schedule_string)

# get tournament id
for tournament in schedule['tournaments']:
    if tournament['name'] == tournament_name:
        
        tournament_id = tournament['id']

        # uncomment line below to identify the tournament names
        # print tournament['name'],tournament['id']
        # if tournament['name'] == target_tournament: break
            
        scores = {}
        scores['tournament'] = tournament_name
        scores['id'] = tournament_id
        scores['courses'] = []
        
        k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(1) + '/scorecards.json'
        scorecards_string = k1.get_contents_as_string()
        scorecards = json.loads(scorecards_string)
    
        if 'round' not in scorecards: continue
        if 'players' not in scorecards['round']: continue     
        # create courses set
        for player in scorecards['round']['players']:
            course = player['course']['name']
            
            if course not in scores['courses']:
                scores['courses'].append(player['course']['name'])
        
        for course in scores['courses']:
                
            scores[course] = {}
            scores[course]['holes'] = {}
                
            for hole_num in xrange(1,18+1):
                scores[course]['holes'][hole_num] = {}
                scores[course]['holes'][hole_num]['scores'] = []
                scores[course]['holes'][hole_num]['occurences'] = {}
                scores[course]['holes'][hole_num]['percentages'] = {} 
        
        for rd in [1,2,3,4]:
            
            # use tournament id to get AWS scorecards
            k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/scorecards.json'
            scorecards_string = k1.get_contents_as_string()
            scorecards = json.loads(scorecards_string)          
            
            if 'round' not in scorecards: continue
            if 'players' not in scorecards['round']: continue 
            
            for player in scorecards['round']['players']:
                if player['course']['name'] == course:
                    for hole in player['scores']:
                        hole_number = hole['number']
                        scores[course]['holes'][hole_number]['scores'].append(int(hole['strokes']))
            
            for hole_num in xrange(1,18+1):
                for stroke_num in xrange(1,9):    
                    scores[course]['holes'][hole_num]['occurences'][stroke_num] = scores[course]['holes'][hole_num]['scores'].count(stroke_num)
                    scores[course]['holes'][hole_num]['percentages'][stroke_num] = float(scores[course]['holes'][hole_num]['occurences'][stroke_num]) / float(len(scores[course]['holes'][hole_number]['scores']))                                                                                
                                                                                
        # save to AWS S3
        scores = json.dumps(scores)
        k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/scores.json'
        k2.set_contents_from_string(scores)    
        
        break
