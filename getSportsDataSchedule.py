import requests
import json
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key

for year in [2013,2014,2015]:

    # get tournament schedule from Sports Data
    sports_data_key = 'd6aw46aafm49s5xyc2bj8vwr'
    full_request_string = 'http://api.sportsdatallc.org/golf-t1/schedule/pga/' + str(year) + '/tournaments/schedule.json?api_key=' + sports_data_key
    r = requests.get(full_request_string)
    schedule = r.json()
    schedule = json.dumps(schedule)

    # save schedule to AWS S3
    c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
    b = c.get_bucket('public.tenthtee')
    k = Key(b)
    k.key = 'sportsData/' + str(year) + '/schedule.json'
    k.set_contents_from_string(schedule)
    
    time.sleep(5)
    print str(year) + ': OK'