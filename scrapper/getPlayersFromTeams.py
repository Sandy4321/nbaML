import requests
import json
import pandas as pd

seasons = {'2010-11','2011-12','2012-13','2013-14','2014-15'}
teamIds = {'chicago bulls':'1610612741'}

columns=['TeamID','PLAYER','PLAYER_ID','POSITION','HEIGHT','WEIGHT','AGE','EXP'] 
players_details = {'Team':None,'TeamID':None,'PLAYER':None,'PLAYER_ID':None,'POSITION':None,'HEIGHT':None,'WEIGHT':None,'AGE':None,'EXP':None}

def find_players_from_team(team,team_id,season):  
    url = 'http://stats.nba.com/stats/commonteamroster?'+ \
    'LeagueID=00&Season='+season+'&TeamID='+team_id
    
    #Create Dict based on JSON response
    response = requests.get(url)
    # shots = response.json()['resultSets'][0]['rowSet']
    data = json.loads(response.text)

    #Create df from data and find averages 
    headers = data['resultSets'][0]['headers']
    player_data = data['resultSets'][0]['rowSet']
    df = pd.DataFrame(player_data,columns=headers)
    df = df[columns]

    print df


 	# players_details['Team']=team

	# for header in players_details:

    # avg_def = df['CLOSE_DEF_DIST'].mean(axis=1)
    # avg_dribbles = df['DRIBBLES'].mean(axis=1)
    # avg_shot_distance = df['SHOT_DIST'].mean(axis=1)
    # avg_touch_time = df['TOUCH_TIME'].mean(axis=1)

    # #add Averages to dictionary then to list
    # player_stats['name'] = name
    # player_stats['avg_defender_distance']=avg_def
    # player_stats['avg_shot_distance'] = avg_shot_distance
    # player_stats['avg_touch_time'] = avg_touch_time
    # player_stats['avg_dribbles'] = avg_dribbles
    # players.append(player_stats.copy())

for season in seasons:
	for name in teamIds:
		find_players_from_team(name,teamIds[name],season)