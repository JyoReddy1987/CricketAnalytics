import json
from bs4 import BeautifulSoup

from boto.s3.connection import S3Connection
from boto.s3.key import Key


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


tournamentName = 'RBC Heritage'

print tournamentName
tournamentName = json.dumps(tournamentName)
print tournamentName 

k = Key(b)
k.key = 'currentTournament'
k.set_contents_from_string(tournamentName)
k.make_public()