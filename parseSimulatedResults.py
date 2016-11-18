import json
import pandas as pd
import numpy as np
import scipy.stats as ss
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')


tournament_name = 'World Golf Championships - Cadillac Championship'
year = 2015
num_trials = 100


timestamp = time.time()

# get field from first round tee times
k = Key(b)
k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/field.json'
field_string = k.get_contents_as_string()
field = json.loads(field_string) 

players = []
scores = []

#for trial in xrange(num_trials):
for player in field:
    
    k1 = Key(b)
    k1.key = 'simulationResults/' + str(year) + '/' + tournament_name + '/' + player
    simulated_results = k1.get_contents_as_string()
    simulated_results = json.loads(simulated_results)

    scores.append(simulated_results['tournament_scores'][0])


# ranks = len(scores) - ss.rankdata(scores).astype(int)
print len(scores)
print scores

scores_series = pd.Series(scores,index=field)
# print ranks
print scores_series

#projected_results = {}
#projected_results['timestamp'] = timestamp
#
#
#
#
#
#
#projected_results = json.dumps(projected_results)
#print projected_results
#
#k2 = Key(b)
#k2.key = 'projectedResults/' + str(year) + '/' + tournament_name + '/' + player
#k2.set_contents_from_string(projected_results)




