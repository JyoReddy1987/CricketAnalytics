from bs4 import BeautifulSoup
import urllib2
import json

import os
from selenium import webdriver


from boto.s3.connection import S3Connection
from boto.s3.key import Key

# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')

# create connection to bucket 
b = c.get_bucket('public.tenthtee')

driver = webdriver.Firefox()
url = "http://www.owgr.com/en/Ranking.aspx?pageNo=1&pageSize=200&country=All"

driver.get(url)
table = driver.find_element_by_tag_name('table')
row = table.find_elements_by_tag_name('td')


ranks = []
player_names = []
countries = []


for data_index in xrange(1,len(row)):
    if data_index == 1 or data_index % 11 == 0:
        rank = row[data_index].text
        ranks.append(rank)
    elif data_index == 4 or (data_index - 4) % 11 == 0:
        name = row[data_index].text
        player_names.append(name)
    elif data_index == 3 or (data_index - 3) % 11 == 0:
        img = row[data_index].find_element_by_tag_name("img")
        country = img.get_attribute("title")
        countries.append(country)
        print country
        
olympics_field_size = 60

rank_map = {}

for rank in xrange(1,len(ranks)):
    rank_map[rank] = {}
    rank_map[rank]['name'] = player_names[rank - 1]
    if countries[rank - 1] == 'ENG' or countries[rank - 1] == 'WAL' or countries[rank - 1]: 
        rank_map[rank]['country'] = countries[rank - 1]
    else:
        rank_map[rank]['country'] = countries[rank - 1]


country_counts = {}
olympics_field = []

for rank in xrange(1,123):
    
    player_country = rank_map[str(rank)]['country']

    if player_country not in country_counts.keys():
        country_counts[player_country] = 1
        olympics_field.append(rank_map[str(rank)]['name'])
        
    else:
        
        if country_counts[player_country] < 4 and rank <= 15:
            olympics_field.append(rank_map[str(rank)]['name'])
        elif country_counts[player_country] < 2:
            olympics_field.append(rank_map[str(rank)]['name'])
        
        country_counts[player_country] += 1

    if len(olympics_field) >= olympics_field_size:
        break

print olympics_field
print len(olympics_field)
print country_counts


#link = 'http://www.owgr.com/en/Ranking.aspx?pageNo=1&pageSize=200&country=All'
#
#page = urllib2.urlopen(link)
#soup = BeautifulSoup(page)
#
#table = soup.find("table")
#player_rows = table.find_all("tr")
#
#player_names = []
#ranks = []
#countries = []
#
#rank_map = {}
#
#for player_row in player_rows:
#    player_data = player_row.find_all("td")
#    for i in xrange(len(player_data)):
#        if i==4: 
#            player_name = player_data[i].text
#            player_names.append(player_name)
#            
#for player_row in player_rows:
#    player_data = player_row.find_all("td")
#    for i in xrange(len(player_data)):
#        if i==0: 
#            rank = player_data[i].text
#            ranks.append(rank)
#            
#for player_row in player_rows:
#    player_data = player_row.find_all("td")
#    for i in xrange(len(player_data)):
#        if i==3: 
#            country = player_data[i].find("img").get("title")
#            countries.append(country)
#
#for rank in xrange(1,len(ranks)):
#    rank_map[rank] = {}
#    rank_map[rank]['name'] = player_names[rank - 1]
#    if countries[rank - 1] == 'ENG' or countries[rank - 1] == 'WAL' or countries[rank - 1]: 
#        rank_map[rank]['country'] = countries[rank - 1]
#    else:
#        rank_map[rank]['country'] = countries[rank - 1]
#
#
#rank_map = json.dumps(rank_map)
#
#k = Key(b)
#k.key = 'owgr/3-27-2015'
#k.set_contents_from_string(rank_map)
#
#rank_map = json.loads(rank_map)
#
#country_counts = {}
#olympics_field = []
#
#for rank in xrange(1,123):
#    
#    player_country = rank_map[str(rank)]['country']
#
#    if player_country not in country_counts.keys():
#        country_counts[player_country] = 1
#        olympics_field.append(rank_map[str(rank)]['name'])
#        
#    else:
#        
#        if country_counts[player_country] < 4 and rank <= 15:
#            olympics_field.append(rank_map[str(rank)]['name'])
#        elif country_counts[player_country] < 2:
#            olympics_field.append(rank_map[str(rank)]['name'])
#        
#        country_counts[player_country] += 1
#
#    if len(olympics_field) >= olympics_field_size:
#        break
#
#print olympics_field
#print len(olympics_field)
#print country_counts