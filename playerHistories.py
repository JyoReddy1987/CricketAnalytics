import requests
from bs4 import BeautifulSoup
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key


tournament = 'RBC Heritage'
tournament_string = 'rbc-heritage'
year = 2015


# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')

k = Key(b)
k.key = '/sportsData/2015/schedule.json'
schedule = k.get_contents_as_string()
schedule = json.loads(schedule)


def identify_tournament_index(schedule,tournament):
    for i in xrange(len(schedule['tournaments'])):
        if schedule['tournaments'][i]['name'] == tournament:
            return i    

def find_last_week_index(current_index):
    return [current_index - 1]

def find_last_months_index(current_index):
    return [current_index - 4, current_index - 3, current_index - 2, current_index - 1]
    
def find_last_3months_index(current_index):
    index_array = [x for x in xrange(current_index - 12, current_index)]
    return index_array
    
def find_last_6months_index(current_index):
    index_array = [x for x in xrange(current_index - 22, current_index)]
    return index_array


def get_pga_tour_field(tournament_string):
    
    link = 'http://www.pgatour.com/tournaments/' + tournament_string + '/field.html'

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
        
    return field


def get_pga_to_sportsdata_map():
    # get current pgatosportsdata mapping
    k1 = Key(b)
    k1.key = 'playerData/pgaToSportsDataMapping'
    current_map = k1.get_contents_as_string()
    
    pga_to_sportsdata_map = json.loads(current_map)
    
    return pga_to_sportsdata_map



def get_strokes_gained_per_tournament(player, year, tournament):
    k1 = Key(b)
    k1.key = 'sportsData/' + str(year) + '/' + tournament + '/strokes_gained.json'
    strokes_gained_json = k1.get_contents_as_string()
    strokes_gained_json = json.loads(strokes_gained_json)
    if player in strokes_gained_json:
        strokes_gained = strokes_gained_json[player]['tournament_strokes_gained']
        return strokes_gained
    else:
        return 0


def lookup_tournament_history(schedule,year,player,index_array):

    total_strokes_gained = 0
    num_tournaments = 0
    
    for tournament_number in index_array:
        tournament_name = schedule['tournaments'][tournament_number]['name']
        
        strokes_gained = get_strokes_gained_per_tournament(player,year,tournament_name)
       
        if strokes_gained != 0: 
            total_strokes_gained += strokes_gained
            num_tournaments += 1
    
    if num_tournaments == 0: return total_strokes_gained
    else: return total_strokes_gained / float(num_tournaments)        



field = get_pga_tour_field(tournament_string)
pga_to_sportsdata_map = get_pga_to_sportsdata_map()


player_histories = {}
player_histories['asOfTournament'] = tournament  


current_index = identify_tournament_index(schedule,tournament)

for player in field:
    sd_name = pga_to_sportsdata_map['players'][player]
    player_histories[player] = {}
    player_histories[player]['lastWeek'] = lookup_tournament_history(schedule,2015,sd_name,find_last_week_index(current_index))
    player_histories[player]['lastMonth'] = lookup_tournament_history(schedule,2015,sd_name,find_last_months_index(current_index))
    player_histories[player]['last3Months'] = lookup_tournament_history(schedule,2015,sd_name,find_last_3months_index(current_index))
    player_histories[player]['last6Months'] = lookup_tournament_history(schedule,2015,sd_name,find_last_6months_index(current_index))

print player_histories
player_histories = json.dumps(player_histories) 

k2 = Key(b)
k2.key = 'history'
k2.set_contents_from_string(player_histories)
k2.make_public()


k3 = Key(b)
k3.key = 'sportsData/' + str(year) + '/' + tournament + '/history'
k3.set_contents_from_string(player_histories)
k3.make_public()
