import json
import requests
from bs4 import BeautifulSoup
import difflib

from boto.s3.connection import S3Connection
from boto.s3.key import Key

year = 2015
tournament_name = 'The Masters'

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')

k = Key(b)
k.key = 'projections/projected_scores.json'
projected_scores_string = k.get_contents_as_string()
projected_scores = json.loads(projected_scores_string)

for score in projected_scores:
    print score[0]['player_name']