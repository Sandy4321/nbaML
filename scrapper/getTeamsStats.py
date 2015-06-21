import datetime

import argparse

import requests
import json
import pandas as pd

# Arguments Parser
parser = argparse.ArgumentParser(description="Process general team requests")
parser.add_argument("-f","--filename",type=str,help="write output to FILE",required=True)
parser.add_argument("-s", "--seasons",type=str,help="list of seasons",required=True)
parser.add_argument("-st","--seasontypes",type=str,help="list of season types:Regular Season,Playoffs",required=False)
parser.add_argument("-mt","--measuretypes",type=str,help="list of measurement types:Base,Advanced",required=False)

args = vars(parser.parse_args())
filename=args['filename']
seasons=args['seasons'].split(",")
seasontypes=args['seasontypes'].split(",")
measures=args['measuretypes'].split(",")	

def get_teams_stats(measure,season,seasontype,conference=""):  
    url = 'http://stats.nba.com/stats/leaguedashteamstats?' + \
    'Conference='+ conference + \
    '&DateFrom=&DateTo=&Division=&GameScope=' + \
    '&GameSegment=&LastNGames=0&LeagueID=00&Location=' + \
    '&MeasureType=' + measure + \
    '&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust' + \
    '=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=' + \
    '&PlusMinus=N&Rank=N' + \
    '&Season=' + season + \
    '&SeasonSegment=' + \
    '&SeasonType=' + seasontype + \
    '&ShotClockRange=&StarterBench=' + \
    '&TeamID=0&VsConference=&VsDivision='

    #Create Dict based on JSON response
    response = requests.get(url)
    # shots = response.json()['resultSets'][0]['rowSet']
    data = json.loads(response.text)

    #Create df from data and find averages 
    headers = data['resultSets'][0]['headers']
    player_data = data['resultSets'][0]['rowSet']
    df = pd.DataFrame(player_data,columns=headers)
    # df = df[columns]

    l_filename = filename + \
    "_"+measure+"_"+season+"_"+seasontype + \
    "_" +str(datetime.datetime.now()) + ".csv"

    df.to_csv(l_filename)
    print df


for measure in measures:
	for season in seasons:
		for seasontype in seasontypes:
			get_teams_stats(measure,season,seasontype)

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

	# get_teams_stats("Base","2014-15","Regular Season")