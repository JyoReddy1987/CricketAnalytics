import requests
import pandas as pd
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


tournament_code = '004'
request_string = 'http://www.pgatour.com/data/r/' + tournament_code + '/leaderboard-v2.json'

r = requests.get(request_string)
data = r.json()

pga_player_list = []

fantasyData = {} 
fantasyData['isFinished'] = data['leaderboard']['is_finished']
fantasyData['timestamp'] = data['last_updated']
fantasyData['roundNum'] = data['debug']['current_round_in_setup']
fantasyData['tournament'] = data['debug']['tournament_in_schedule_file_name']
fantasyData['roundState'] = data['leaderboard']['round_state']
fantasyData['course_data'] = {}

for course in data['leaderboard']['courses']:
    fantasyData['course_data'][course['course_id']] = {}
    fantasyData['course_data'][course['course_id']]['course_name'] = course['course_name']
    fantasyData['course_data'][course['course_id']]['course_id'] = course['course_id']

        
fantasyData['player_data'] = {}

for player_index in xrange(len(data['leaderboard']['players'])):
    
    player = data['leaderboard']['players'][player_index]['player_bio']['first_name'] + ' ' + data['leaderboard']['players'][player_index]['player_bio']['last_name']
    print player
    pga_player_list.append(player)
    fantasyData['player_data'][player] = {}
    fantasyData['player_data'][player]['player_id'] = data['leaderboard']['players'][player_index]['player_id']
    fantasyData['player_data'][player]['score'] = data['leaderboard']['players'][player_index]['total']
    fantasyData['player_data'][player]['status'] = data['leaderboard']['players'][player_index]['status']
    fantasyData['player_data'][player]['holes'] = data['leaderboard']['players'][player_index]['holes']
    fantasyData['player_data'][player]['start_hole'] = data['leaderboard']['players'][player_index]['start_hole']
    fantasyData['player_data'][player]['thru'] = data['leaderboard']['players'][player_index]['thru']
    fantasyData['player_data'][player]['dk_round_score'] = 0
    fantasyData['player_data'][player]['draftday_round_score'] = 0
    fantasyData['player_data'][player]['current_position'] = data['leaderboard']['players'][player_index]['current_position']
    fantasyData['player_data'][player]['par_performance'] = data['leaderboard']['players'][player_index]['par_performance']
    fantasyData['player_data'][player]['course_id'] = data['leaderboard']['players'][player_index]['course_id']
    
    if fantasyData['player_data'][player]['status'] == 'active':
        addForRound = (4 - fantasyData['roundNum']) * 18
        fantasyData['player_data'][player]['numHolesToGo'] = 18 - fantasyData['player_data'][player]['thru'] + addForRound
    else:
        fantasyData['player_data'][player]['numHolesToGo'] = 0

            
    fantasyData['player_data'][player]['holes'] = {}
        
    if fantasyData['player_data'][player]['status'] == 'active':
        for hole_index in xrange(18):
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']] = {}
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['par'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['par']
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['score'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['strokes']
            if data['leaderboard']['players'][player_index]['holes'][hole_index]['strokes']:
                fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['relToPar'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['strokes'] - data['leaderboard']['players'][player_index]['holes'][hole_index]['par']

                relToPar = fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['relToPar']
                if relToPar == -3: fantasyData['player_data'][player]['dk_round_score'] += 20
                elif relToPar == -2: fantasyData['player_data'][player]['dk_round_score'] += 8
                elif relToPar == -1: fantasyData['player_data'][player]['dk_round_score'] += 3
                elif relToPar == 0: fantasyData['player_data'][player]['dk_round_score'] += .5
                elif relToPar == 1: fantasyData['player_data'][player]['dk_round_score'] -= .5
                elif relToPar >= 2: fantasyData['player_data'][player]['dk_round_score'] -= 1



## save round data and then add the previous rounds
if fantasyData['roundNum'] == 1:

    for player_index in xrange(len(data['leaderboard']['players'])):
        player = data['leaderboard']['players'][player_index]['player_bio']['first_name'] + ' ' + data['leaderboard']['players'][player_index]['player_bio']['last_name']
    
        fantasyData['player_data'][player]['dk_total_score'] = fantasyData['player_data'][player]['dk_round_score']
        fantasyData['player_data'][player]['draftday_total_score'] = fantasyData['player_data'][player]['draftday_round_score']
    
        savedfantasyData = json.dumps(fantasyData)
 
        k = Key(b)
        k.key = 'archive/2015/' + fantasyData['tournament'] + '/' + str(fantasyData['roundNum']) + '/fantasyScoringData.json'
        k.set_contents_from_string(savedfantasyData)


elif fantasyData['roundNum'] == 2:

    k1 = Key(b)
    k1.key = 'archive/2015/' + fantasyData['tournament'] + '/1/fantasyScoringData.json'
    round_two_data = k1.get_contents_as_string()
    round_two_data = json.loads(round_two_data)

    for player_index in xrange(len(data['leaderboard']['players'])):
        player = data['leaderboard']['players'][player_index]['player_bio']['first_name'] + ' ' + data['leaderboard']['players'][player_index]['player_bio']['last_name']

        fantasyData['player_data'][player]['dk_total_score'] = round_two_data['player_data'][player]['dk_total_score'] + fantasyData['player_data'][player]['dk_round_score']
        fantasyData['player_data'][player]['draftday_total_score'] = round_two_data['player_data'][player]['draftday_total_score'] + fantasyData['player_data'][player]['draftday_round_score']
    
    savedfantasyData = json.dumps(fantasyData)
    
    k = Key(b)
    k.key = 'archive/2015/' + fantasyData['tournament'] + '/' + str(fantasyData['roundNum']) + '/fantasyScoringData.json'
    k.set_contents_from_string(savedfantasyData)


elif fantasyData['roundNum'] == 3:

    k1 = Key(b)
    k1.key = 'archive/2015/' + fantasyData['tournament'] + '/2/fantasyScoringData.json'
    round_two_data = k1.get_contents_as_string()
    round_two_data = json.loads(round_two_data)

    for player_index in xrange(len(data['leaderboard']['players'])):
        player = data['leaderboard']['players'][player_index]['player_bio']['first_name'] + ' ' + data['leaderboard']['players'][player_index]['player_bio']['last_name']

        fantasyData['player_data'][player]['dk_total_score'] = round_two_data['player_data'][player]['dk_total_score'] + fantasyData['player_data'][player]['dk_round_score']
        fantasyData['player_data'][player]['draftday_total_score'] = round_two_data['player_data'][player]['draftday_total_score'] + fantasyData['player_data'][player]['draftday_round_score']
    
    savedfantasyData = json.dumps(fantasyData)
    
    k = Key(b)
    k.key = 'archive/2015/' + fantasyData['tournament'] + '/' + str(fantasyData['roundNum']) + '/fantasyScoringData.json'
    k.set_contents_from_string(savedfantasyData)


# if not first round, get total score for previous round
elif fantasyData['roundNum'] == 4:

    k1 = Key(b)
    k1.key = 'archive/2015/' + fantasyData['tournament'] + '/3/fantasyScoringData.json'
    round_three_data = k1.get_contents_as_string()
    round_three_data = json.loads(round_three_data)

    for player_index in xrange(len(data['leaderboard']['players'])):
        player = data['leaderboard']['players'][player_index]['player_bio']['first_name'] + ' ' + data['leaderboard']['players'][player_index]['player_bio']['last_name']
        fantasyData['player_data'][player]['dk_total_score'] = round_three_data['player_data'][player]['dk_total_score'] + fantasyData['player_data'][player]['dk_round_score']
        fantasyData['player_data'][player]['draftday_total_score'] = round_three_data['player_data'][player]['draftday_total_score'] + fantasyData['player_data'][player]['draftday_round_score']
    
    savedfantasyData = json.dumps(fantasyData)
    
    k = Key(b)
    k.key = 'archive/2015/' + fantasyData['tournament'] + '/' + str(fantasyData['roundNum']) + '/fantasyScoringData.json'
    k.set_contents_from_string(savedfantasyData)


print fantasyData

k2 = Key(b)
k2.key = 'fantasyScoringData.json'
k2.set_contents_from_string(savedfantasyData)
k2.make_public()
        
                               

