import requests
import json


from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


playersPerGroup = 2
numGroups = 6

player_list = ['Zach Johnson','Luke Donald','Stewart Cink','Stuart Appleby','Ben Crane','Scott Brown','Rory Sabbatini','Jhonattan Vegas','Steven Bowditch','Scott Stallings','Phil Mickelson','Billy Horschel']   #Use PGA Tour spelling of all names

groups = [['Zach Johnson','Luke Donald'],['Stewart Cink','Stuart Appleby'],['Ben Crane','Scott Brown'],['Rory Sabbatini','Jhonattan Vegas'],['Steven Bowditch','Scott Stallings'],['Phil Mickelson','Billy Horschel']]

weighting = {}
for group in groups:
    for player in group:
        weighting[player] = 0
        
        
weighting['playersPerGroup'] = playersPerGroup
weighting['numGroups'] = numGroups
weighting['groups'] = groups


