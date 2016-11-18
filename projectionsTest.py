import requests
import pandas as pd
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


r = requests.get('https://s3.amazonaws.com/public.tenthtee/fantasyScoringData.json')

data = r.json()
# get the current fantasy score
#    get players, current score, round, holes remaining

#print data['player_data']['Danny Lee']['course_id']
numCourses = 2
courseIds = [004,104]
finalRoundCourseId = 004


# set up 

rdNum = data['roundNum']



courseName = data['course_data'][data['player_data']['Danny Lee']['course_id']]['course_name']
playersCourseId = data['player_data']['Danny Lee']['course_id']

if rdNum == 1:
    if numCourses == 2:
        thirdRoundCourseId =  finalRoundCourseId
        if playersCourseId == courseIds[0]:
            secondRoundCourseId = courseIds[1] 
        else: # courseId == courseIds[1]
            secondRoundCourseId = courseIds[0]
    else: # numCourses == 3
        thirdRoundCourseId =  finalRoundCourseId
        if playersCourseId == courseIds[0]:
            secondRoundCourseId = courseIds[1] 
        else: # courseId == courseIds[1]
            secondRoundCourseId = courseIds[0]


print courseName
print data['course_data']

#for player_data in data['player_data']:
#    print player_data