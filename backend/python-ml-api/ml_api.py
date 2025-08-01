import re

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV

from datetime import datetime, date,timedelta
import requests

from bs4 import BeautifulSoup, Comment

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI()
cached_predictions = []

# Get current date and time

imputer: SimpleImputer = joblib.load("imputer.pkl")
scaler:  StandardScaler = joblib.load("scaler.pkl")
lr:      LogisticRegression = joblib.load("lr_model.pkl")
svm:     SVC = joblib.load("svm_model.pkl")
mlp:     MLPClassifier = joblib.load("mlp_model.pkl")



#BIG IMPROVMENTS TO MAKE:
#1. STarting Pther ERA on that DAy: Have starting pitcher name: get ERA at time
#2. Total Wins and total losses On season
#3. Try to find more avg stats

mlb_teams = {
    "Arizona Diamondbacks": "ARI",
    "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS",
    "Chicago White Sox": "CWS",
    "Chicago Cubs": "CHC",
    "Cincinnati Reds": "CIN",
    "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL",
    "Detroit Tigers": "DET",
    "Houston Astros": "HOU",
    "Kansas City Royals": "KC",
    "Los Angeles Angels": "LAA",
    "Los Angeles Dodgers": "LAD",
    "Miami Marlins": "MIA",
    "Milwaukee Brewers": "MIL",
    "Minnesota Twins": "MIN",
    "New York Yankees": "NYY",
    "New York Mets": "NYM",
    "Athletics": "OAK",
    "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SD",
    "San Francisco Giants": "SF",
    "Seattle Mariners": "SEA",
    "St. Louis Cardinals": "STL",
    "Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX",
    "Toronto Blue Jays": "TOR",
    "Washington Nationals": "WSH"
}

def get_team_stats():
    def clean_team_name(s):
        # 1. Remove leading and trailing digits
        s = s.strip()  # remove surrounding spaces

        # Remove digits from start and end
        s = re.sub(r'^\d+|\d+$', '', s).strip()

        return s

    fix = {
        "Arizona DiamondbacksD-backs": "Arizona Diamondbacks",
        "Atlanta BravesBraves": "Atlanta Braves",
        "Baltimore OriolesOrioles": "Baltimore Orioles",
        "Boston Red SoxRed Sox": "Boston Red Sox",
        "Chicago CubsCubs": "Chicago Cubs",
        "Chicago White SoxWhite Sox": "Chicago White Sox",
        "Cincinnati RedsReds": "Cincinnati Reds",
        "Cleveland GuardiansGuardians": "Cleveland Guardians",
        "Colorado RockiesRockies": "Colorado Rockies",
        "Detroit TigersTigers": "Detroit Tigers",
        "Houston AstrosAstros": "Houston Astros",
        "Kansas City RoyalsRoyals": "Kansas City Royals",
        "Los Angeles AngelsAngels": "Los Angeles Angels",
        "Los Angeles DodgersDodgers": "Los Angeles Dodgers",
        "Miami MarlinsMarlins": "Miami Marlins",
        "Milwaukee BrewersBrewers": "Milwaukee Brewers",
        "Minnesota TwinsTwins": "Minnesota Twins",
        "New York MetsMets": "New York Mets",
        "New York YankeesYankees": "New York Yankees",
        "Oakland AthleticsAthletics": "Oakland Athletics",
        "Philadelphia PhilliesPhillies": "Philadelphia Phillies",
        "Pittsburgh PiratesPirates": "Pittsburgh Pirates",
        "San Diego PadresPadres": "San Diego Padres",
        "San Francisco GiantsGiants": "San Francisco Giants",
        "Seattle MarinersMariners": "Seattle Mariners",
        "St. Louis CardinalsCardinals": "St. Louis Cardinals",
        "Tampa Bay RaysRays": "Tampa Bay Rays",
        "Texas RangersRangers": "Texas Rangers",
        "Toronto Blue JaysBlue Jays": "Toronto Blue Jays",
        "Washington NationalsNationals": "Washington Nationals",
    }

    m_teams = {
        "Angels": "LAA",
        "Astros": "HOU",
        "Athletics": "OAK",
        "Blue Jays": "TOR",
        "Braves": "ATL",
        "Brewers": "MIL",
        "Cardinals": "STL",
        "Cubs": "CHC",
        "D'backs": "ARI",
        "Dodgers": "LAD",
        "Giants": "SF",
        "Guardians": "CLE",
        "Mariners": "SEA",
        "Marlins": "MIA",
        "Mets": "NYM",
        "Nationals": "WSH",
        "Orioles": "BAL",
        "Padres": "SD",
        "Phillies": "PHI",
        "Pirates": "PIT",
        "Rangers": "TEX",
        "Rays": "TB",
        "Red Sox": "BOS",
        "Reds": "CIN",
        "Rockies": "COL",
        "Royals": "KC",
        "Tigers": "DET",
        "Twins": "MIN",
        "White Sox": "CWS",
        "Yankees": "NYY"
    }

    url = "https://www.mlb.com/stats/team"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    html = requests.get(url, headers=headers).text

    from io import StringIO
    df = pd.read_html(StringIO(html))[0]

    df['TEAMTEAM'] = df['TEAMTEAM'].apply(clean_team_name)
    for key, val in fix.items():
        df.loc[df['TEAMTEAM'].str.contains(key, na=False), 'TEAMTEAM'] = val
    df.rename(columns={'TEAMTEAM': 'Team', "GG": "G", "ABAB": "AB", "RR": "R", "HH": "H", "2B2B": "2B", "3B3B": "3B",
                       "SBSB": "SB", "CSCS": "CS", 'caret-upcaret-downHRcaret-upcaret-downHR': "HR", "RBIRBI": "RBI",
                       "BBBB": "BB", "SOSO": "SO", "AVGAVG": "AVG", "OBPOBP": "OBP", "SLGSLG": "SLG", "OPSOPS": "OPS"},
              inplace=True)
    for key, val in mlb_teams.items():
        df.loc[df['Team'].str.contains(key, na=False), 'Team'] = val
    team_batting_stats = df.set_index('Team').apply(lambda row: row.tolist(), axis=1).to_dict()
    # print(team_batting_stats)
    # Games : 1
    # AB: 2
    # R : 3
    # H : 4
    # 2b: 5
    # 3b : 6
    # hr : 7
    # rbi : 8
    # bb :
    # 9
    # so : 10
    # sb : 11
    # cs : 12
    # avg : 13
    # obp : 14
    # slg : 15
    # ops : 16

    url = "https://www.mlb.com/stats/team/pitching"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    html = requests.get(url, headers=headers).text

    df = pd.read_html(html)[0]
    print(df)
    df['TEAMTEAM'] = df['TEAMTEAM'].apply(clean_team_name)
    for key, val in fix.items():
        df.loc[df['TEAMTEAM'].str.contains(key, na=False), 'TEAMTEAM'] = val
    df.rename(columns={'TEAMTEAM': 'Team', "GG": "G", "ABAB": "AB", "RR": "R", "HH": "H", "2B2B": "2B", "3B3B": "3B",
                       "SBSB": "SB", "CSCS": "CS", 'caret-upcaret-downHRcaret-upcaret-downHR': "HR", "RBIRBI": "RBI",
                       "BBBB": "BB", "SOSO": "SO", "AVGAVG": "AVG", "OBPOBP": "OBP", "SLGSLG": "SLG", "OPSOPS": "OPS"},
              inplace=True)
    for key, val in mlb_teams.items():
        df.loc[df['Team'].str.contains(key, na=False), 'Team'] = val
    team_pitching_stats = df.set_index('Team').apply(lambda row: row.tolist(), axis=1).to_dict()
    # print(team_pitching_stats)
    # wins : 1
    # losses : 2
    # era : 3
    # games : 4
    # complete games : 6
    # shutouts : 7
    # saves : 8
    # save oppotunities : 9
    #  ip : 10
    #  h allowed : 11
    # r allowed : 12
    # er : 13
    # hr allowed : 14
    # Hit batsman : 15
    #
    # walks : 16
    # so : 17
    # whip : 18
    # avg : 19

    # team_batting_stats = {}
    # url  ="https://www.baseball-reference.com/leagues/majors/2025-standard-batting.shtml"
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    # data = requests.get(url, headers=headers)
    # soup = BeautifulSoup(data.text, 'html.parser')
    # batting_table = soup.select('table.sortable')

    # print(len(batting_table))

    # batting_table = batting_table[0]
    # i = 0
    # for row in batting_table.tbody.find_all('tr'):
    #     # 1) get the <th> with the team link
    #     # th = row.find('th', {'data-stat': 'team_name'})
    #     if row is not None and i != 30:
    #         team = str(row.find('th').find('a'))

    #         team = team.split('>')[-2].split('<')[0]

    #         # print(team)
    #         team = mlb_teams[team.strip()]
    #         team_stat= []
    #         for td in row.find_all('td'):
    #             team_stat.append(td.text)
    #         team_batting_stats[team] = team_stat
    #     i +=1

    # print(team_stats)

    #NEEDE TEAM STAT INDICIES:

    # R per Game  = 2
    # tot games = 3
    # tot PA = 4   # CANT GET
    # tot AB = 5
    # tot R = 6
    # tot H = 7
    # tot 2B= 8
    # 3B = 9
    # tot HR = 10
    # tot RBI = 11
    # SB = 12
    # CS = 13 #CANT GET
    #  BB = 14
    #   SO = 15
    #   BA = 16
    #   OBP = 17
    #   SLG = 18
    #   OPS = 19
    #   Grounded into DP = 22  #DONT HAVE
    # HBP = 23 #DONT HAVE
    # Sh= 24 #DONT HAVE ANY BELOW
    # SF = 25
    #  IBB = 26
    #  LOB = 27





    # team_pitching_stats = {}
    # url  ="https://www.baseball-reference.com/leagues/majors/2025-standard-pitching.shtml"
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    # data = requests.get(url, headers=headers)
    # soup = BeautifulSoup(data.text, 'html.parser')
    # pit_table = soup.select('table.sortable')
    # # print(len(pit_table))
    # pit_table = pit_table[0]
    # i = 0
    # for row in pit_table.tbody.find_all('tr'):
    #     # 1) get the <th> with the team link
    #     # th = row.find('th', {'data-stat': 'team_name'})
    #     if row is not None and i != 30:
    #         team = str(row.find('th').find('a'))

    #         team = team.split('>')[-2].split('<')[0]

    #         # print(team)
    #         team = mlb_teams[team.strip()]
    #         team_stat= []
    #         for td in row.find_all('td'):
    #             team_stat.append(td.text)
    #         team_pitching_stats[team] = team_stat
    #     i +=1
    # # print(team_pitching_stats)



    # Pitching INdicies:
    # Total # pitchers used = 0
    # RA/G = 2
    # Wins = 3
    # Losses = 4
    # ERA = 6
    # Games = 7
    # IP = 14
    # H allowed = 15
    # R allowed = 16
    # ER  = 17
    # UER = R allowed - ER
    # HR allowed = 18
    # Pitcher Walks batter = 19
    # Pitccher IBB = 20
    # Pitcher SO = 21
    # Pitcher HBP = 22
    # Batters Faced = 25
    # LOB = 34

    # team_adv_pitching_stats = {}
    # url  ="https://www.baseball-reference.com/leagues/majors/2025-advanced-pitching.shtml"
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    # data = requests.get(url, headers=headers)
    # soup = BeautifulSoup(data.text, 'html.parser')
    # pit_table = soup.select('table.sortable')
    # # print(len(pit_table))
    # pit_table = pit_table[0]
    # i = 0
    # for row in pit_table.tbody.find_all('tr'):
    #     # 1) get the <th> with the team link
    #     # th = row.find('th', {'data-stat': 'team_name'})
    #     if row is not None and i != 30:
    #         team = str(row.find('th').find('a'))

    #         team = team.split('>')[-2].split('<')[0]

    #         # print(team)
    #         team = mlb_teams[team.strip()]
    #         team_stat= []
    #         for td in row.find_all('td'):
    #             team_stat.append(td.text)
    #         team_adv_pitching_stats[team] = team_stat
    #     i +=1
    # print(team_adv_pitching_stats)
    #Opponent BA = 0
    #Opp OBP = 1
    # Opp SLG = 2
    # Opp OPS = 3

    # team_fielding_stats= {}
    # url  ="https://www.baseball-reference.com/leagues/majors/2025-standard-fielding.shtml"
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    # data = requests.get(url, headers=headers)
    # soup = BeautifulSoup(data.text, 'html.parser')
    # pit_table = soup.select('table.sortable')
    # # print(len(pit_table))
    # pit_table = pit_table[0]
    # i = 0
    # for row in pit_table.tbody.find_all('tr'):
    #     # 1) get the <th> with the team link
    #     # th = row.find('th', {'data-stat': 'team_name'})
    #     if row is not None and i != 30:
    #         team = str(row.find('th').find('a'))

    #         team = team.split('>')[-2].split('<')[0]

    #         # print(team)
    #         team = mlb_teams[team.strip()]
    #         team_stat= []
    #         for td in row.find_all('td'):
    #             team_stat.append(td.text)
    #         team_fielding_stats[team] = team_stat
    #     i +=1


    # print(team_fielding_stats)
    #
    # errors commited = 10
    # Double Plays Turned =11


    # end_date = datetime.now() - timedelta(days=1)  # yesterday
    # start_date = end_date - timedelta(days=11)     # 12 days total including yesterday
    #
    # # Format dates as YYYY-MM-DD
    # start_date_str = start_date.strftime("%Y-%m-%d")
    # end_date_str = end_date.strftime("%Y-%m-%d")
    #
    # url = 'https://www.fangraphs.com/leaders/splits-leaderboards?utm_source=chatgpt.com&splitArr=&splitArrPitch=&autoPt=false&splitTeams=false&statType=team&statgroup=1&startDate='+ start_date_str + '&endDate=' + end_date_str + '&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&position=B&sort=23,1'
    url = 'https://www.mlb.com/stats/team?timeframe=-14'
    team_10_batting= {}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    pit_table = soup.select('table')[0]
    # print(pit_table)

    i = 0
    for team in pit_table.tbody.find_all('span'):
        if 'full-G_bAyq40' in str(team):
            team =str(team)
            team = team.split("<")[-2].split(">")[-1]
            # print(team)
            team_10_batting[mlb_teams[team.strip()]] = []

        # team_10_batting[mlb_teams[team.text.strip()]] = []
    # print(team_10_batting)
    for row in pit_table.tbody.find_all('tr'):
        # 1) get the <th> with the team link
        th = row.find('th')
        team = str(th.find('a'))
        team = team.split('=')[1].split('class')[0].strip().strip('"').strip('"')
        # print(team)
        if row is not None and i != 30:
            for td in row.find_all('td'):
                team_10_batting[mlb_teams[team.strip()]].append(td.text)
        i +=1
    # print(team_10_batting)


    #Rolling Avg Hitting
    #Games: 1
    #AB = 2
    # r : 3
    # H : 4
    # 2B: 5
    # 3B: 6
    # HR = 7
    # RBI : 8
    # BB : 9
    # SO : 10
    # SB = 11
    # CS = 12
    # AVG : 13



# TEAM PITCHING LAST 10
#     url = 'https://www.mlb.com/stats/team/pitching?timeframe=-14'
#     team_10_pit= {}

#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
#     data = requests.get(url, headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')
#     pit_table = soup.select('table')[0]
#     # print(pit_table)

#     i = 0
#     for team in pit_table.tbody.find_all('span'):
#         if 'full-G_bAyq40' in str(team):
#             team =str(team)
#             team = team.split("<")[-2].split(">")[-1]
#             # print(team)
#             team_10_pit[mlb_teams[team.strip()]] = []

#         # team_10_batting[mlb_teams[team.text.strip()]] = []
#     # print("sfddd")
#     # print(pit_table.tbody.find_all('tr'))
#     for row in pit_table.tbody.find_all('tr'):
#         # 1) get the <th> with the team link
#         th = row.find('th')
#         team = str(th.find('a'))
#         team = team.split('=')[1].split('class')[0].strip().strip('"').strip('"')
#         print("team: "+ team)
  
#         if row is not None and i != 30:
   
#             #td is only the row of the astros stats 
#             #not getting all other teams stats 
#             print(row)
#             for td in row.find_all('td'):
  
#                 team_10_pit[mlb_teams[team.strip()]].append(td.text)
#         i +=1





        # print(team_10_pit)


        # ERA : 3
        # IP : 10
        # H Allowed: 11
        # R allowed : 12
        # ER : 13
        # HR ALLowed: 14
        # Hit Batter: 15
        # Wals: 16
        # Strikeouts: 17
        # Opp Avg: 19
        url = 'https://www.mlb.com/standings/mlb'
        team_win= {}

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        pit_table = soup.select('table')[0]
        # print(pit_table)

        i =0





        for row in pit_table.tbody.find_all('tr'):
            # 1) get the <th> with the team link
            th = row.find('th')
            team = str(th.find('a'))
            team = team.split('=')[1].split('class')[0].strip().strip('"').strip('"')
            team = team.split('aria')[0].strip().strip('"')
            # print(team)
            t = []
            if row is not None and i != 30:
                for td in row.find_all('td'):
                    t.append(td.text)
                team_win[mlb_teams[team.strip()]] = t
            i +=1
    # print(team_win)

    #tot wins : 0
    #tot loss: 1
    #Win % : 2
    # Last 1o: 5
    #Streak: 6
    # return team_batting_stats, team_pitching_stats, team_10_batting, team_10_pit, team_win
    return team_batting_stats, team_pitching_stats, team_10_batting, team_win

def get_todays_games():
    m_teams = {
        "Angels": "LAA",
        "Astros": "HOU",
        "Athletics": "OAK",
        "Blue Jays": "TOR",
        "Braves": "ATL",
        "Brewers": "MIL",
        "Cardinals": "STL",
        "Cubs": "CHC",
        "D'backs": "ARI",
        "Dodgers": "LAD",
        "Giants": "SF",
        "Guardians": "CLE",
        "Mariners": "SEA",
        "Marlins": "MIA",
        "Mets": "NYM",
        "Nationals": "WSH",
        "Orioles": "BAL",
        "Padres": "SD",
        "Phillies": "PHI",
        "Pirates": "PIT",
        "Rangers": "TEX",
        "Rays": "TB",
        "Red Sox": "BOS",
        "Reds": "CIN",
        "Rockies": "COL",
        "Royals": "KC",
        "Tigers": "DET",
        "Twins": "MIN",
        "White Sox": "CWS",
        "Yankees": "NYY"
    }

    url = 'https://www.baseball-reference.com/previews/'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    game_table = soup.select('table.teams')
    team_games = []
    for table in game_table:
        a = table.tbody.find_all('a')
        away_team = m_teams[a[0].text]
        home_team = m_teams[a[2].text]
        # print(home_team + " vs " + away_team)
        team_games.append([home_team, away_team])
    return team_games

def get_todays_games():
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    response = requests.get(url)
    data = response.json()

    matchups = []
    for event in data['events']:
        competitors = event['competitions'][0]['competitors']
        home = next(team['team']['abbreviation'] for team in competitors if team['homeAway'] == 'home')
        away = next(team['team']['abbreviation'] for team in competitors if team['homeAway'] == 'away')
        matchups.append((home, away))
    
    return matchups


def getTeamStats(team, team_batting_stats, team_pitching_stats, team_10_batting,  team_win):
    res = []
    res.append(float(team_batting_stats[team][4]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][2]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][3]) / float(team_batting_stats[team][1]))
    # Raw count
    res.append(float(team_batting_stats[team][5]) / float(team_batting_stats[team][1]))
    # More ratios
    res.append(float(team_batting_stats[team][6]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][7]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][8]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][9]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][10]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][11]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][12]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][13]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][14]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][16]) / float(team_batting_stats[team][1]))
    res.append(float(team_batting_stats[team][15]) / float(team_batting_stats[team][1]))

    # Pitching stats per game
    res.append(float(team_pitching_stats[team][11]) / float(team_batting_stats[team][1]))
    res.append(float(team_pitching_stats[team][12]) / float(team_batting_stats[team][1]))
    res.append(float(team_pitching_stats[team][3]))
    # Difference
    res.append(float(team_pitching_stats[team][12]) - float(team_pitching_stats[team][13]))
    # More pitching ratios
    res.append(float(team_pitching_stats[team][16]) / float(team_batting_stats[team][1]))
    res.append(float(team_pitching_stats[team][17]) / float(team_batting_stats[team][1]))
    res.append(float(team_pitching_stats[team][14]) / float(team_batting_stats[team][1]))
    res.append(float(team_pitching_stats[team][15]) / float(team_batting_stats[team][1]))

    # Fielding ratios per game
  # Last 10 games batting averages
    # res.append(float(team_10_batting[team][3]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][4]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][5]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][6]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][7]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][8]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][9]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][10]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][11]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_batting[team][12]) / float(team_10_batting[team][1]))
    # # On-base percentage (float)
    # obp = ((float(team_10_batting[team][13]) * float(team_10_batting[team][2])) + float(team_10_batting[team][9])) / (
    #             float(team_10_batting[team][2]) + float(team_10_batting[team][9]))
    # res.append(obp)
    # res.append(float(team_10_batting[team][13]))
    # # Slugging and OPS as floats
    # slg = ((float(team_10_batting[team][4]) - (
    #             float(team_10_batting[team][5]) + float(team_10_batting[team][6]) + float(
    #         team_10_batting[team][7]))) + (2 * float(team_10_batting[team][5])) + (
    #                    3 * float(team_10_batting[team][6])) + (4 * float(team_10_batting[team][7]))) / float(
    #     team_10_batting[team][2])
    # res.append(obp + slg)
    # res.append(slg)


# TEAM 10 PITCHING APPEND 
    # print("eam_10_pit: " + str(len(team_10_pit[team])))
    # print(team_10_pit[team])
    # # Last 10 games pitching ratios
    # res.append(float(team_10_pit[team][13]) / float(team_10_batting[team][1]))
    # res.append((float(team_10_pit[team][12]) - float(team_10_pit[team][13])) / float(team_10_batting[team][1]))
    # res.append(float(team_10_pit[team][11]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_pit[team][12]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_pit[team][16]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_pit[team][17]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_pit[team][14]) / float(team_10_batting[team][1]))
    # res.append(float(team_10_pit[team][15]) / float(team_10_batting[team][1]))




    res.append(int(team_win[team][5].split("-")[0]))
    res.append(int(team_win[team][5].split("-")[1]))
    return res

# acc = {'All Models Same' : [], "2 Models Same"}

def predict_with_models(diff_vec: list) -> int:
    """
    diff_vec: a list of 56 feature‐differences (home - away)
    Returns: 1 if home team wins, 0 if away team wins.
    """
    x = np.array(diff_vec, dtype=float).reshape(1, -1)
    x_imp = imputer.transform(x)
    x_scl = scaler.transform(x_imp)

    # We already loaded lr, svm, mlp. Do majority vote:
    lr_pred = int(lr.predict(x_scl)[0])
    svm_pred = int(svm.predict(x_scl)[0])
    nn_pred  = int(mlp.predict(x_scl)[0])

    vote_sum = lr_pred + svm_pred + nn_pred
    if vote_sum == 3:
        return 1
    elif vote_sum == 0:
        return 0
    else:
        # In case of 2‐1 split, tie‐break however you prefer. For example, pick “home” if lr+svm >=2:
        return 1 if (lr_pred + svm_pred) >= 2 else 0
#

# class GamePreview(BaseModel):
#     home: str
#     away: str
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

class MatchupRequest(BaseModel):
    team1: str
    team2: str

class MatchupResponse(BaseModel):
    winner: str

def predict_winner(team1: str, team2: str) -> str:

    team_batting_stats, team_pitching_stats, team_10_batting,  team_win = get_team_stats()
    

    home_vec = getTeamStats(team1, team_batting_stats, team_pitching_stats,  team_10_batting,  team_win)
    away_vec = getTeamStats(team2, team_batting_stats, team_pitching_stats,  team_10_batting,  team_win)
    diff_vec = [h - a for h, a in zip(home_vec, away_vec)]

    result = predict_with_models(diff_vec)  # or your voting logic
    return team1 if result==1 else team2

@app.post("/predict", response_model=MatchupResponse)
async def predict(matchup: MatchupRequest):
    winner = predict_winner(matchup.team1, matchup.team2)
    return MatchupResponse(winner=winner)

