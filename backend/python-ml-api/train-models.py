import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

# 1) Load your CSV once:
df = pd.read_csv("games.csv")
# … (all the diff features, mapping, etc. exactly as in your existing code) …

# 2) Build X, y, and split:

FEATURE_NAMES = [
    # 'Plate Appearances per game_diff',
    'Hits per game_diff',
    "At Bats per game_diff",
    "Runs Scored per game_diff",
    "Doubles per game_diff",
    "Triples per game_diff",
    "Home Runs per game_diff",
    "RBI per game_diff",
    "Walks per game_diff",
    "Times Struck Out per game_diff",
    # "Times Hit By Pitch per game_diff",
    #
    # "Sacrifice Hits per game_diff",
    # "Sac Flies per game_diff",

    # "Reaches on Errors per game_diff",
    # "Double Plays Hit Into per game_diff",
    "Stolen Bases per game_diff",
    "Times Caught Stealing per game_diff",
    "Total Batting Average_diff",
    "Total OBP_diff",
    "Total OPS_diff",
    "Total SLG_diff",
    # 'Left On Base per game_diff',
    'Hits Allowed per game_diff',
    'Runs Allowed per game_diff',
    'Earned Runs Allowed per Game_diff',
    'Unearned Runs per game_diff',
    'Walks Issued per game_diff',
    'Stikeouts By Pitching Staff per game_diff',
    'HR Allowed per game_diff',
    'Times Mets Pitcher Hits Their Batter per game_diff',
    # 'Batters Faced per game_diff',
    # 'Pitches Thrown per game_diff',
    # 'Strikes Thrown per game_diff',
    # 'Inherited Runners per game_diff',
    # 'Inherited Runners Scored per game_diff',
    # 'Stolen Bases Allowed per game_diff',
    # 'Caught Them Stealing per game_diff',
    # 'Opponent At Bats per game_diff',
    # 'Doubles Allowed per game_diff',
    # 'Triples Allowed per game_diff',
    # 'Sacrifice Hits Against per game_diff',
    # 'Sac Flies Against per game_diff',
    # 'Double Plays Got per game_diff',
    # 'Defensive Errors per game_diff',
    # 'Number of Pitchers In Game per game_diff',
    # 'Runs Averaged Last 10 Games_diff',
    # # 'Averaged Last 10 Games Averaged Last 10 Games_diff',
    # 'Hits Averaged Last 10 Games_diff',
    # 'Doubles Averaged Last 10 Games_diff',
    # 'Triples Averaged Last 10 Games_diff',
    # 'HR Averaged Last 10 Games_diff',
    # 'RBI Averaged Last 10 Games_diff',
    # 'Walks Gotten Averaged Last 10 Games_diff',
    # 'Batters That Struck Out Averaged Last 10 Games_diff',
    # # 'Batters Inentionally Walked Averaged Last 10 Games_diff',
    # # 'Sacrafice Hits Averaged Last 10 Games_diff',
    # # 'Batters Hit Averaged Last 10 Games_diff',
    # # 'Sacrifice Flies Averaged Last 10 Games_diff',
    # # 'Reached ON Error Averaged Last 10 Games_diff',
    # # 'Batters Grounded Into Double PLays Averaged Last 10 Games_diff',
    # 'Stolen Bases Averaged Last 10 Games_diff',
    # 'Caught Stealing Averaged Last 10 Games_diff',
    # 'OBP Averaged Last 10 Games_diff',
    # 'BA Walked Averaged Last 10 Games_diff',
    # 'OPS Averaged Last 10 Games_diff',
    # 'SLG Averaged Last 10 Games_diff',
    # 'LOB Averaged Last 10 Games_diff',


# TEAM 10 PIT
#     'ER Averaged Last 10 Games_diff',
#     'UR Averaged Last 10 Games_diff',
#     'H Allowed Averaged Last 10 Games_diff',
#     'R Allowed Averaged Last 10 Games_diff',
#     'BB Issued Averaged Last 10 Games_diff',
#     'SO By Pitcher Averaged Last 10 Games_diff',
#     'HR Allowed Averaged Last 10 Games_diff',
#     'Our Pitcher Hits Their Batter Averaged Last 10 Games_diff',




    # 'RA Averaged Last 10 Games_diff',
    # 'BF Averaged Last 10 Games_diff',
    # 'Pit Averaged Last 10 Games_diff',
    # 'Str Averaged Last 10 Games_diff',
    # 'IR Averaged Last 10 Games_diff',
    # 'IS Averaged Last 10 Games_diff',
    # 'Opponent At Bats Averaged Last 10 Games_diff',
    # 'SB Allowed Averaged Last 10 Games_diff',
    # 'Caught Them Stealing Averaged Last 10 Games_diff',
    # '2B Given Up Averaged Last 10 Games_diff',
    # '3B Given Up Averaged Last 10 Games_diff',
    # 'Sac H Given Up Averaged Last 10 Games_diff',
    # 'Sac Flies Given Up Averaged Last 10 Games_diff',
    'Wins Last 10_diff',
    'Losses Last 10_diff',

]
for diff_name in FEATURE_NAMES:
    # strip off the trailing "_diff" to get the common base
    base = diff_name.replace('_diff', '')

    home_col = f"{base}_home"
    away_col = f"{base}_away"

    # sanity check: make sure both exist
    if home_col in df.columns and away_col in df.columns:
        df[diff_name] = df[home_col] - df[away_col]
    else:
        missing = [c for c in (home_col, away_col) if c not in df.columns]
        raise KeyError(f"Missing columns for `{diff_name}`: {missing}")

df['Rslt_home'] = df['Rslt_home'].map({'W': 1, 'L': 0})
df = df.dropna(subset=['Rslt_home'])

y = df["Rslt_home"]  # If 1 if home team wins, 0 if they lose
X = df[FEATURE_NAMES]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3) Fit imputer + scaler on the training set:
imputer = SimpleImputer(strategy="mean")
X_train_imp = imputer.fit_transform(X_train)
X_test_imp = imputer.transform(X_test)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imp)
X_test_scaled = scaler.transform(X_test_imp)

# 4) Train each classifier once:
lr = LogisticRegression(max_iter=2000, random_state=42)
lr.fit(X_train_scaled, y_train)

svm = SVC(kernel="rbf", C=10, gamma=0.01, probability=True, random_state=42)
svm.fit(X_train_scaled, y_train)

mlp = MLPClassifier(
    hidden_layer_sizes=(50,),
    alpha=0.001,
    activation="relu",
    solver="adam",
    max_iter=500,
    random_state=42,
    early_stopping=True
)
mlp.fit(X_train_scaled, y_train)

# 5) (Optionally) Compute and print train/test accuracy once:
# y_pred_svm = svm.predict(X_test_scaled)
# print("SVM Test accuracy:", accuracy_score(y_test, y_pred_svm))

# 6) Save all three models, plus the imputer and scaler, to disk:
joblib.dump(imputer, "imputer.pkl")
joblib.dump(scaler,  "scaler.pkl")
joblib.dump(lr,      "lr_model.pkl")
joblib.dump(svm,     "svm_model.pkl")
joblib.dump(mlp,     "mlp_model.pkl")

print("Finished training and saved models to disk.")