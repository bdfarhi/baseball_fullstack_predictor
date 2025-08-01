from pybaseball import schedule_and_record
from pybaseball import team_game_logs, standings
import pandas as pd

from bs4 import BeautifulSoup
# df = schedule_and_record(2023, 'NYM')  # NY Mets, 2023
# print(df.columns)


all_year_df = []
year= [2005, 2006, 2007, 2008, 2009,2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
# year= [2005, 2006, 2007]
for y in year:
    teams = ['ARI','ATL','TBR','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET',
             'HOU','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK',
             'PHI','PIT','SDP','SEA','SFG','STL','TEX','TOR','WSN']


    team_dfs = {}
    for team in teams:
        if team == 'TBR' and y < 2008:
            team = 'TBD'
        if team == 'MIA' and y < 2012:
            team = 'FLA'
        # df2 = team_game_logs(2023, 'NYM')
        # print(df2)
        print(y, team)



        df_batting = team_game_logs(y, team, log_type="batting")

        df_pitching = team_game_logs(y, team, log_type="pitching")
        # print(df2.columns)

        df_pitching.rename(columns={'H': 'Hits Allowed', "R":"Runs Allowed", "BB":"Walks Issued", "SO":"Strikouts By Pitching Staff", "HR":"HR Allowed", "HBP":"Our Pitcher Hits Their Batter","CS": "Caught Them Stealing","AB":"Opponents At Bats", "2B":"Doubles Allowed","3B":"Triples Allowed", "SH":"Sacrafice Hits Against", "SF":"Sacrafice Flies Against", "ROE":"Defensive Errors","GDP":"Got Double Play", "NumPlayers":"Number of Pitchers Who Appeared in Game", "SB": "SB Allowed"}, inplace=True)

        df = pd.concat([df_batting, df_pitching],axis=1)

        identical = df['Game'].iloc[:, 0].equals(df['Game'].iloc[:, 1])
        if identical:
            df = df.loc[:, ~df.columns.duplicated()]
        value_columns = df.columns[df.columns == 'Date']

        # Drop the second instance of 'value' (i.e., the second occurrence)
        if len(value_columns) > 1:
            # Find index of second 'value' column
            second_index = [i for i, col in enumerate(df.columns) if col == 'Date'][1]
            df = df.drop(df.columns[second_index], axis=1)
        value_columns = df.columns[df.columns == 'Home']

        # Drop the second instance of 'value' (i.e., the second occurrence)
        if len(value_columns) > 1:
            # Find index of second 'value' column
            second_index = [i for i, col in enumerate(df.columns) if col == 'Home'][1]
            df = df.drop(df.columns[second_index], axis=1)
        value_columns = df.columns[df.columns == 'Opp']
        # print(df.columns)
        # print(df["Rslt"])
        # Drop the second instance of 'value' (i.e., the second occurrence)
        if len(value_columns) > 1:
            # Find index of second 'value' column
            second_index = [i for i, col in enumerate(df.columns) if col == 'Opp'][1]
            df = df.drop(df.columns[second_index], axis=1)
        value_columns = df.columns[df.columns == 'Rslt']

        # Drop the second instance of 'value' (i.e., the second occurrence)
        if len(value_columns) > 1:
            # Find index of second 'value' column
            second_index = [i for i, col in enumerate(df.columns) if col == 'Rslt'][1]
            df = df.drop(df.columns[second_index], axis=1)

        df['Hits per game'] = df["H"].shift(1).cumsum().fillna(0) / df["Game"]-1
        # print(df["Total Hits"])
        # print(df.columns)



        #Need Hits PEr Game, At BAts per game, Runs Scored for Game, doubles per game, Triples per game , Home runs per game etc.
        df["Plate Appearances per game"] = df["PA"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["At Bats per game"] = df["AB"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Runs Scored per game"] = df["R"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Doubles per game"] = df["2B"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Triples per game"] = df["3B"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Home Runs per game"] = df["HR"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["RBI per game"] = df["RBI"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Walks per game"] = df["BB"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Times Struck Out per game"] = df["SO"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Times Hit By Pitch per game"] = df["HBP"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Sacrifice Hits per game"] = df["SH"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Sac Flies per game"] = df["SF"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Reaches on Errors per game"] = df["ROE"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Double Plays Hit Into per game"] = df["GDP"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Stolen Bases per game"] = df["SB"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Times Caught Stealing per game"] = df["CS"].shift(1).cumsum().fillna(0) / df["Game"]-1

        df['Total Hits'] = df["H"].shift(1).cumsum().fillna(0)
        df['Total AB'] = df["AB"].shift(1).cumsum().fillna(0)
        #NEED TO FIX HITS / AB
        df["Total Batting Average"] = df["Total Hits"] / df["Total AB"]
        #Hits + Walks / AB
        df['Total BB'] = df["BB"].shift(1).cumsum().fillna(0)
        df['Total HBP'] = df["HBP"].shift(1).cumsum().fillna(0)
        df['Total SF'] = df["SF"].shift(1).cumsum().fillna(0)
        numerator = df['Total Hits'] + df['Total BB'] + df['Total HBP']
        denominator = df['Total AB'] + df['Total BB'] + df['Total HBP'] + df['Total SF']

        df['Total OBP'] = numerator / denominator

        # Optional: handle division by zero by replacing NaN or inf with 0
        df['Total OBP'] = df['Total OBP'].fillna(0)

        df["Total Doubles"] = df["2B"].shift(1).cumsum().fillna(0)
        df["Total Triples"] = df["3B"].shift(1).cumsum().fillna(0)
        df["Total Home Runs"] = df["HR"].shift(1).cumsum().fillna(0)
        df["Total Singles"] = df["Total Hits"] - (df["Total Doubles"] + df["Total Triples"] + df["Total Home Runs"])
        numerator = (df["Total Singles"] +
                     2 * df["Total Doubles"] +
                     3 * df["Total Triples"] +
                     4 * df["Total Home Runs"])

        denominator = df["Total AB"]

        df["Total SLG"] = numerator / denominator

        # Handle division by zero safely:
        df["Total SLG"] = df["Total SLG"].fillna(0)

        df["Total OPS"] = df["Total OBP"] + df["Total SLG"]

        df["Left On Base per game"] =df["LOB"].shift(1).cumsum().fillna(0)/ df["Game"]-1

        df["Hits Allowed per game"] =df["Hits Allowed"].shift(1).cumsum().fillna(0) /df["Game"]-1
        df["Runs Allowed per game"] =df["Runs Allowed"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Total Earned Runs Allowed"] =df["ER"].shift(1).cumsum().fillna(0)
        df["Earned Runs Allowed per Game"] =df["ER"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Unearned Runs per game"] =df["UER"].shift(1).cumsum().fillna(0)/ df["Game"]-1
        df["Walks Issued per game"] =df["Walks Issued"].shift(1).cumsum().fillna(0)/ df["Game"]-1
        df["Stikeouts By Pitching Staff per game"] =df["Strikouts By Pitching Staff"].shift(1).cumsum().fillna(0)/ df["Game"]-1
        df["HR Allowed per game"] =df["HR Allowed"].shift(1).cumsum().fillna(0)/ df["Game"]-1
        df["Times Mets Pitcher Hits Their Batter per game"] =df["Our Pitcher Hits Their Batter"].shift(1).cumsum().fillna(0)/ df["Game"]-1

        df["IP"] = df["IP"].shift(1).cumsum().fillna(0)
        df["ERA"] = (df["Total Earned Runs Allowed"] / df["IP"]) * 9

        #NEed to Make per game
        df["Batters Faced per game"] = df["BF"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Pitches Thrown per game"] = df["Pit"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Strikes Thrown per game"] = df["Str"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Inherited Runners per game"] = df["IR"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Inherited Runners Scored per game"] = df["IS"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Stolen Bases Allowed per game"] = df["SB Allowed"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Caught Them Stealing per game"] = df["Caught Them Stealing"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Opponent At Bats per game"] = df["Opponents At Bats"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Doubles Allowed per game"] = df["Doubles Allowed"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Triples Allowed per game"] = df["Triples Allowed"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Sacrifice Hits Against per game"] = df["Sacrafice Hits Against"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Sac Flies Against per game"] = df["Sacrafice Flies Against"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Double Plays Got per game"] = df["Got Double Play"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Defensive Errors per game"] = df["Defensive Errors"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df["Number of Pitchers In Game per game"] = df["Number of Pitchers Who Appeared in Game"].shift(1).cumsum().fillna(0) / df["Game"]-1
        df['Rslt'] = df['Rslt'].apply(lambda x: 'W' if 'W' in x else ('L' if 'L' in x else x))
        df["PitchersUsed"] = df["PitchersUsed"].apply(lambda x: x.split(",")[0].split(" ")[0])

        # Transform 'OppStart': take everything before the '('
        df["OppStart"] = df["OppStart"].apply(lambda x: x.split("(")[0])
        df["Starting Pitcher"] = df["PitchersUsed"]
        df['Opp'] = df['Opp'].replace('FLA', 'MIA')
        df['Opp'] = df['Opp'].replace('TBD', 'TBR')


        #Rolling STatisticsdef
        def add_rolling_average(df, source_col, window=10, new_col=None):
        # """
        # Adds a new column to the DataFrame that is the rolling average of the
        # previous `window` values in `source_col`, excluding the current row's value.
        #
        # Parameters:
        # - df: pandas.DataFrame
        # - source_col: str, the column to compute the rolling average on
        # - window: int, number of previous rows to consider
        # - new_col: str or None, name of the new column. If None, defaults to source_col + '_rolling_avg'
        #
        # Returns:
        # - df: pandas.DataFrame with the new column added
        # """
            if new_col is None:
                new_col = f"{source_col}_rolling_avg"

            df[new_col] = df[source_col].shift(1).rolling(window=window).mean()
            return df


        #NEED TO ROLLING WINS
        #
        # df = add_rolling_average(df, source_col="R", new_col=team+ " Runs Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="AB", new_col=team+ " Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="H", new_col=team+ " Hits Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="2B", new_col=team+ " Doubles Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="3B", new_col=team+ " Triples Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="HR", new_col=team+ " HR Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="RBI", new_col=team+ " RBI Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="BB", new_col=team+ " Walks Gotten Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="SO", new_col=team+ " Batters That Struck Out Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="IBB", new_col=team+ " Batters Inentionally Walked Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="SH", new_col=team+ " Sacrafice Hits Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="HBP", new_col=team+ " Batters Hit Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="SF", new_col=team+ " Sacrifice Flies Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="ROE", new_col=team+ " Reached ON Error Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="GDP", new_col=team+ " Batters Grounded Into Double PLays Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="SB", new_col=team+ " Stolen Bases Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="CS", new_col=team+ " Caught Stealing Averaged Last 10 Games")
        #
        # df = add_rolling_average(df, source_col="OBP", new_col=team+ " OBP Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="BA", new_col=team+ " BA Walked Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="OPS", new_col=team+ " OPS Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="SLG", new_col=team+ " SLG Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="LOB", new_col=team+ " LOB Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="ER", new_col=team+ " ER Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="UER", new_col=team+ " UR Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Hits Allowed", new_col=team+ " H Allowed Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Runs Allowed", new_col=team+ " R Allowed Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Walks Issued", new_col=team+ " BB Issued Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Strikouts By Pitching Staff", new_col=team+ " SO By Pitcher Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="HR Allowed", new_col=team+ " HR Allowed Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Our Pitcher Hits Their Batter", new_col=team+ " Our Pitcher Hits Their Batter Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="ERA", new_col=team+ " RA Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="BF", new_col=team+ " BF Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Pit", new_col=team+ " Pit Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Str", new_col=team+ " Str Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="IR", new_col=team+ " IR Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="IS", new_col=team+ " IS Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Opponents At Bats", new_col=team+ " Opponent At Bats Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="SB Allowed", new_col=team+ " SB Allowed Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Caught Them Stealing", new_col=team+ " Caught Them Stealing Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Doubles Allowed", new_col=team+ " 2B Given Up Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Triples Allowed", new_col=team+ " 3B Given Up Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Sacrafice Hits Against", new_col=team+ " Sac H Given Up Averaged Last 10 Games")
        # df = add_rolling_average(df, source_col="Sacrafice Flies Against", new_col=team+ " Sac Flies Given Up Averaged Last 10 Games")
        src_cols = [
            "R", "AB", "H", "2B", "3B", "HR", "RBI", "BB", "SO", "IBB", "SH", "HBP", "SF",
            "ROE", "GDP", "SB", "CS", "OBP", "BA", "OPS", "SLG", "LOB", "ER", "UER",
            "Hits Allowed", "Runs Allowed", "Walks Issued", "Strikouts By Pitching Staff",
            "HR Allowed", "Our Pitcher Hits Their Batter", "ERA", "BF", "Pit", "Str",
            "IR", "IS", "Opponents At Bats", "SB Allowed", "Caught Them Stealing",
            "Doubles Allowed", "Triples Allowed", "Sacrafice Hits Against", "Sacrafice Flies Against"
        ]

        new_cols = [f"{col!s} Averaged Last 10 Games" for col in [
            "Runs", "Averaged Last 10 Games", "Hits", "Doubles", "Triples", "HR",
            "RBI", "Walks Gotten", "Batters That Struck Out", "Batters Inentionally Walked",
            "Sacrafice Hits", "Batters Hit", "Sacrifice Flies", "Reached ON Error",
            "Batters Grounded Into Double PLays", "Stolen Bases", "Caught Stealing",
            "OBP", "BA Walked", "OPS", "SLG", "LOB", "ER", "UR",
            "H Allowed", "R Allowed", "BB Issued", "SO By Pitcher", "HR Allowed",
            "Our Pitcher Hits Their Batter", "RA", "BF", "Pit", "Str", "IR", "IS",
            "Opponent At Bats", "SB Allowed", "Caught Them Stealing",
            "2B Given Up", "3B Given Up", "Sac H Given Up", "Sac Flies Given Up"
        ]]

        # actually compute all rolling means at once
        rolling = (
            df[src_cols]
            .rolling(window=10, min_periods=1)  # or drop min_periods if you want NaNs
            .mean()
            .set_axis(new_cols, axis=1)
        )
        print(df["Starting Pitcher"])
        print(df["OppStart"])

        # concatenate back onto df in one go
        df = pd.concat([df, rolling], axis=1)


        df = df.drop(["PA", "PitchersUsed", "R", "AB", "H", "2B", "3B", "HR", "RBI", "BB", "IBB", "SO", "HBP", "SH",
                      "SF", "ROE", "GDP", "SB", "CS", "BA", "OBP", "SLG", "OPS" , "LOB",
                      "NumPlayers", "Thr","IP", "ER", "UER", "Hits Allowed",
                      "Runs Allowed", "Walks Issued", "Strikouts By Pitching Staff",
                      "HR Allowed", 'Our Pitcher Hits Their Batter', 'ERA',
                      'BF', 'Pit', 'Str', 'IR', 'IS','SB Allowed',
                      'Caught Them Stealing', 'Opponents At Bats','Doubles Allowed',
                      'Triples Allowed', 'Sacrafice Hits Against',
                      'Sacrafice Flies Against',
                      'Number of Pitchers Who Appeared in Game','Umpire',
                      'Total Hits','Total AB','Total BB',
                      'Total HBP', 'Total SF','IP',
                      'Defensive Errors', 'Got Double Play'],axis=1)


        df['win_numeric'] = (df['Rslt'] == 'W').astype(int)
        df["total_wins"]= df["win_numeric"].shift(1).cumsum().fillna(0)

        # Use rolling to count 'W' in the last 10 rows (excluding current)
        df['Wins Last 10'] = df['win_numeric'].shift(1).rolling(window=10, min_periods=1).sum()

        # Optional: drop helper column
        df.drop(columns='win_numeric', inplace=True)

        df['Loss_Num'] = (df['Rslt'] == 'L').astype(int)
        df["total_loss"] = df["Loss_Num"].shift(1).cumsum().fillna(0)

        # Use rolling to count 'W' in the last 10 rows (excluding current)
        df['Losses Last 10'] = df['Loss_Num'].shift(1).rolling(window=10, min_periods=1).sum()

        # Optional: drop helper column
        df.drop(columns='Loss_Num', inplace=True)
        if team != "FLA" or team!="TBD":
            team_dfs[team] = df
        elif team =="FLA":
            team_dfs["MIA"] = df
        elif team =="TBD":
            team_dfs["TBR"] = df

    # print(team_dfs)
    # prins["NYM"].columns)
    # print(team_dfs["NYM"]["Rslt"])t(team_df

    dfs = []
    # print(team_dfs["NYM"]["Home"])
    opp_team = team_dfs["NYM"]["OppStart"]
    for team, df in team_dfs.items():
        df2 = df.copy()
        df2['Team']    = team
        df2['Team'] = df2['Team'].replace('FLA', 'MIA')
        df2['Team'] = df2['Team'].replace('TBD', 'TBR')
        # assume your original df has a column 'Home' containing the home‑team code when they are home
        # if instead you have a boolean you can adapt accordingly
        df2['is_home'] = (df2['Home'])
        dfs.append(df2)

    full = pd.concat(dfs, ignore_index=True)
    print("Full: "+ str(full.shape))
    home = full[full['Home']].reset_index(drop=True)
    print("Home: "+str(home.shape))
    away = full[~full['Home']].reset_index(drop=True)
    print("Away: "+ str(away.shape))
    # for col in ['Date', 'Starting Pitcher', 'OppStart']:
    #     home[col] = home[col].astype(str).str.strip()
    #     away[col] = away[col].astype(str).str.strip()
    #     # if case isn’t significant:
    #     home[col] = home[col].str.upper()
    #     away[col] = away[col].str.upper()
    # merged = pd.merge(
    #     home,
    #     away,
    #     how='inner',
    #     left_on = ['Date', "Team","Opp", "Starting Pitcher", 'OppStart'],
    #     right_on= ['Date',"Opp", "Team", 'OppStart','Starting Pitcher'],
    #     suffixes=('_home', '_away')
    # )
    merged = pd.merge(
        home,
        away,
        how='inner',
        left_on=['Date', 'Starting Pitcher', 'OppStart'],
        right_on=['Date', 'OppStart', 'Starting Pitcher'],
        suffixes=('_home', '_away')
    )
    print("Merged1: "+ str(merged.shape))
    merged = merged[
        (merged['Opp_home'] == merged['Team_away']) &
        (merged['Opp_away'] == merged['Team_home'])
    ]
    print("Merged2: "+ str(merged.shape))
    # what dates do you have in both home and away?
    # common_dates = set(home['Date']) & set(away['Date'])
    # print("Dates in common:", len(common_dates), "examples:", list(common_dates)[:5])
    #
    # # what pitcher names overlap?
    # common_sp = set(home['Starting Pitcher']) & set(away['OppStart'])
    # common_osp = set(home['OppStart']) & set(away['Starting Pitcher'])
    # print("SP vs OppStart overlap:", len(common_sp), "and", len(common_osp))
    # for col in ['Date', 'Starting Pitcher', 'OppStart']:
    #     home[col] = home[col].astype(str).str.strip()
    #     away[col] = away[col].astype(str).str.strip()
    #     # if case isn’t significant:
    #     home[col] = home[col].str.upper()
    #     away[col] = away[col].str.upper()
    #
    #
    # print(home[['Date', 'Starting Pitcher', 'OppStart']].dtypes)
    # print(away[['Date', 'OppStart', 'Starting Pitcher']].dtypes)
    # test = pd.merge(home, away,
    #                 left_on=['Date', 'Starting Pitcher', 'OppStart'],
    #                 right_on=['Date', 'OppStart', 'Starting Pitcher'],
    #                 suffixes=('_h', '_a'),
    #                 how='inner')
    # print(test.head())
    #
    # print(team, "merged shape:", merged.shape)

    all_year_df.append(merged)
all_games = pd.concat(all_year_df, ignore_index=True)
print("all_games: "+ str(all_games.shape))
all_games.to_csv('games_more.csv', index=False)

