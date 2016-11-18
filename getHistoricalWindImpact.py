import requests
import json
import datetime
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key



year = 2015
tournament_name = 'Puerto Rico Open'
timezone_offset = 5

sports_data_key = 'd6aw46aafm49s5xyc2bj8vwr' 
# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')


k = Key(b) 
k.key = 'sportsData/' + str(year) + '/schedule.json'
schedule_string = k.get_contents_as_string()
schedule = json.loads(schedule_string)


results = {}


for tournament in schedule['tournaments']:
    if tournament['name'] == tournament_name:
        
        results[tournament_name] = {}
        
        tournament_id = tournament['id']
        #city = tournament['venue']['city']
        #state = tournament['venue']['state']
        start_date = tournament['start_date']
        #print city, state, start_date
        
        #get first round tee_times
        link = 'http://api.sportsdatallc.org/golf-t1/teetimes/pga/' + str(2015) + '/tournaments/' + tournament_id + '/rounds/'+ str(1) + '/teetimes.json?api_key=' + sports_data_key
        r = requests.get(link)
        tee_times = r.json()

        time.sleep(1)

        #get third round tee_times
        link = 'http://api.sportsdatallc.org/golf-t1/teetimes/pga/' + str(2015) + '/tournaments/' + tournament_id + '/rounds/'+ str(3) + '/teetimes.json?api_key=' + sports_data_key
        r = requests.get(link)
        rd3_tee_times = r.json()
        
        made_cut_list = []
        
        for course_data in rd3_tee_times['round']['courses']:
            for pairings_data in course_data['pairings']:
                for player_data in pairings_data['players']:
                    
                    name = player_data['first_name'] + ' ' + player_data['last_name']
                    made_cut_list.append(name)
        
        print len(made_cut_list)
        
        
        # get strokes gained for first round 
        k = Key(b)
        k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/1/strokes_gained.json'
        strokes_gained_rd1 = k.get_contents_as_string()
        strokes_gained_rd1 = json.loads(strokes_gained_rd1)
        
        # get strokes gained for first round 
        k1 = Key(b)
        k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/2/strokes_gained.json'
        strokes_gained_rd2 = k1.get_contents_as_string()
        strokes_gained_rd2 = json.loads(strokes_gained_rd2)
        
                                                        
        for course_data in tee_times['round']['courses']:
            for pairings_data in course_data['pairings']:
                for player_data in pairings_data['players']:
                    
                    name = player_data['first_name'] + ' ' + player_data['last_name']
                    
                    results[tournament_name][name] = {}
                                        
                    tee_time = pairings_data['tee_time']
                    tee_time = datetime.datetime.strptime(tee_time, "%Y-%m-%dT%H:%M:%S+00:00")
                    
                    results[tournament_name][name]['rd1_tee_time'] = datetime.datetime.strftime(tee_time - datetime.timedelta(hours=5),'%H:%M')
                    if tee_time < datetime.datetime(int(start_date.split("-")[0]),int(start_date.split("-")[1]),int(start_date.split("-")[2]),10 + timezone_offset,30): results[tournament_name][name]['early-late'] = True
                    else: results[tournament_name][name]['early-late'] = False
                    
                    if name in strokes_gained_rd1.keys():                        
                        results[tournament_name][name]['rd1_strokes_gained'] = strokes_gained_rd1[name]['rd_strokes_gained']
                    else: results[tournament_name][name]['rd1_strokes_gained'] = 0
                    
                    if name in strokes_gained_rd2.keys():
                        results[tournament_name][name]['rd2_strokes_gained'] = strokes_gained_rd2[name]['rd_strokes_gained']
                    else: results[tournament_name][name]['rd2_strokes_gained'] = 0                    
      
        early_late_strokes_gained = 0
        late_early_strokes_gained = 0
        num_early_late = 0
        num_late_early = 0
                            
        for name in results[tournament_name].keys():
            if results[tournament_name][name]['early-late']:
                early_late_strokes_gained += results[tournament_name][name]['rd1_strokes_gained']
                early_late_strokes_gained += results[tournament_name][name]['rd2_strokes_gained']
                num_early_late += 1
            else: 
                late_early_strokes_gained += results[tournament_name][name]['rd1_strokes_gained']
                late_early_strokes_gained += results[tournament_name][name]['rd2_strokes_gained']
                num_late_early += 1
                
        print early_late_strokes_gained, late_early_strokes_gained, num_early_late, num_late_early
        print results
        
        break    
                     
                
            


#player_map = json.dumps(player_map)
#
#
#k2 = Key(b)
#k2.key = 'playerData/pgaToSportsDataMapping'
#k2.set_contents_from_string(player_map)