import requests


# This script requests scoring data from the PGA Tour and then turns it into a DraftKings fantasy score 
# Only addresses scores for the current round of the tournament
# Does scores earned for points earned for each hole.  Does NOT calculate the scores earned based on place, all rds under 70, bogey-free round, or three birdies in a row

# if run as is, this script will print "[player name] [DraftKings points earned this round]" for each player during the final round of the 2015 Farmers Insurance Open.  For example: Brooks Koepka 13.5.
# the second half of the players earn no points this round because they missed the cut 


# Link to PGA TOUR website
# '004' points to the 2015 Northern Trust Open.  Because the tournament is completed, the final round is returned as the current round.
tournament_code = '004'
request_string = 'http://www.pgatour.com/data/r/' + tournament_code + '/leaderboard-v2.json'


# Request json scoring data from PGA Tour website
r = requests.get(request_string)
data = r.json()



# Create a json file for scoring data, starting with tournament information
fantasyData = {} 
fantasyData['isFinished'] = data['leaderboard']['is_finished']
fantasyData['timestamp'] = data['last_updated']
fantasyData['roundNum'] = data['debug']['current_round_in_setup']
fantasyData['tournament'] = data['debug']['tournament_in_schedule_file_name']
fantasyData['roundState'] = data['leaderboard']['round_state']
fantasyData['course_data'] = {}

# there can be several courses - up to 3 per tournament
for course in data['leaderboard']['courses']:
    fantasyData['course_data'][course['course_id']] = {}
    fantasyData['course_data'][course['course_id']]['course_name'] = course['course_name']
    fantasyData['course_data'][course['course_id']]['course_id'] = course['course_id']

        
fantasyData['player_data'] = {}

# go through all the players
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
    fantasyData['player_data'][player]['current_position'] = data['leaderboard']['players'][player_index]['current_position']
    fantasyData['player_data'][player]['par_performance'] = data['leaderboard']['players'][player_index]['par_performance']
    fantasyData['player_data'][player]['course_id'] = data['leaderboard']['players'][player_index]['course_id']
    
    # create a key for number of holes remaining in the tournament
    if fantasyData['player_data'][player]['status'] == 'active':
        addForRound = (4 - fantasyData['roundNum']) * 18
        fantasyData['player_data'][player]['numHolesToGo'] = 18 - fantasyData['player_data'][player]['thru'] + addForRound
    else:
        fantasyData['player_data'][player]['numHolesToGo'] = 0

            
    fantasyData['player_data'][player]['holes'] = {}
        
    if fantasyData['player_data'][player]['status'] == 'active':
        
        #for each player who is still active in the tournament, go through each hole and record the score, par, and the players score relative to par
        for hole_index in xrange(18):
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']] = {}
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['par'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['par']
            fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['score'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['strokes']
            if data['leaderboard']['players'][player_index]['holes'][hole_index]['strokes']:
                fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['relToPar'] = data['leaderboard']['players'][player_index]['holes'][hole_index]['strokes'] - data['leaderboard']['players'][player_index]['holes'][hole_index]['par']

                # translate the score relative to par into DraftKings points
                relToPar = fantasyData['player_data'][player]['holes'][data['leaderboard']['players'][player_index]['holes'][hole_index]['course_hole_id']]['relToPar']
                if relToPar == -3: fantasyData['player_data'][player]['dk_round_score'] += 20
                elif relToPar == -2: fantasyData['player_data'][player]['dk_round_score'] += 8
                elif relToPar == -1: fantasyData['player_data'][player]['dk_round_score'] += 3
                elif relToPar == 0: fantasyData['player_data'][player]['dk_round_score'] += .5
                elif relToPar == 1: fantasyData['player_data'][player]['dk_round_score'] -= .5
                elif relToPar >= 2: fantasyData['player_data'][player]['dk_round_score'] -= 1
                
    print player, fantasyData['player_data'][player]['dk_round_score']





                               

