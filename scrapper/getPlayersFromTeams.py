import argparse

import requests
import json
import pandas as pd

# Arguments Parser
parser = argparse.ArgumentParser(description="Process general team requests")
parser.add_argument("-f","--filename",type=str,help="write output to FILE",required=True)
parser.add_argument("-s", "--seasons",type=str,help="list of seasons",required=True)
parser.add_argument("-tIds","--teamIds",type=str,help="Team Ids file",required=True)

args = vars(parser.parse_args())
filename=args['filename']
seasons=args['seasons'].split(",")
teamIds=args['teamIds']

columns=['TeamID','PLAYER','PLAYER_ID','POSITION','HEIGHT','WEIGHT','AGE','EXP'] 

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

    return df

teamIdsDF = pd.read_csv(teamIds)

for season in seasons:
    l_filename = filename + \
    "_"+season+ \
    "_" + ".csv"
    playersInfo = pd.DataFrame(columns=columns)    
    for index,row in teamIdsDF.iterrows():
    	playersInfo = playersInfo.append(find_players_from_team(str(row['TEAM_NAME']),str(row['TEAM_ID']),season),ignore_index=True)
    playersInfo.to_csv(l_filename)
