import json
import requests
from bs4 import BeautifulSoup
import difflib

from boto.s3.connection import S3Connection
from boto.s3.key import Key



tournament_name = 'RBC Heritage'
pga_tournament_link = 'rbc-heritage'
year = 2015
sports_data_key = 'd6aw46aafm49s5xyc2bj8vwr'    



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

k = Key(b)
k.key = 'sportsData/' + str(year) + '/schedule.json'
schedule_string = k.get_contents_as_string()
schedule = json.loads(schedule_string)


# get tournament id
for tournament in schedule['tournaments']:
    # uncomment line below to identify the tournament names
    # print tournament['name'],tournament['id']
    # if tournament['name'] == target_tournament: break
    
    # identify tournament to get api 
    if tournament['name'] == tournament_name:
        tournament_id = tournament['id']


        # get sportsData first round tee times list
        request_string = 'http://api.sportsdatallc.org/golf-t1/teetimes/pga/' + str(year) + '/tournaments/' + tournament_id + '/rounds/1/teetimes.json?api_key=' + sports_data_key
        r = requests.get(request_string)
        teetimes = r.json()
        teetimes = json.dumps(teetimes)
                
        # save tee times to AWS S3
        k.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/1/teetimes.json'
        k.set_contents_from_string(teetimes)
    
        break
            


k1 = Key(b)
k1.key = 'sportsData/' + str(year) + '/' + tournament_name + '/rounds/1/teetimes.json'
sd_tee_times = k1.get_contents_as_string()
sd_tee_times = json.loads(sd_tee_times)

sd_field = []

for course_info in sd_tee_times['round']['courses']:
    for pairings_info in course_info['pairings']:
        for player_info in pairings_info['players']:
            sd_field.append(player_info['first_name'] + ' ' + player_info['last_name'])
            

# get current mapping
k2 = Key(b)
k2.key = 'playerData/sportsDataToPgaMapping'
current_mapping = k2.get_contents_as_string()

current_mapping = json.loads(current_mapping)



# get PGA Tour field list for tournament 

pga_field = []

link = 'http://pgatour.com/tournaments/' + pga_tournament_link + '/field.html'
r = requests.get(link)
soup = BeautifulSoup(r.text)
player_table = soup.find(class_='field-table-content')
players = player_table.find_all('p')
for player in players:
    raw_name = player.text
    clean_name = raw_name.split(',')
    clean_name = clean_name[1][1:] + ' ' + clean_name[0] 
    pga_field.append(clean_name)



# compare new sd field to current mapping
# see if any names aren't in keys 

for player in sd_field:
    if player not in current_mapping['players'].keys():
        if player in pga_field:
            current_mapping['players'][player] = player
        else:
            print player, difflib.get_close_matches(player,pga_field)
        
current_mapping['asOfTournament'] = tournament_name
current_mapping['asOfYear'] = year
current_mapping = json.dumps(current_mapping)

k3 = Key(b)
k3.key = 'playerData/sportsDataToPgaMapping'
current_mapping = k3.set_contents_from_string(current_mapping)




