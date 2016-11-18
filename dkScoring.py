import requests
import pandas as pd
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

tournament_code = '003'
request_string = 'http://www.pgatour.com/data/r/' + tournament_code + '/leaderboard-v2.json'

r = requests.get(request_string)
data = r.json()

fantasyData = {}
fantasyData['isFinished'] = data['leaderboard']['is_finished']
fantasyData['timestamp'] = data['last_updated']
fantasyData['roundNum'] = data['debug']['current_round_in_setup']
fantasyData['tournament'] = data['debug']['tournament_in_schedule_file_name']
fantasyData['roundState'] = data['leaderboard']['round_state']
fantasyData['player_data'] = {}

for player_index in xrange(len(data['leaderboard']['players'])):
    
    player = data['leaderboard']['players'][player_index]['player_bio']['first_name'] + ' ' + data['leaderboard']['players'][player_index]['player_bio']['last_name']
    
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
    fantasyData['player_data'][player]['holes'] = {}
        
    if fantasyData['player_data'][player]['status'] == 'active':
        for hole_index in xrange(18):
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']] = {}
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['par'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['par']
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['score'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['strokes']
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['relToPar'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['strokes'] - data['leaderboard']['players'][player_index]['holes'][hole_index]['par']

            relToPar = fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['relToPar']
            if relToPar == -1: fantasyData['player_data'][player]['dk_round_score'] += 20
            elif relToPar == -2: fantasyData['player_data'][player]['dk_round_score'] += 8
            elif relToPar == -1: fantasyData['player_data'][player]['dk_round_score'] += 3
            elif relToPar == 0: fantasyData['player_data'][player]['dk_round_score'] += .5
            elif relToPar == 1: fantasyData['player_data'][player]['dk_round_score'] -= .5
            elif relToPar >= 2: fantasyData['player_data'][player]['dk_round_score'] -= 1


print data['leaderboard']['players'][0]