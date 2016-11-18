import requests
import json
import time
import math

from boto.s3.connection import S3Connection
from boto.s3.key import Key

tournament_name = 'The Masters'
year = 2015

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

k.key = 'sportsData/' + str(year) + '/schedule.json'
schedule_string = k.get_contents_as_string()
schedule = json.loads(schedule_string)

# get tournament id
for tournament in schedule['tournaments']:
    
    if tournament['name'] == tournament_name:
    # uncomment line below to identify the tournament names
    # print tournament['name'],tournament['id']
    # if tournament['name'] == target_tournament: break
    
    # identify tournament to get api 
    #if tournament['name'] == tournament_name:
        
        tournament_id = tournament['id']
        print tournament_id
        
        # HOLE STATS
        sports_data_key = 'd6aw46aafm49s5xyc2bj8vwr'    
        request_string = 'http://api.sportsdatallc.org/golf-t1/hole_stats/pga/' + str(year) + '/tournaments/' + tournament_id + '/hole-statistics.json?api_key=' + sports_data_key

        r = requests.get(request_string)
        hole_stats = r.json()
        hole_stats = json.dumps(hole_stats)

        # save hole_stats to AWS S3
        k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/hole_stats.json'
        k.set_contents_from_string(hole_stats)
        print 'hole stats'
        
        # SCORECARDS
        for rd in [1,2,3,4]:
            
            # use tournament id to get round scores
            time.sleep(1)
            request_string = 'http://api.sportsdatallc.org/golf-t1/scorecards/pga/' + str(year) + '/tournaments/' + tournament_id + '/rounds/'+ str(rd) + '/scores.json?api_key=' + sports_data_key
            r = requests.get(request_string)
            scorecards = r.json()
            scorecards = json.dumps(scorecards)
    
            # save hole_stats to AWS S3
            k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/scorecards.json'
            k.set_contents_from_string(scorecards)
            time.sleep(3)
            print 'scorecards - rd ' + str(rd)
            
        
            # TEETIMES
            request_string = 'http://api.sportsdatallc.org/golf-t1/teetimes/pga/' + str(year) + '/tournaments/' + tournament_id + '/rounds/'+ str(rd) + '/teetimes.json?api_key=' + sports_data_key
            r = requests.get(request_string)
            teetimes = r.json()
            teetimes = json.dumps(teetimes)
    
    
            # save tee times to AWS S3
            k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/teetimes.json'
            k.set_contents_from_string(teetimes)
            time.sleep(3)
            print 'tee times - rd ' + str(rd)


            # HOLE AVERAGES 
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
            
            print 'hole averages - rd ' + str(rd)
            time.sleep(1)
            
            
            # STROKES GAINED
            k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/scorecards.json'
            if k1.key not in keys: continue
            scorecards_string = k1.get_contents_as_string()
            scorecards = json.loads(scorecards_string)
        
            # use tournament id to get AWS hole averages
            k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/hole_averages.json'
            if k2.key not in keys: continue
            hole_averages_string = k2.get_contents_as_string()
            hole_averages = json.loads(hole_averages_string)
            
            if 'round' not in scorecards: continue
            if 'players' not in scorecards['round']: continue
                                                            
            strokes_gained = {}
            strokes_gained['tournament'] = tournament_name
            strokes_gained['id'] = tournament_id
            strokes_gained['round'] = rd    
            
            # create courses set
            for player in scorecards['round']['players']:
                
                player_name = player['first_name'] + ' ' + player['last_name']
                strokes_gained[player_name] = {}
                
                course = player['course']['name']
                strokes_gained[player_name]['course'] = course
                strokes_gained[player_name]['rd_strokes_gained'] = 0
                strokes_gained[player_name]['num_holes'] = 0
        
                for score in player['scores']:    
                    hole_num = score['number'] 
                    strokes_gained[player_name][hole_num] = {}
                    strokes_gained[player_name][hole_num]['strokes'] = float(score['strokes'])
                    if strokes_gained[player_name][hole_num]['strokes'] == 0: continue
                    strokes_gained[player_name][hole_num]['average'] = float(hole_averages[course]['holes'][str(hole_num)]['average'])
                    strokes_gained[player_name][hole_num]['strokes_gained'] = float(hole_averages[course]['holes'][str(hole_num)]['average']) - float(score['strokes'])
                    strokes_gained[player_name]['rd_strokes_gained'] += float(strokes_gained[player_name][hole_num]['strokes_gained']) 
                    if player_name == 'Will MacKenzie':
                        print player_name, hole_num, score['strokes'],hole_averages[course]['holes'][str(hole_num)]['average'], strokes_gained[player_name][hole_num]['strokes_gained'], strokes_gained[player_name]['rd_strokes_gained']
                    strokes_gained[player_name]['num_holes'] += 1
                if player_name == 'Rory McIlroy':
                    print "rd_strokes_gained: ", rd, strokes_gained[player_name]['rd_strokes_gained']
                    
                # save to AWS S3
            strokes_gained = json.dumps(strokes_gained)
            k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/strokes_gained.json'
            k2.set_contents_from_string(strokes_gained)
            print 'strokes gained - rd ' + str(rd)
            time.sleep(1)
            
            # VARIANCES  
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
            
            print 'variances - rd ' + str(rd)
            time.sleep(1)
        
            print year, tournament_name, rd
            time.sleep(1)
                       
                       
        # SCORE DISTRIBUTION
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
        
        print 'score distributions'    
            
            

        # STROKES GAINED BY TOURNAMENT  
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
                    
        # save to AWS S3
        strokes_gained = json.dumps(strokes_gained)
        k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/strokes_gained.json'
        k2.set_contents_from_string(strokes_gained)    
        print 'strokes gained by tournament'
        
        # VARIANCES BY TOURNAMENT 
        k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/1/scorecards.json'
        if k1.key not in keys: continue
        scorecards_string = k1.get_contents_as_string()
        scorecards = json.loads(scorecards_string)
        
        variances = {}
        variances['tournament'] = tournament_name
        variances['id'] = tournament_id
        
        if 'players' not in scorecards['round']: continue
        
        # create courses set
        for player in scorecards['round']['players']:
            
            player_name = player['first_name'] + ' ' + player['last_name']
            variances[player_name] = {}
            variances[player_name]['tournament_variance'] = 0
            variances[player_name]['tournament_num_holes'] = 0
            
            for rd in [1,2,3,4]:
            
                # use tournament id to get AWS scorecards  
                k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/variances.json'
                if k1.key not in keys: continue
                rd_strokes_gained = k1.get_contents_as_string()
                rd_strokes_gained = json.loads(rd_strokes_gained)
                
                if player_name not in rd_strokes_gained: continue
                
                variances[player_name]['tournament_variance'] += float(rd_strokes_gained[player_name]['rd_variance'])
                variances[player_name]['tournament_num_holes'] += float(rd_strokes_gained[player_name]['num_holes'])
                
            #print player_name,variances[player_name]['tournament_variances'], variances[player_name]['tournament_num_holes']
    
        # save to AWS S3
        strokes_gained = json.dumps(variances)
        k2.key = 'sportsData/' + str(year) + '/' + tournament_name + '/variances.json'
        k2.set_contents_from_string(strokes_gained)
        print 'variance by tournament'    