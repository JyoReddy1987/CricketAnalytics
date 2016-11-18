import requests
import json
import difflib
import time
from bs4 import BeautifulSoup


from boto.s3.connection import S3Connection
from boto.s3.key import Key



year = 2015
tournament_name = 'RBC Heritage'
tournament_link = 'rbc-heritage'

sports_data_key = 'd6aw46aafm49s5xyc2bj8vwr' 
# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')

k = Key(b)
k.key = 'sportsData/' + str(year) + '/schedule.json'
schedule_string = k.get_contents_as_string()
schedule = json.loads(schedule_string)

sd_list = []


for tournament in schedule['tournaments']:
    tournament_id = tournament['id']

    if tournament['name'] == tournament_name:
            
        # get field through first round tee times
        # CHANGE TO FIELD -> SPORTS DATA NAMES
        link = 'http://api.sportsdatallc.org/golf-t1/teetimes/pga/' + str(2015) + '/tournaments/' + tournament_id + '/rounds/'+ str(1) + '/teetimes.json?api_key=' + sports_data_key
        r = requests.get(link)

        tee_times = r.json()
    
        for course_data in tee_times['round']['courses']:
            for pairings_data in course_data['pairings']:
                for player_data in pairings_data['players']:
                    name = player_data['first_name'] + ' ' + player_data['last_name']
                    if name not in sd_list:
                        sd_list.append(name)
                    
        break

print len(sd_list)




# get current pgatosportsdata mapping
k1 = Key(b)
k1.key = 'playerData/pgaToSportsDataMapping'
current_map = k1.get_contents_as_string()



player_map = {}
player_map['asOfTournament'] = tournament_name
player_map['asOfYear'] = 2015
player_map['players'] = {}




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



for player in field:
    if player not in sd_list:
        print player, difflib.get_close_matches(player,sd_list)
        if player == 'Zachary Blair': player_map['players'][player] = 'Zac Blair'
        elif player == 'Brendon de Jonge': player_map['players'][player] = 'Brendon De Jonge'
        elif player == 'Gonzalo Fdez-Castano': player_map['players'][player] = 'Gonzalo Fernandez-Castano'
        elif player == 'Charles Howell III': player_map['players'][player] = 'Charles Howell'
        elif player == 'Billy Hurley III': player_map['players'][player] = 'Billy Hurley'
        elif player == 'Davis Love III': player_map['players'][player] = 'Davis Love'
        elif player == 'Bill Lunde': player_map['players'][player] = 'William Lunde'
        elif player == 'Nigel P. Spence': player_map['players'][player] = 'Nigel Spence'
        elif player == 'Carlos Sainz Jr': player_map['players'][player] = 'Carlos Sainz'
        elif player == 'Tian-Lang Guan': player_map['players'][player] = 'Guan Tian-Lang'
        elif player == 'Stephen Lewton': player_map['players'][player] = 'Steve Lewton'
        elif player == 'Freddie Jacobson': player_map['players'][player] = 'Fredrik Jacoboson'
        elif player == 'Jr. Serna': player_map['players'][player] = 'Efren Serna'
        elif player == 'Steve Stricker': player_map['players'][player] = 'Steve Stricker'
        elif player == 'WC Liang': player_map['players'][player] = 'Wen-Chong Liang'
        elif player == 'Yan Wei Liu': player_map['players'][player] = 'Yan-wei Liu'
        elif player == 'Richard S. Johnson': player_map['players'][player] = 'Richard Johnson'
        elif player == 'S.J. Park': player_map['players'][player] = 'Sung Joon Park'
        elif player == 'Rafael Cabrera Bello': player_map['players'][player] = 'Rafael Cabrera-Bello'
        elif player == 'Sangmoon Bae': player_map['players'][player] = 'Sang-Moon Bae'
        elif player == 'Darren Clarke': player_map['players'][player] = 'Darren Clarke'
        elif player == 'Austin Cook': player_map['players'][player] = 'Austin Cook'
        elif player == 'Kelvin Day': player_map['players'][player] = 'Kelvin Day'
        elif player == 'Cody Gribble': player_map['players'][player] = 'Cody Gribble'
        elif player == 'Smylie Kaufman': player_map['players'][player] = 'Smylie Kaufman'
        elif player == 'Andrew Landry': player_map['players'][player] = 'Andrew Landry'
        elif player == 'Ben Willman': player_map['players'][player] = 'Ben Willman'
    else:
        player_map['players'][player] = player
        
    
player_map = json.dumps(player_map)

# get current pgatosportsdata mapping
k2 = Key(b)
k2.key = 'playerData/pgaToSportsDataMapping'
k2.set_contents_from_string(player_map)
