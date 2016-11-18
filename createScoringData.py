import requests
import json
import datetime

from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


started = True




tournament_code = '005'

#Use PGA Tour spelling of all names
player_list = ['Jordan Spieth',
'Dustin Johnson',
'Jason Day',
'Jimmy Walker',
'Ian Poulter',
'Graham DeLaet',
'Patrick Reed',
'Chris Kirk',
'Hunter Mahan',
'Brandt Snedeker',
'Nick Watney',
'Jim Furyk']

#Use PGA Tour spelling of all names

roundNum = 1
tournament = 'At&T Pebble Beach National Pro-Am'





leaderboard_string = 'http://www.pgatour.com/data/r/' + tournament_code + '/leaderboard-v2.json'

r = requests.get(leaderboard_string)

data = r.json()

# create json object with all the players who are in this week's competitions
# get START_HOLES, SCORES, FANTASY_SCORES, REMAINING_HOLES, STATUS (if round is official, then scores are official)   

scoringData = {}

if started == True:
    scoringData['isFinished'] = data['leaderboard']['is_finished']
    scoringData['timestamp'] = data['last_updated']
    scoringData['tournament'] = data['debug']['tournament_in_schedule_file_name']
    scoringData['roundNum'] = data['debug']['current_round_in_setup']

    for player_index in xrange(len(data['leaderboard']['players'])):
    
        player = data['leaderboard']['players'][player_index]['player_bio']['first_name'] + ' ' + data['leaderboard']['players'][player_index]['player_bio']['last_name']
        
        if player in player_list:
            print player, data['leaderboard']['players'][player_index]['status'], data['leaderboard']['players'][player_index]['thru']
            scoringData[player] = {}
            scoringData[player]['score'] = data['leaderboard']['players'][player_index]['total']
            scoringData[player]['status'] = data['leaderboard']['players'][player_index]['status']
            scoringData[player]['holes'] = data['leaderboard']['players'][player_index]['holes']        
            if scoringData[player]['status'] in ['dq','wd'] and data['leaderboard']['players'][player_index]['holes'] == []:
                next            
            else:
                scoringData[player]['startHole'] = data['leaderboard']['players'][player_index]['start_hole']
                scoringData[player]['currentPosition'] = data['leaderboard']['players'][player_index]['current_position']
                scoringData[player]['playerId'] = data['leaderboard']['players'][player_index]['player_id']
                scoringData[player]['holesCompletedThisRound'] =  data['leaderboard']['players'][player_index]['thru']
                scoringData[player]['holes'] = []
        
                for hole_num in xrange(18):
            
                    hole_info = {}
                    hole_info['holeNum'] = data['leaderboard']['players'][player_index]['holes'][hole_num]['course_hole_id']
                    hole_info['par'] = data['leaderboard']['players'][player_index]['holes'][hole_num]['par']
                    hole_info['strokes'] = data['leaderboard']['players'][player_index]['holes'][hole_num]['strokes']
            
            
                    scoringData[player]['holes'].append(hole_info)

else:
    scoringData['tournament'] = tournament
    scoringData['roundNum'] = 1    


feedData = {}

feedData['roundNum'] = roundNum
feedData['tournament'] = scoringData['tournament']
feedData['players'] = {}

for player in player_list:
    
    if started == True:
        feedData['players'][player] = {}
        feedData['timestamp'] = scoringData['timestamp']
        feedData['tournament'] = scoringData['tournament']
        feedData['players'][player]['score'] = scoringData[player]['score']
        feedData['players'][player]['status'] = scoringData[player]['status']
        feedData['players'][player]['holes'] = scoringData[player]['holes']
        feedData['players'][player]['thru'] = scoringData[player]['holesCompletedThisRound']
        if feedData['players'][player]['thru'] != None:
            feedData['players'][player]['holesRemaining'] = 18 - scoringData[player]['holesCompletedThisRound']
        else:
            feedData['players'][player]['holesRemaining'] = 18
        feedData['players'][player]['dkScore'] = 15
    else:
        feedData['players'][player] = {}
        feedData['players'][player]['score'] = 0
        feedData['players'][player]['status'] = 0
        feedData['players'][player]['holes'] = 0
        feedData['players'][player]['holesRemaining'] = 18 
        feedData['players'][player]['thru'] = 0
        feedData['players'][player]['dkScore'] = 0


feedData1 = json.dumps(feedData)


k = Key(b)
k.key = 'scoringData.json'
k.set_contents_from_string(feedData1)
k.make_public()

k2 = Key(b)
k2.key = 'archive/2015/' + feedData['tournament'] + '/' + str(feedData['roundNum']) + '/scoringData.json'
k2.set_contents_from_string(feedData1)
k2.make_public()

print feedData1