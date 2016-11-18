import json
import datetime

# created from the tee time information
from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L') 

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


players = ['Sam Saunders',
'Adam Hadwin',
'Lee Westwood',
'David Hearn',
'Carlos Ortiz',
'Jerry Kelly',
'Greg Chalmers',
'Tony Finau',
'Michael Putnam',
'Brendon de Jonge',
'Ricky Barnes',
'Jason Bohn',
'Sam Saunders',
'Adam Hadwin',
'Lee Westwood',
'David Hearn',
'Carlos Ortiz',
'Jerry Kelly',
'Greg Chalmers',
'Tony Finau',
'Michael Putnam',
'Brendon de Jonge',
'Ricky Barnes',
'Jason Bohn',
'Sam Saunders',
'Adam Hadwin',
'Lee Westwood',
'David Hearn',
'Carlos Ortiz',
'Jerry Kelly',
'Greg Chalmers',
'Tony Finau',
'Michael Putnam',
'Brendon de Jonge',
'Ricky Barnes',
'Jason Bohn']


tournament = "Valspar Championship"
roundNum = 1

date = {
    "year" : 2015,
    "month" : 2,
    "day" : 12,
    "dayName" : "Thursday"
}

# two hours fifteen minutes after first tee time
# datetime is EST because server is EST
# GMT is five hours past EST

match_cutoff_time = {
    "hour" : 19,
    "minute" : 00
}




match_data = {}
match_data['date'] = date
match_data['players'] = players
match_data['tournament'] = tournament
match_data['roundNum'] = roundNum

if datetime.datetime.now() >= datetime.datetime(date['year'],date['month'],date['day'],match_cutoff_time['hour'],match_cutoff_time['minute']): 
    match_data['cutoffTime'] = 0
else:
    match_data['cutoffTime'] = match_cutoff_time

match_data = json.dumps(match_data)

print match_data


k = Key(b)
k.key = 'matchData.json'
k.set_contents_from_string(match_data)
k.make_public()

k2 = Key(b)
k2.key = 'archive/2015/' + tournament + '/' + str(roundNum) + '/matchData.json'
k2.set_contents_from_string(match_data)
k2.make_public()
