import requests
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

started = True

tournament_code = '002'

#Use PGA Tour spelling of all names

roundNum = 4


scoring_rubric = {}
scoring_rubric[-3] = 20
scoring_rubric[-2] = 8
scoring_rubric[-1] = 3
scoring_rubric[0] = .5
scoring_rubric[1] = -.5
scoring_rubric[2] = -1




def eventPoints(event):
    
    points = 0
    if event == 'double eagle':
        points = 20
    elif event == 'eagle':
        points = 8
    elif event == 'birdie':
        points = 3
    elif event == 'par':
        points = .5
    elif event == 'bogey':
        points = -.5
    elif event == 'double bogey or worse':
        points = -1
    elif event == 'three birdies in a row':
        points = 3
    elif event == 'bogey-free round':
        points = 3
    elif event == 'all rounds under seventy':
        points = 5
    elif event == '1st place':
        points = 30
    elif event == '2nd place':
        points = 20
    elif event == '3rd place':
        points = 18
    elif event == '4th place':
        points = 16
    elif event == '5th place':
        points = 14
    elif event == '6th place':
        points = 12
    elif event == '7th place':
        points = 10
    elif event == '8th place':
        points = 9
    elif event == '9th place':
        points = 8
    elif event == '10th place':
        points = 7
    elif event == '11th-15th place':
        points = 6
    elif event == '16th-20th place':
        points = 5
    elif event == '21th-25th place':
        points = 4
    elif event == '26th-30th place':
        points = 3
    elif event == '31th-40th place':
        points = 2
    elif event == '41th-50th place':
        points = 1

    return points




leaderboard_string = 'http://www.pgatour.com/data/r/' + tournament_code + '/leaderboard-v2.json'

r = requests.get(leaderboard_string)

data = r.json()

# create json object with all the players who are in this week's competitions
# get START_HOLES, SCORES, FANTASY_SCORES, REMAINING_HOLES, STATUS (if round is official, then scores are official)   

scoringData = {}
scoringData['isFinished'] = data['leaderboard']['is_finished']
scoringData['timestamp'] = data['last_updated']
scoringData['tournament'] = data['debug']['tournament_in_schedule_file_name']
scoringData['roundNum'] = data['debug']['current_round_in_setup']

for player_index in xrange(len(data['leaderboard']['players'])):
    
    player = data['leaderboard']['players'][player_index]['player_bio']['first_name'] + ' ' + data['leaderboard']['players'][player_index]['player_bio']['last_name']
    
    scoringData[player] = {}
    scoringData[player]['score'] = data['leaderboard']['players'][player_index]['total']
    scoringData[player]['status'] = data['leaderboard']['players'][player_index]['status']
    scoringData[player]['holes'] = data['leaderboard']['players'][player_index]['holes']        
    if scoringData[player]['status'] in ['dq','wd','cut']: # and data['leaderboard']['players'][player_index]['holes'] == []:
        next        

    else:
        scoringData[player]['startHole'] = data['leaderboard']['players'][player_index]['start_hole']
        scoringData[player]['currentPosition'] = data['leaderboard']['players'][player_index]['current_position']
        scoringData[player]['playerId'] = data['leaderboard']['players'][player_index]['player_id']
        scoringData[player]['holesCompletedThisRound'] =  data['leaderboard']['players'][player_index]['thru']
        
        scoringData[player]['DKRoundPoints'] = 0
        scoringData[player]['birdiesInARow'] = False 
        scoringData[player]['holes'] = {}
        
        
        for hole_num in xrange(18):
        
            event = ''
            hole_info = {}
            hole_info['holeNum'] = data['leaderboard']['players'][player_index]['holes'][hole_num]['course_hole_id']
            hole_info['par'] = data['leaderboard']['players'][player_index]['holes'][hole_num]['par']
            hole_info['strokes'] = data['leaderboard']['players'][player_index]['holes'][hole_num]['strokes']
         
            scoringData[player]['holes'][hole_info['holeNum']] = {}
            scoringData[player]['holes'][hole_info['holeNum']]['par'] = hole_info['par']
            scoringData[player]['holes'][hole_info['holeNum']]['strokes'] = hole_info['strokes']
            scoringData[player]['holes'][hole_info['holeNum']]['relative to par'] = hole_info['strokes'] - hole_info['par']
            
            if scoringData[player]['holes'][hole_info['holeNum']]['relative to par'] == -3:
                event = 'double eagle'
            elif scoringData[player]['holes'][hole_info['holeNum']]['relative to par'] == -2:
                event = 'eagle'
            elif scoringData[player]['holes'][hole_info['holeNum']]['relative to par'] == -1:
                event = 'birdie'
            elif scoringData[player]['holes'][hole_info['holeNum']]['relative to par'] == 0:
                event = 'par'
            elif scoringData[player]['holes'][hole_info['holeNum']]['relative to par'] == 1:
                event = 'bogey'
            elif scoringData[player]['holes'][hole_info['holeNum']]['relative to par'] >= 2:
                event = 'double bogey or worse'
                
            scoringData[player]['holes'][hole_info['holeNum']]['dk_points'] = eventPoints(event)  
            scoringData[player]['DKRoundPoints'] += scoringData[player]['holes'][hole_info['holeNum']]['dk_points'] 
           
             
scoringData = json.dumps(scoringData)

print scoringData

k = Key(b)
k.key = 'dkScoring.json'
k.set_contents_from_string(scoringData)
k.make_public()