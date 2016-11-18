import pandas as pd
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key



year = 2015
tournament = 'Valero Texas Open'

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')


k = Key(b)
k.key = 'playerData/vvToPgaMapping'
player_map = k.get_contents_as_string()

player_map = json.loads(player_map)


salaries = pd.read_csv('https://s3.amazonaws.com/public.tenthtee/vv/VVSalaries.csv')

salaries_map = {}

for index,row in salaries.iterrows():
    pga_name = player_map['players'][row['PlayerName']]
    salaries.set_value(index,'PlayerName',pga_name)
    salaries_map[pga_name] = int(row['Salary'])
    
salaries_map = json.dumps(salaries_map)

k2 = Key(b)
k2.key = 'vv/salaries'
k2.set_contents_from_string(salaries_map)
k2.make_public()

k3 = Key(b)
k3.key = 'vv/' + str(year) + '/' + tournament + '/salaries'
k3.set_contents_from_string(salaries_map)