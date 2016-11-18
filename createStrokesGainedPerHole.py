import json
import time
import requests
from bs4 import BeautifulSoup

from boto.s3.connection import S3Connection
from boto.s3.key import Key

year = 2015
tournament_name = 'World Golf Championships - Cadillac Championship' 

c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
b = c.get_bucket('public.tenthtee')
k = Key(b)


# get the field list
k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/field.json'
field_string = k.get_contents_as_string()
field = json.loads(field_string)


# get the weights
k2 = Key(b)
k2.key = 'weights/' + str(year) + '/' + tournament_name + '/' + 'weights.json'
tournament_weights = k2.get_contents_as_string()
tournament_weights = json.loads(tournament_weights)





for player in field:
    
    avg_strokes_gained = {}
    
    cumulative_strokes_gained = 0
    cumulative_variance = 0
    cumulative_holes_played = 0
    
    for tournament in tournament_weights['weights']:
       
        weight = tournament_weights['weights'][tournament]['weight']
        tournament_year = tournament_weights['weights'][tournament]['year']
        days_before = tournament_weights['weights'][tournament]['days_before']
        if days_before == 0: continue
        
        # check if player is in the first round tee times
        k3 = Key(b)
        k3.key = 'sportsData/' + str(tournament_year) + '/' + tournament + '/rounds/' + str(1) + '/teetimes.json'
        teetimes = k3.get_contents_as_string()
        teetimes = json.loads(teetimes)

        players = []

        #print teetimes['round']['courses'][0]['pairings'][0]['players'][0]

        for course_index in xrange(len(teetimes['round']['courses'])):
            if  'pairings' in teetimes['round']['courses'][course_index]:
                for pairings_index in xrange(len(teetimes['round']['courses'][course_index]['pairings'])):
                    for name in teetimes['round']['courses'][course_index]['pairings'][pairings_index]['players']:
                        full_name = name['first_name'] + ' ' + name['last_name']
                        players.append(full_name)
        
        if player not in players: continue
        
        # get the tournament strokes gained 
        k4 = Key(b)
        k4.key = 'sportsData/' + str(tournament_year) + '/' + tournament + '/strokes_gained.json'
        strokes_gained = k4.get_contents_as_string()
        strokes_gained = json.loads(strokes_gained)
        
        # print tournament_year,tournament, player, strokes_gained[player]['tournament_strokes_gained'], strokes_gained[player]['tournament_num_holes']
        cumulative_strokes_gained += strokes_gained[player]['tournament_strokes_gained'] * weight
        cumulative_holes_played += strokes_gained[player]['tournament_num_holes'] * weight
        
        # get the tournament variance 
        k5 = Key(b)
        k5.key = 'sportsData/' + str(tournament_year) + '/' + tournament + '/variances.json'
        variances = k5.get_contents_as_string()
        variances = json.loads(variances)    
        
        cumulative_variance += variances[player]['tournament_variance'] * weight
        
        
    avg_strokes_gained['cumulative_strokes_gained'] = cumulative_strokes_gained
    avg_strokes_gained['cumulative_variance'] = cumulative_variance
    avg_strokes_gained['cumulative_holes_played'] = cumulative_holes_played
    if cumulative_holes_played == 0: 
        avg_strokes_gained['average_strokes_gained'] = -0.05
        avg_strokes_gained['average_variance'] = .45
    else:
        avg_strokes_gained['average_strokes_gained'] = cumulative_strokes_gained / cumulative_holes_played
        avg_strokes_gained['average_variance'] = cumulative_variance / cumulative_holes_played
    
    print player, cumulative_strokes_gained, cumulative_variance, cumulative_holes_played, avg_strokes_gained['average_strokes_gained'], avg_strokes_gained['average_variance']

    # save individual player in order to not have to make it through the whole field without timeout...  can use keys to see if that player is already done later
    avg_strokes_gained = json.dumps(avg_strokes_gained)
    k6 = Key(b)
    k6.key = 'AvgStrokesGained/' + str(year) + '/' + tournament_name + '/' + player
    k6.set_contents_from_string(avg_strokes_gained)