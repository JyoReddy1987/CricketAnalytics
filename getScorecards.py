import requests
import json
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key

tournament_name = 'Northern Trust Open'

# get tournament schedule from AWS
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
b = c.get_bucket('public.tenthtee')
k = Key(b)

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
    if tournament['name'] == tournament_name:
        tournament_id = tournament['id']

        for rd in [1,2,3,4]:
            # use tournament id to get round scores
            request_string = 'http://api.sportsdatallc.org/golf-t1/scorecards/pga/' + str(year) + '/tournaments/' + tournament_id + '/rounds/'+ str(rd) + '/scores.json?api_key=' + sports_data_key
            r = requests.get(request_string)
            scorecards = r.json()
            scorecards = json.dumps(scorecards)
    
            # save hole_stats to AWS S3
            k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/' + str(rd) + '/scorecards.json'
            k.set_contents_from_string(scorecards)
        
            time.sleep(3)
            print year, tournament_name, rd
        
        break