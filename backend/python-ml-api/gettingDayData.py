# from pybaseball import team_game_logs
# import pandas as pd
# from datetime import datetime, date,timedelta
# import requests
#
# from bs4 import BeautifulSoup
# import time
# current_year = datetime.now().year
#
# FEATURE_NAMES = [
#     'Plate Appearances per game',
#     'Hits per game',
#     'At Bats per game',
#     'Runs Scored per game',
#     'Doubles per game',
#     'Triples per game',
#     'Home Runs per game',
#     'RBI per game',
#     'Walks per game',
#     'Times Struck Out per game',
#     'Times Hit By Pitch per game',
#     'Sacrifice Hits per game',
#     'Sac Flies per game',
#     'Reaches on Errors per game',
#     'Double Plays Hit Into per game',
#     'Stolen Bases per game',
#     'Times Caught Stealing per game',
#     'Total Batting Average',
#     'Total OBP',
#     'Total OPS',
#     'Total SLG',
#     'Left On Base per game',
#     'Hits Allowed per game',
#     'Runs Allowed per game',
#     'Earned Runs Allowed per Game',
#     'Unearned Runs per game',
#     'Walks Issued per game',
#     'Stikeouts By Pitching Staff per game',
#     'HR Allowed per game',
#     'Times Mets Pitcher Hits Their Batter per game',
#     'Batters Faced per game',
#     # 'Pitches Thrown per game', # Dont Have
#     # 'Strikes Thrown per game', # Dont Have
#     # 'Inherited Runners per game', # Dont HAve
#     # 'Inherited Runners Scored per game', # DOnt have
#     # 'Stolen Bases Allowed per game', # Dont have
#     # 'Caught Them Stealing per game', # Dont have
#     # 'Opponent At Bats per game', # dont Have
#     'Doubles Allowed per game',
#     'Triples Allowed per game',
#     # 'Sacrifice Hits Against per game',#Dont have
#     # 'Sac Flies Against per game',#Dont have
#     'Double Plays Got per game',
#     'Defensive Errors per game',
#     # 'Number of Pitchers In Game per game', # dont have
#     #DONT HAVE ANY AVERAGE YET
#     'Runs Averaged Last 10 Games',
#     # 'Averaged Last 10 Games Averaged Last 10 Games',
#     'Hits Averaged Last 10 Games',
#     'Doubles Averaged Last 10 Games',
#     'Triples Averaged Last 10 Games',
#     'HR Averaged Last 10 Games',
#     'RBI Averaged Last 10 Games',
#     'Walks Gotten Averaged Last 10 Games',
#     'Batters That Struck Out Averaged Last 10 Games',
#     # 'Batters Inentionally Walked Averaged Last 10 Games', # dont have
#     # 'Sacrafice Hits Averaged Last 10 Games', #dont have
#     # 'Batters Hit Averaged Last 10 Games', # dont have
#     # 'Sacrifice Flies Averaged Last 10 Games', #dont have
#     # 'Reached ON Error Averaged Last 10 Games', #maybe
#     # 'Batters Grounded Into Double PLays Averaged Last 10 Games', #dont have
#     'Stolen Bases Averaged Last 10 Games',
#     'Caught Stealing Averaged Last 10 Games',
#     'OBP Averaged Last 10 Games',
#     'BA Walked Averaged Last 10 Games',
#     'OPS Averaged Last 10 Games',
#     'SLG Averaged Last 10 Games',
#     # 'LOB Averaged Last 10 Games', #dont have
#     'ER Averaged Last 10 Games',
#     'UR Averaged Last 10 Games',
#     'H Allowed Averaged Last 10 Games',
#     'R Allowed Averaged Last 10 Games',
#     'BB Issued Averaged Last 10 Games',
#     'SO By Pitcher Averaged Last 10 Games',
#     'HR Allowed Averaged Last 10 Games',
#     'Our Pitcher Hits Their Batter Averaged Last 10 Games',
#     'RA Averaged Last 10 Games',
#     # 'BF Averaged Last 10 Games', #dont have
#     # 'Pit Averaged Last 10 Games',#dont have
#     # 'Str Averaged Last 10 Games',#dont have
#     # 'IR Averaged Last 10 Games',#dont have
#     # 'IS Averaged Last 10 Games',##dont have
#     # 'Opponent At Bats Averaged Last 10 Games', # dont hav e
#     # 'SB Allowed Averaged Last 10 Games',#dont have
#     # 'Caught Them Stealing Averaged Last 10 Games',#dont have
#     # '2B Given Up Averaged Last 10 Games',#domt have
#     # '3B Given Up Averaged Last 10 Games',#dot have
#     # 'Sac H Given Up Averaged Last 10 Games',#dont have
#     # 'Sac Flies Given Up Averaged Last 10 Games',#dont hav e
#     'Wins Last 10',
#     'Losses Last 10',
# ]
# mlb_teams = {
#     "Arizona Diamondbacks": "ARI",
#     "Atlanta Braves": "ATL",
#     "Baltimore Orioles": "BAL",
#     "Boston Red Sox": "BOS",
#     "Chicago White Sox": "CWS",
#     "Chicago Cubs": "CHC",
#     "Cincinnati Reds": "CIN",
#     "Cleveland Guardians": "CLE",
#     "Colorado Rockies": "COL",
#     "Detroit Tigers": "DET",
#     "Houston Astros": "HOU",
#     "Kansas City Royals": "KC",
#     "Los Angeles Angels": "LAA",
#     "Los Angeles Dodgers": "LAD",
#     "Miami Marlins": "MIA",
#     "Milwaukee Brewers": "MIL",
#     "Minnesota Twins": "MIN",
#     "New York Yankees": "NYY",
#     "New York Mets": "NYM",
#     "Athletics": "OAK",
#     "Philadelphia Phillies": "PHI",
#     "Pittsburgh Pirates": "PIT",
#     "San Diego Padres": "SD",
#     "San Francisco Giants": "SF",
#     "Seattle Mariners": "SEA",
#     "St. Louis Cardinals": "STL",
#     "Tampa Bay Rays": "TB",
#     "Texas Rangers": "TEX",
#     "Toronto Blue Jays": "TOR",
#     "Washington Nationals": "WSH"
# }
#
#
# team_batting_stats = {}
# url  ="https://www.baseball-reference.com/leagues/majors/2025.shtml"
# data = requests.get(url)
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
#
#         team = team.split('>')[-2].split('<')[0]
#
#         # print(team)
#         team = mlb_teams[team.strip()]
#         team_stat= []
#         for td in row.find_all('td'):
#             team_stat.append(td.text)
#         team_batting_stats[team] = team_stat
#     i +=1
#
# # print(team_stats)
#
#
#
# #NEEDE TEAM STAT INDICIES:
#
# # R per Game  = 2
# # tot games = 3
# # tot PA = 4
# # tot AB = 5
# # tot R = 6
# # tot H = 7
# # tot 2B= 8
# # 3B = 9
# # tot HR = 10
# # tot RBI = 11
# # SB = 12
# # CS = 13
# #  BB = 14
# #   SO = 15
# #   BA = 16
# #   OBP = 17
# #   SLG = 18
# #   OPS = 19
# #   Grounded into DP = 22
# # HBP = 23
# # Sh= 24
# # SF = 25
# #  IBB = 26
# #  LOB = 27
#
#
#
#
#
# team_pitching_stats = {}
# url  ="https://www.baseball-reference.com/leagues/majors/2025-standard-pitching.shtml"
# data = requests.get(url)
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
#
#         team = team.split('>')[-2].split('<')[0]
#
#         # print(team)
#         team = mlb_teams[team.strip()]
#         team_stat= []
#         for td in row.find_all('td'):
#             team_stat.append(td.text)
#         team_pitching_stats[team] = team_stat
#     i +=1
# # print(team_pitching_stats)
#
#
#
# # Pitching INdicies:
# # Total # pitchers used = 0
# # RA/G = 2
# # Wins = 3
# # Losses = 4
# # ERA = 6
# # Games = 7
# # IP = 14
# # H allowed = 15
# # R allowed = 16
# # ER  = 17
# # UER = R allowed - ER
# # HR allowed = 18
# # Pitcher Walks batter = 19
# # Pitccher IBB = 20
# # Pitcher SO = 21
# # Pitcher HBP = 22
# # Batters Faced = 25
# # LOB = 34
#
# team_adv_pitching_stats = {}
# url  ="https://www.baseball-reference.com/leagues/majors/2025-advanced-pitching.shtml"
# data = requests.get(url)
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
#
#         team = team.split('>')[-2].split('<')[0]
#
#         # print(team)
#         team = mlb_teams[team.strip()]
#         team_stat= []
#         for td in row.find_all('td'):
#             team_stat.append(td.text)
#         team_adv_pitching_stats[team] = team_stat
#     i +=1
# # print(team_adv_pitching_stats)
# #Opponent BA = 0
# #Opp OBP = 1
# # Opp SLG = 2
# # Opp OPS = 3
#
# team_fielding_stats= {}
# url  ="https://www.baseball-reference.com/leagues/majors/2025-advanced-pitching.shtml"
# data = requests.get(url)
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
#
#         team = team.split('>')[-2].split('<')[0]
#
#         # print(team)
#         team = mlb_teams[team.strip()]
#         team_stat= []
#         for td in row.find_all('td'):
#             team_stat.append(td.text)
#         team_fielding_stats[team] = team_stat
#     i +=1
#
#
# # print(team_fielding_stats)
# #
# # errors commited = 10
# # Double Plays Turned =11
#
#
# # end_date = datetime.now() - timedelta(days=1)  # yesterday
# # start_date = end_date - timedelta(days=11)     # 12 days total including yesterday
# #
# # # Format dates as YYYY-MM-DD
# # start_date_str = start_date.strftime("%Y-%m-%d")
# # end_date_str = end_date.strftime("%Y-%m-%d")
# #
# # url = 'https://www.fangraphs.com/leaders/splits-leaderboards?utm_source=chatgpt.com&splitArr=&splitArrPitch=&autoPt=false&splitTeams=false&statType=team&statgroup=1&startDate='+ start_date_str + '&endDate=' + end_date_str + '&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&position=B&sort=23,1'
# url = 'https://www.mlb.com/stats/team?timeframe=-14'
# team_10_batting= {}
#
# data = requests.get(url)
# soup = BeautifulSoup(data.text, 'html.parser')
# pit_table = soup.select('table')[0]
# # print(pit_table)
#
# i = 0
# for team in pit_table.tbody.find_all('span'):
#     if 'full-G_bAyq40' in str(team):
#         team =str(team)
#         team = team.split("<")[-2].split(">")[-1]
#         print(team)
#         team_10_batting[mlb_teams[team.strip()]] = []
#
#     # team_10_batting[mlb_teams[team.text.strip()]] = []
# print(team_10_batting)
# for row in pit_table.tbody.find_all('tr'):
#     # 1) get the <th> with the team link
#     th = row.find('th')
#     team = str(th.find('a'))
#     team = team.split('=')[1].split('class')[0].strip().strip('"').strip('"')
#     print(team)
#     if row is not None and i != 30:
#         for td in row.find_all('td'):
#             team_10_batting[mlb_teams[team.strip()]].append(td.text)
#     i +=1
# print(team_10_batting)
#
#
# #Rolling Avg Hitting
# #Games: 1
# #AB = 2
# # r : 3
# # H : 4
# # 2B: 5
# # 3B: 6
# # HR = 7
# # RBI : 8
# # BB : 9
# # SO : 10
# # SB = 11
# # CS = 12
# # AVG : 13
#
#
# url = 'https://www.mlb.com/stats/team/pitching?timeframe=-14'
# team_10_pit= {}
#
# data = requests.get(url)
# soup = BeautifulSoup(data.text, 'html.parser')
# pit_table = soup.select('table')[0]
# # print(pit_table)
#
# i = 0
# for team in pit_table.tbody.find_all('span'):
#     if 'full-G_bAyq40' in str(team):
#         team =str(team)
#         team = team.split("<")[-2].split(">")[-1]
#         print(team)
#         team_10_pit[mlb_teams[team.strip()]] = []
#
#     # team_10_batting[mlb_teams[team.text.strip()]] = []
# print(team_10_pit)
# for row in pit_table.tbody.find_all('tr'):
#     # 1) get the <th> with the team link
#     th = row.find('th')
#     team = str(th.find('a'))
#     team = team.split('=')[1].split('class')[0].strip().strip('"').strip('"')
#     print(team)
#     if row is not None and i != 30:
#         for td in row.find_all('td'):
#             team_10_pit[mlb_teams[team.strip()]].append(td.text)
#     i +=1
# print(team_10_pit)
#
#
# # ERA : 3
# # IP : 10
# # H Allowed: 11
# # R allowed : 12
# # ER : 13
# # HR ALLowed: 14
# # Hit Batter: 15
# # Wals: 16
# # Strikeouts: 17
# # Opp Avg: 19
# url = 'https://www.mlb.com/standings/mlb'
# team_win= {}
#
# data = requests.get(url)
# soup = BeautifulSoup(data.text, 'html.parser')
# pit_table = soup.select('table')[0]
# # print(pit_table)
#
# i =0
#
#
#
#
#
# for row in pit_table.tbody.find_all('tr'):
#     # 1) get the <th> with the team link
#     th = row.find('th')
#     team = str(th.find('a'))
#     team = team.split('=')[1].split('class')[0].strip().strip('"').strip('"')
#     team = team.split('aria')[0].strip().strip('"')
#     print(team)
#     t = []
#     if row is not None and i != 30:
#         for td in row.find_all('td'):
#             t.append(td.text)
#         team_win[mlb_teams[team.strip()]] = t
#     i +=1
# print(team_win)
#
# #tot wins : 0
# #tot loss: 1
# #Win % : 2
# # Last 1o: 5
# #Streak: 6
#
# m_teams = {
#     "Angels": "LAA",
#     "Astros": "HOU",
#     "Athletics": "OAK",
#     "Blue Jays": "TOR",
#     "Braves": "ATL",
#     "Brewers": "MIL",
#     "Cardinals": "STL",
#     "Cubs": "CHC",
#     "D'backs": "ARI",
#     "Dodgers": "LAD",
#     "Giants": "SF",
#     "Guardians": "CLE",
#     "Mariners": "SEA",
#     "Marlins": "MIA",
#     "Mets": "NYM",
#     "Nationals": "WSH",
#     "Orioles": "BAL",
#     "Padres": "SD",
#     "Phillies": "PHI",
#     "Pirates": "PIT",
#     "Rangers": "TEX",
#     "Rays": "TB",
#     "Red Sox": "BOS",
#     "Reds": "CIN",
#     "Rockies": "COL",
#     "Royals": "KC",
#     "Tigers": "DET",
#     "Twins": "MIN",
#     "White Sox": "CWS",
#     "Yankees": "NYY"
# }
#
# url = 'https://www.baseball-reference.com/previews/'
#
# data = requests.get(url)
# soup = BeautifulSoup(data.text, 'html.parser')
# game_table = soup.select('table.teams')
# team_games = []
# for table in game_table:
#     a = table.tbody.find_all('a')
#     away_team = m_teams[a[0].text]
#     home_team = m_teams[a[2].text]
#     print(home_team + " vs " + away_team)
#     team_games.append([home_team, away_team])
#
# predictor = []
#
# def getTeamStats(team, team_batting_stats, team_pitching_stats, team_fielding_stats, team_10_batting, team_10_pit, team_win):
#     res = []
#     res.append(team_batting_stats[team][4] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][7] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][5] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][2])
#     res.append(team_batting_stats[team][8] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][9] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][10] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][11] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][14] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][15] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][23] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][24] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][25] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][22] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][12] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][13] / team_batting_stats[team][3])
#     res.append(team_batting_stats[team][16])
#     res.append(team_batting_stats[team][17])
#     res.append(team_batting_stats[team][19])
#     res.append(team_batting_stats[team][18])
#     res.append(team_batting_stats[team][27] / team_batting_stats[team][3])
#     res.append(team_pitching_stats[team][15] / team_batting_stats[team][3])
#     res.append(team_pitching_stats[team][2])
#     res.append(team_pitching_stats[team][6])
#     res.append(team_pitching_stats[team][2] - team_pitching_stats[team][6])
#     res.append(team_pitching_stats[team][19] / team_batting_stats[team][3])
#     res.append(team_pitching_stats[team][21] / team_batting_stats[team][3])
#     res.append(team_pitching_stats[team][18] / team_batting_stats[team][3])
#     res.append(team_pitching_stats[team][22] / team_batting_stats[team][3])
#     res.append(team_pitching_stats[team][25] / team_batting_stats[team][3])
#     res.append(team_fielding_stats[team][11] / team_batting_stats[team][3])
#     res.append(team_fielding_stats[team][10] / team_batting_stats[team][3])
#     res.append(team_10_batting[team][3] / team_10_batting[team][1])
#     res.append(team_10_batting[team][4] / team_10_batting[team][1])
#     res.append(team_10_batting[team][5] / team_10_batting[team][1])
#     res.append(team_10_batting[team][6] / team_10_batting[team][1])
#     res.append(team_10_batting[team][7] / team_10_batting[team][1])
#     res.append(team_10_batting[team][8] / team_10_batting[team][1])
#     res.append(team_10_batting[team][9] / team_10_batting[team][1])
#     res.append(team_10_batting[team][10] / team_10_batting[team][1])
#     res.append(team_10_batting[team][11] / team_10_batting[team][1])
#     res.append(team_10_batting[team][12] / team_10_batting[team][1])
#     obp = ((team_10_batting[team][13] * team_10_batting[team][2]) + team_10_batting[team][9]) / (
#                 team_10_batting[team][2] + team_10_batting[team][9])
#     res.append(obp)
#     res.append(team_10_batting[team][13])
#     slg = ((team_10_batting[team][4] - (
#                 team_10_batting[team][5] + team_10_batting[team][6] + team_10_batting[team][7])) + (
#                        2 * team_10_batting[team][5]) + (3 * team_10_batting[team][6]) + (
#                        4 * team_10_batting[team][7])) / (team_10_batting[team][2])
#     res.append(obp + slg)
#     res.append(slg)
#     res.append(team_10_pit[team][13] / team_10_batting[team][1])
#     res.append((team_10_pit[team][12] - team_10_pit[team][13]) / team_10_batting[team][1])
#     res.append(team_10_pit[team][11] / team_10_batting[team][1])
#     res.append(team_10_pit[team][12] / team_10_batting[team][1])
#     res.append(team_10_pit[team][16] / team_10_batting[team][1])
#     res.append(team_10_pit[team][17] / team_10_batting[team][1])
#     res.append(team_10_pit[team][14] / team_10_batting[team][1])
#     res.append(team_10_pit[team][15] / team_10_batting[team][1])
#     res.append(int(team_win[team][5].split("-")[0]))
#     res.append(int(team_win[team][5].split("-")[1]))
#     return res
#
# #
# for game in team_games:
#     home_team, away_team = game[0], game[1]
#
#     home_predictor = getTeamStats(home_team ,team_batting_stats, team_pitching_stats, team_fielding_stats, team_10_batting, team_10_pit, team_win)
#     away_predictor = getTeamStats(away_team, team_batting_stats, team_pitching_stats, team_fielding_stats, team_10_batting, team_10_pit, team_win)
#     i = 0
#     while i < len(home_predictor):
#         predictor[i] = home_predictor[i] - away_predictor[i]



#BIG IMPROVMENTS TO MAKE:
#1. STarting Pther ERA on that DAy: Have starting pitcher name: get ERA at time
#2. Total Wins and total losses On season
#3. Try to find more avg stats

#
#
#
# import pandas as pd
# from datetime import datetime, timedelta
# from pybaseball import schedule_and_record, team_game_logs
# from curl_cffi import requests as curl_requests
# import requests
#
# # === Monkey-patch requests.get ===
# original_get = requests.get
#
# def curl_cffi_get(url, *args, **kwargs):
#     return curl_requests.get(url, impersonate='chrome101')
#
# requests.get = curl_cffi_get
#
# # === Team abbreviations ===
# teams = [
#     'ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET',
#     'HOU', 'KC', 'LAA', 'LAD', 'MIA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK',
#     'PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL', 'TB', 'TEX', 'TOR', 'WSH'
# ]
#
# # === Today's matchups ===
# target_date = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))
# seen_games = set()
# daily_games = []
#
# for team in teams:
#     try:
#         df = schedule_and_record(target_date.year, team)
#         df['Date'] = pd.to_datetime(df['Date'])
#         games_today = df[df['Date'] == target_date]
#
#         for _, row in games_today.iterrows():
#             home_team = team if row['Home_Away'] == 'Home' else row['Opp']
#             away_team = row['Opp'] if row['Home_Away'] == 'Home' else team
#             game = (home_team, away_team)
#             if game not in seen_games:
#                 seen_games.add(game)
#                 daily_games.append(game)
#     except Exception as e:
#         print(f"Error loading schedule for {team}: {e}")
#
# print("Today's MLB games:")
# for game in daily_games:
#     print(game)
#
# # === Load game logs up to yesterday ===
# season_year = datetime.today().year
# end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
#
# print("Loading data...")
# all_logs = []
#
# for team in teams:
#     try:
#         logs = team_game_logs(season_year, team, 'batting')
#         logs['Team'] = team
#         all_logs.append(logs)
#     except Exception as e:
#         print(f"Error loading data for {team}: {e}")
#
# if all_logs:
#     combined_logs = pd.concat(all_logs, ignore_index=True)
#     combined_logs['Date'] = pd.to_datetime(combined_logs['Date'])
#     filtered_logs = combined_logs[combined_logs['Date'] <= end_date]
#
#     # Aggregate stats by team
#     team_stats_dict = {}
#     for team in teams:
#         team_logs = filtered_logs[filtered_logs['Team'] == team]
#         if not team_logs.empty:
#             stat_cols = team_logs.select_dtypes(include='number').columns
#             total_stats = team_logs[stat_cols].sum().tolist()
#             team_stats_dict[team] = total_stats
#         else:
#             team_stats_dict[team] = []
#
#     print("Finished team stats dictionary:")
#     print(team_stats_dict)
#
# # === Restore original requests.get ===
# requests.get = original_get
