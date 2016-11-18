import requests
import pandas as pd
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')



request_string = 'https://s3.amazonaws.com/public.tenthtee/dk/contest-standings-4161803.csv' 

contest_data = {}
contest_data['contestName'] = 'testContest'
contest_data['payoutStructure'] = [100,40,10,5,5,5]
contest_data['tournament'] = 'testTournament'
contest_data['dateStarted'] = 'testDate'
contest_data['site'] = 'testSite'
contest_data['teams'] = []

df = pd.read_csv(request_string)


for index, row in df.iterrows():
    new_row = {}
    new_row['username'] = row['EntryName']
    new_row['team'] = []

    if type(row['Lineup']) != float:
        lineup_array = row['Lineup'].split(',')

        new_row['team'].append(lineup_array[0][4:])
        new_row['team'].append(lineup_array[1][4:])
        new_row['team'].append(lineup_array[2][4:])
        new_row['team'].append(lineup_array[3][4:])
        new_row['team'].append(lineup_array[4][4:])
        new_row['team'].append(lineup_array[5][4:])

    contest_data['teams'].append(new_row)
    if index == 10: break    
            
#
#usernames = []
#player_one = []
#player_two = []
#player_three = []
#player_four = []
#player_five = []
#player_six = []
#
#
#for index, row in df.iterrows():
#    
#    usernames.append(row['EntryName'])
#    
#    player_one.append(lineup_array[0][4:])
#    player_two.append(lineup_array[1][4:])
#    player_three.append(lineup_array[2][4:])
#    player_four.append(lineup_array[3][4:])
#    player_five.append(lineup_array[4][4:])
#    player_six.append(lineup_array[5][4:])
#    
#
#df = pd.DataFrame(usernames,columns=['usernames'])
#df['player_one'] = player_one
#df['player_two'] = player_two
#df['player_three'] = player_three
#df['player_four'] = player_four
#df['player_five'] = player_five
#df['player_six'] = player_six
#
#csv = df.to_csv()

contest_data = json.dumps(contest_data)

k = Key(b)
k.key = 'dk/4161803'
k.set_contents_from_string(contest_data)
k.make_public()

print contest_data
