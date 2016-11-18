import json
import pandas as pd
import numpy as np
import random
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')


tournament_name = 'World Golf Championships - Cadillac Championship'
year = 2015
num_trials = 10000


timestamp = time.time()


# get field from first round tee times
k = Key(b)
k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/field.json'
field_string = k.get_contents_as_string()
field = json.loads(field_string) 


for player in field:

    # get player_distribution    
    k1 = Key(b)
    k1.key = 'simulationDistributions/' + str(year) + '/' + tournament_name + '/' + player
    player_distribution = k1.get_contents_as_string()
    player_distribution = json.loads(player_distribution)
    
    #print player, player_distribution['scoreMean'], player_distribution['scoreVariance']
    
    simulated_results = {}
    simulated_results['timestamp'] = timestamp
    
    
    # only simulate the holes that need to be simulated
    if player_distribution['status'] == 'Not started':
        
        unrounded_scores = np.random.normal(player_distribution['scoreMean'],player_distribution['scoreVariance'],num_trials).tolist()
        simulated_results['tournament_scores'] = [round(score) for score in unrounded_scores]
        
        raw_dk_scores = np.random.normal(player_distribution['dkMean'],player_distribution['dkVariance'],num_trials).tolist()
        simulated_results['dk_scores'] = [round(score,1) for score in raw_dk_scores]
        
        # save results
        simulated_results = json.dumps(simulated_results)
        
        k2 = Key(b)
        k2.key = 'simulationResults/' + str(year) + '/' + tournament_name + '/' + player
        k2.set_contents_from_string(simulated_results)
        
        k3 = Key(b)
        k3.key = 'simulationResults/' + str(year) + '/' + tournament_name + '/' + str(timestamp) + '/' + player
        k3.set_contents_from_string(simulated_results)
    
    print player
        
    #    
    #    for rd in xrange(1,4+1):
    #                     
    #        rd_string = 'Rd' + str(rd)
    #        
    #        simulated_results[rd_string] = {}
    #        simulated_results[rd_string]['course'] = player_distribution[rd_string]['course']
    #        simulated_results[rd_string]['holes'] = {}
    #        
    #        for hole_num in xrange(1,18+1):
    #                        
    #            simulated_results[rd_string]['holes'][hole_num] = {}
    #            simulated_results[rd_string]['holes'][hole_num]['score'] = []
    #            simulated_results[rd_string]['holes'][hole_num]['dkScore'] = []
    #
    #            adjusted_distribution = pd.Series(player_distribution[rd_string]['holes'][str(hole_num)], index=[x for x in xrange(1,8+1)])
    #            
    #            cumulative_distribution = np.cumsum(adjusted_distribution)
    #    
    #            for trial in xrange(num_trials):
    #                
    #                r = random.random()    
    #                score = np.where(cumulative_distribution > r)[0][0] + 1  #+1 because np.where return zero-indexed array
    #                print hole_num, trial, score
    #                # simulated_results[rd_string]['holes'][hole_num]['score'].append(str(score)) 
    #                
    #                simulated_results['tournament_scores'][trial] += score
    #                # get hole points for fantasy outcome
    #                
    #    
    #    # save results
    #    simulated_results = json.dumps(simulated_results)
    #    
    #    k2 = Key(b)
    #    k2.key = 'simulationResults/' + str(year) + '/' + tournament_name + '/' + player
    #    k2.set_contents_from_string(simulated_results)
    #    
    #    k3 = Key(b)
    #    k3.key = 'simulationResults/' + str(year) + '/' + tournament_name + '/' + str(timestamp) + '/' + player
    #    k3.set_contents_from_string(simulated_results)
    #
    #print player
    #    