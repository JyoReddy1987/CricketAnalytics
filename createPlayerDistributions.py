import requests
import json
import pandas as pd
import numpy as np
import random
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key


tournament_name = 'World Golf Championships - Cadillac Championship'
year = 2015
timestamp = time.time()


# returns [mean,variance] for the hole
# takes adjusted_distribution Series
def calculate_dk_parameters(adjusted_distribution, par):
    
    mean = 0
    variance = 0
    
    for score in xrange(8):
        if (score + 1) - par == 0:
            points = .5
        elif (score + 1) - par == 1:
            points = -.5
        elif (score + 1) - par > 1:
            points = -1
        elif (score + 1) - par == -1:
            points = 3
        elif (score + 1) - par < -1:
            points = 8
            
        mean += points * adjusted_distribution.tolist()[score]

    for score in xrange(8):
        if (score + 1) - par == 0:
            points = .5
        elif (score + 1) - par == 1:
            points = -.5
        elif (score + 1) - par > 1:
            points = -1
        elif (score + 1) - par == -1:
            points = 3
        elif (score + 1) - par < -1:
            points = 8
        
        variance += pow((points - mean),2) * adjusted_distribution.tolist()[score]
        
    
    return [mean,variance]


def calculate_mean(hole_distribution):

    running_total = 0
    for score in range(hole_distribution.index[0],hole_distribution.index[len(hole_distribution)-1] + 1):
        if score in hole_distribution.index:
            running_total = running_total + score * hole_distribution.get_value(score)
                     
    return running_total



def shift_distribution_mean(score_distribution,mean,target):
    
    # remember: underlying score distribution is altered.  Ok since pulling course distribution from file
    
    # find non-zero values above and below the score distribution
    temp_distribution = score_distribution[score_distribution > 0]
    
    #print temp_distribution
    upper = temp_distribution[temp_distribution.index > target]
    upper_avg = calculate_mean(upper)
    upper_sum = sum(upper)
    
    lower = temp_distribution[temp_distribution.index < target]
    lower_avg = calculate_mean(lower)
    #lower_sum = sum(lower)
    
    pct_change = (lower_avg - target + target * upper_sum) / (target * upper_sum - upper_avg)  # >1 for increase, < 1 decrease
    
    # change score distribution.  new distribution sum will be greater than zero for shift up, less than zero for shift down
    for score in range(upper.index[0], upper.index[0] + len(upper)):
        score_distribution[score] = score_distribution[score] * pct_change
    
    # normalize to 1    
    score_distribution = score_distribution / sum(score_distribution)
    
    # print score_distribution
    # print sum(score_distribution)
        
    return score_distribution





# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


# get field from first round tee times
k = Key(b)
k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/field.json'
field_string = k.get_contents_as_string()
field = json.loads(field_string) 
#print field


# get hole stats to get the pars
k1 = Key(b)
k1.key = 'sportsData/' + str(year-1) + '/' + 'WGC Cadillac Championship' + '/hole_stats.json'
hole_stats = k1.get_contents_as_string()
hole_stats = json.loads(hole_stats)
print hole_stats['rounds'][0]['cources'][0]['holes'][0]['par']

# get hole distribution(s)
k2 = Key(b)
if tournament_name == 'World Golf Championships - Cadillac Championship':
    k2.key = 'sportsData/' + str(year-1) + '/WGC Cadillac Championship/scores.json'
else:
    k2.key = 'sportsData/' + str(year-1) + '/' + tournament_name + '/scores.json'
    
scores_string = k2.get_contents_as_string()
scores = json.loads(scores_string) 


courses = scores['courses']


# if only one course, use that course for all rounds
if len(courses) == 1:
    print 'test'

for player in field:
    player_distribution = {}
    player_distribution['player'] = player
    player_distribution['status'] = 'Not started'
    player_distribution['timestamp'] = timestamp
    player_distribution['thru'] = 0  # create only the holes that will need to be simulated

        
    player_distribution['scoreMean'] = 0
    player_distribution['scoreVariance'] = 0
    
    player_distribution['dkMean'] = 0    
    player_distribution['dkVariance'] = 0    

    player_distribution['Rd1'] = {}
    player_distribution['Rd1']['teetime'] = 0
    player_distribution['Rd1']['starthole'] = 0
    player_distribution['Rd1']['course'] = courses[0]
    player_distribution['Rd1']['holes'] = {}
    for hole_num in xrange(1,18+1):
        player_distribution['Rd1']['holes'][hole_num] = {}
        player_distribution['Rd1']['holes'][hole_num]['percentages'] = []        
        for score in xrange(1,8+1):
            player_distribution['Rd1']['holes'][hole_num]['percentages'].append(scores[courses[0]]['holes'][str(hole_num)]['percentages'][str(score)])

    player_distribution['Rd2'] = {}
    player_distribution['Rd2']['course'] = courses[0]
    player_distribution['Rd2']['teetime'] = 0
    player_distribution['Rd2']['starthole'] = 0
    player_distribution['Rd2']['holes'] = {}
    for hole_num in xrange(1,18+1):
        player_distribution['Rd2']['holes'][hole_num] = {}
        player_distribution['Rd2']['holes'][hole_num]['percentages'] = []
        for score in xrange(1,8+1):
            player_distribution['Rd2']['holes'][hole_num]['percentages'].append(scores[courses[0]]['holes'][str(hole_num)]['percentages'][str(score)])

    player_distribution['Rd3'] = {}
    player_distribution['Rd3']['course'] = courses[0]
    player_distribution['Rd3']['teetime'] = 0
    player_distribution['Rd3']['starthole'] = 0
    player_distribution['Rd3']['holes'] = {}
    for hole_num in xrange(1,18+1):
        player_distribution['Rd3']['holes'][hole_num] = {}
        player_distribution['Rd3']['holes'][hole_num]['percentages'] = []
        for score in xrange(1,8+1):
            player_distribution['Rd3']['holes'][hole_num]['percentages'].append(scores[courses[0]]['holes'][str(hole_num)]['percentages'][str(score)])
    
    player_distribution['Rd4'] = {}
    player_distribution['Rd4']['course'] = courses[0]
    player_distribution['Rd4']['teetime'] = 0
    player_distribution['Rd4']['starthole'] = 0
    player_distribution['Rd4']['holes'] = {}
    for hole_num in xrange(1,18+1):
        player_distribution['Rd4']['holes'][hole_num] = {}
        player_distribution['Rd4']['holes'][hole_num]['percentages'] = []
        for score in xrange(1,8+1):
            player_distribution['Rd4']['holes'][hole_num]['percentages'].append(scores[courses[0]]['holes'][str(hole_num)]['percentages'][str(score)])


    # get avg strokes gained for field
    k3 = Key(b)
    
    #for player in field:
    k3.key = 'AvgStrokesGained/' + str(year) + '/' + tournament_name + '/' + player
    avg_strokes_gained_string = k3.get_contents_as_string()
    avg_strokes_gained = json.loads(avg_strokes_gained_string) 
    
    
    # adjust distribution(s) for avg strokes gained
    for rd in xrange(1,4+1):
        
        rd_string = 'Rd' + str(rd)
        
        round_score = 0
        
        for hole_num in xrange(1,18+1):
            #print player_distribution[rd_string]['holes'][hole_num], sum(player_distribution[rd_string]['holes'][hole_num]) / float(len(player_distribution[rd_string]['holes'][hole_num]))
            
            current_distribution = pd.Series(player_distribution[rd_string]['holes'][hole_num]['percentages'], index=[x for x in xrange(1,8+1)])
            
            
            current_mean = calculate_mean(current_distribution)
            target_mean = current_mean - avg_strokes_gained['average_strokes_gained']
            
            
            adjusted_distribution = shift_distribution_mean(current_distribution,current_mean,target_mean)
            variance = adjusted_distribution.var()            
            
      
            
            # INSERT WEATHER, PIN PLACEMENT CHANGES HERE
            
            
            
            player_distribution[rd_string]['holes'][hole_num]['percentages'] = adjusted_distribution.tolist()
            player_distribution[rd_string]['holes'][hole_num]['mean'] = target_mean
            player_distribution[rd_string]['holes'][hole_num]['variance'] = variance
            
            
            player_distribution['dkMean'] += calculate_dk_parameters(adjusted_distribution,hole_stats['rounds'][0]['cources'][0]['holes'][hole_num - 1]['par'])[0]
            player_distribution['dkVariance'] = calculate_dk_parameters(adjusted_distribution,hole_stats['rounds'][0]['cources'][0]['holes'][hole_num - 1]['par'])[1]
            
            #print hole_num,target_mean, variance
            
            player_distribution['scoreMean'] += target_mean
            player_distribution['scoreVariance'] += variance
    
    
    print player, tournament_name, player_distribution['scoreMean'], player_distribution['scoreVariance'], player_distribution['dkMean'],player_distribution['dkVariance']
        
    player_distribution = json.dumps(player_distribution)
    
    # save player_distribution    
    k4 = Key(b)
    k4.key = 'simulationDistributions/' + str(year) + '/' + tournament_name + '/' + player
    k4.set_contents_from_string(player_distribution)
    
    k5 = Key(b)
    k5.key = 'simulationDistributions/' + str(year) + '/' + tournament_name + '/' + str(timestamp) + '/' + player
    k5.set_contents_from_string(player_distribution)

    
# adjust distribution for avg variance
# adjust distribution for wind
# adjust distribution for pressure


        # draw random numbers

        #cumulative_distribution = np.cumsum(adjusted_distribution)
        #print cumulative_distribution
    
        #r = random.random()
    
        #score = np.where(cumulative_distribution > r)[0][0] + 1 # +1 because np.where return zero-indexed array
        
        #round_score += score
        
    #print round_score    
    
#    return [player,hole,score,relation_to_par] 

# save results in aws
# five servers with different codes

# another server that tabulates fantasy scores
