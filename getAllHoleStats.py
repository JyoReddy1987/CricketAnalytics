import requests
import json
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key



# get tournament schedule from AWS
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
b = c.get_bucket('public.tenthtee')
k = Key(b)

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
    
        # use tournament id to get hole_stats
        sports_data_key = 'd6aw46aafm49s5xyc2bj8vwr'    
        request_string = 'http://api.sportsdatallc.org/golf-t1/hole_stats/pga/' + str(year) + '/tournaments/' + tournament_id + '/hole-statistics.json?api_key=' + sports_data_key

        r = requests.get(request_string)
        hole_stats = r.json()
        hole_stats = json.dumps(hole_stats)

        # save hole_stats to AWS S3
        k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/hole_stats.json'
        k.set_contents_from_string(hole_stats)
        
        time.sleep(5)
        print year, tournament_name
