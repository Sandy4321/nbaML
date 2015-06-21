import datetime

import argparse

import requests
import json
import pandas as pd

import os
from __init__ import DATA_ROOT

# Arguments Parser
parser = argparse.ArgumentParser(description="Process players leagueleaders")
parser.add_argument("-f","--filename",type=str,help="write output to FILE",required=True)
parser.add_argument("-s", "--seasons",type=str,help="list of seasons",required=True)
parser.add_argument("-st","--seasontypes",type=str,help="list of season types:Regular Season,Playoffs",required=True)
parser.add_argument("-sc","--statcategory",type=str,help="sort by statcategory:MIN,OREB,DREB,REB,AST,STL,BLK,PTS,",required=True)


args = vars(parser.parse_args())
filename=args['filename']
seasons=args['seasons'].split(",")
seasontypes=args['seasontypes'].split(",")
statcategories=args['statcategory'].split(",")

def get_league_leaders_stats(season,seasontype,statcategory="PTS"):  
    url = 'http://stats.nba.com/stats/leagueleaders?' + \
    'LeagueID=00&PerMode=PerGame&Scope=S' + \
    '&Season='+season + \
    '&SeasonType='+seasontype + \
    '&StatCategory='+statcategory

    #Create Dict based on JSON response
    response = requests.get(url)
    # shots = response.json()['resultSets'][0]['rowSet']
    data = json.loads(response.text)

    #Create df from data and find averages 
    headers = data['resultSet']['headers']
    player_data = data['resultSet']['rowSet']
    df = pd.DataFrame(player_data,columns=headers)
    # df = df[columns]

    return df

for season in seasons:
    for seasontype in seasontypes:
        for statcategory in statcategories:
            l_df = get_league_leaders_stats(season,seasontype,statcategory)
            l_filename = filename + "_"+statcategory+"_"+season+"_"+seasontype + \
            "_"+str(datetime.datetime.now()) + ".csv"
            
            l_df.to_csv(l_filename)