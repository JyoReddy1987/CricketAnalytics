import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')



contest_structure = {}


contest_structure['Draftkings'] = {}
contest_structure['Draftday'] = {}
contest_structure['Victiv'] = {}
contest_structure['Fantasyfeud'] = {}


contest_structure['Draftkings']['numPlayers'] = 6
contest_structure['Draftkings']['salaryCap'] = 50000

contest_structure['Victiv']['numPlayers'] = 7
contest_structure['Victiv']['salaryCap'] = 50000

contest_structure['Draftday']['numPlayers'] = 6
contest_structure['Draftday']['salaryCap'] = 100000

contest_structure['Fantasyfeud']['numPlayers'] = 10
contest_structure['Fantasyfeud']['salaryCap'] = 1000000


contest_structure = json.dumps(contest_structure)


k = Key(b)
k.key = 'contestStructure'
k.set_contents_from_string(contest_structure)


