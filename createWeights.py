import json
import datetime
from boto.s3.connection import S3Connection
from boto.s3.key import Key
# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')





# create tournament weights
tournament_name = 'World Golf Championships - Cadillac Championship'
year = 2015

weighting_chart = [.005,.01,.015,.03]  # this scheme goes to zero at forty weeks
num_weeks = 40
num_days = 40 * 7



# get this year's tournament list
request_key = 'sportsData/' + str(year) + '/schedule.json'
k = Key(b)
k.key = request_key
schedule = k.get_contents_as_string()

schedule = json.loads(schedule)



# get start date of this tournament
for tournament in schedule['tournaments']:
    if tournament['name'] == tournament_name: break

start_date = tournament['start_date']
start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')


tournament_weights = {}
tournament_weights['current_tournament'] = tournament_name
tournament_weights['year'] = year
tournament_weights['weights'] = {}


# find how many days behind the other tournaments are
for tournament in schedule['tournaments']:
    test_name = tournament['name']
    
    if test_name == tournament_name: continue

    test_start_date = tournament['start_date']
    test_start_date = datetime.datetime.strptime(test_start_date,'%Y-%m-%d')
    
    weeks = (start_date.date() - test_start_date.date()).days / 7
    
    if weeks > 40: continue
    elif weeks < 0: continue
    elif weeks in [0,1,2,3,4]: 
        if weeks == 0: weeks = 1
        weight = 1 - (weeks * weighting_chart[0])
    elif weeks in [5,6,7,8]: weight =  1.02 - (weeks * weighting_chart[1])
    elif weeks in [9,10,11,12]: weight = 1.06  - (weeks * weighting_chart[2])
    elif weeks > 12 and weeks <= 40: weight = 1.24 - (weeks * weighting_chart[3])
    
    tournament_weights['weights'][test_name] = {}
    tournament_weights['weights'][test_name]['days_before'] = (start_date.date() - test_start_date.date()).days
    tournament_weights['weights'][test_name]['year'] = year
    tournament_weights['weights'][test_name]['weight'] = weight

    # print test_name, (start_date.date() - test_start_date.date()).days, weight


# find earliest tournament
# if earliest tournament is less than 40 weeks * 7 days before, get the previous years schedule and run through the same process
earliest_tournament = schedule['tournaments'][0]
earliest_name = earliest_tournament['name']
earliest_start_date = datetime.datetime.strptime(earliest_tournament['start_date'],'%Y-%m-%d')
earliest_days_before =  (start_date.date() - earliest_start_date.date()).days



if earliest_days_before < num_days:
   
    # get this year's tournament list
    request_key = 'sportsData/' + str(year - 1) + '/schedule.json'
    k = Key(b)
    k.key = request_key
    schedule = k.get_contents_as_string()

    schedule = json.loads(schedule)
    
    for tournament in schedule['tournaments']:
        test_name = tournament['name']
        test_start_date = tournament['start_date']
        test_start_date = datetime.datetime.strptime(test_start_date,'%Y-%m-%d')
        
        weeks = (start_date.date() - test_start_date.date()).days / 7        
        if weeks > 40: continue
        elif weeks < 0: continue
        elif weeks in [0,1,2,3,4]: 
            if weeks == 0: weeks = 1
            weight = 1 - (weeks * weighting_chart[0])
        elif weeks in [5,6,7,8]: weight =  1.02 - (weeks * weighting_chart[1])
        elif weeks in [9,10,11,12]: weight = 1.06  - (weeks * weighting_chart[2])
        elif weeks > 12 and weeks <= 40: weight = 1.24 - (weeks * weighting_chart[3])
        
        tournament_weights['weights'][test_name] = {}
        tournament_weights['weights'][test_name]['year'] = year - 1
        tournament_weights['weights'][test_name]['days_before'] = (start_date.date() - test_start_date.date()).days
        tournament_weights['weights'][test_name]['weight'] = weight  



tournament_weights = json.dumps(tournament_weights)                
                                                
k2 = Key(b)
k2.key = 'weights/' + str(year) + '/' + tournament_name + '/' + 'weights.json'
k2.set_contents_from_string(tournament_weights)
