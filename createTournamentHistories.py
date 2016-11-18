import json
import requests
from bs4 import BeautifulSoup
from boto.s3.connection import S3Connection
from boto.s3.key import Key


sports_data_key = 'd6aw46aafm49s5xyc2bj8vwr' 
next_tournament = "Shell Houston Open"
year = 2015
tournament_link = 'shell-houston-open'


results_json = {}  


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')



link = 'http://www.pgatour.com/tournaments/' + tournament_link + '/field.html'

field = []

r = requests.get(link)
soup = BeautifulSoup(r.text)
player_table = soup.find(class_='field-table-content')
players = player_table.find_all("p")
for player in players:
    raw_name = player.text
    clean_name = raw_name.split(',')
    clean_name = clean_name[1][1:] + ' ' + clean_name[0]
    field.append(clean_name)
        
print "field:", len(field)

# get mapping from PGA names to SportsData names
k1 = Key(b)
k1.key = 'playerData/pgaToSportsDataMapping'
player_map = k1.get_contents_as_string()
player_map = json.loads(player_map)



for pga_name in field:
    
    player = player_map['players'][pga_name]
    
    results_json[pga_name] = []
    
    for year in [2013,2014]:
        
        player_results = {}
        
        k = Key(b)
        k.key = 'sportsData/' + str(year) + '/schedule.json'
        schedule_string = k.get_contents_as_string()
        schedule = json.loads(schedule_string)
    
        for tournament_index in xrange(len(schedule['tournaments'])):
    
            if schedule['tournaments'][tournament_index]['name'] == next_tournament:
        
                player_results['tournament'] = schedule['tournaments'][tournament_index]['name']
                player_results['year'] = str(year)
                    
                # get the tournament strokes gained
                k1 = Key(b)
                k1.key = 'sportsData/' + str(year) + '/' + schedule['tournaments'][tournament_index]['name'] + '/strokes_gained.json'
                strokes_gained = k1.get_contents_as_string()
                strokes_gained = json.loads(strokes_gained)
        
                if player not in strokes_gained.keys(): 
                    player_results['strokes_gained'] = 0
                    player_results['num_holes'] = 0
        
                else:
                    player_results['strokes_gained'] = strokes_gained[player]['tournament_strokes_gained']
                    player_results['num_holes'] = strokes_gained[player]['tournament_num_holes']
        
                results_json[pga_name].append(player_results)
                break


results_json = json.dumps(results_json)

k3 = Key(b)
k3.key = 'tournament_history.json'
k3.set_contents_from_string(results_json)
k3.make_public()

k2 = Key(b)
k2.key = 'sportsData/' + str(year) + '/' + next_tournament + '/tournament_history.json'
k2.set_contents_from_string(results_json)
