import pandas as pd

# Load datasets
summary = pd.read_csv("/Users/asmita/Desktop/Data Viz PROJECT/archive-2/all_season_summary.csv")
details = pd.read_csv("/Users/asmita/Desktop/Data Viz PROJECT/archive-2/all_season_details.csv")
batting = pd.read_csv("/Users/asmita/Desktop/Data Viz PROJECT/archive-2/all_season_batting_card.csv")
bowling = pd.read_csv("/Users/asmita/Desktop/Data Viz PROJECT/archive-2/all_season_bowling_card.csv")
points = pd.read_csv("/Users/asmita/Desktop/Data Viz PROJECT/archive-2/points_table.csv")

# Quick look
# print(summary.head())
# print(details.head())
# print(batting.head())
# print(bowling.head())
# print(points.head())

# print(summary.info())
# print(details.info())
# print(batting.info())
# print(bowling.info())
# print(points.info())
import pandas as pd

# -------------------------
# Team mapping for consistency
# -------------------------
team_mapping = {
    'Gujarat Titans': 'GT',
    'Chennai Super Kings': 'CSK',
    'Lucknow Super Giants': 'LSG',
    'Mumbai Indians': 'MI',
    'Rajasthan Royals': 'RR',
    'Royal Challengers Bangalore': 'RCB',
    'Kolkata Knight Riders': 'KKR',
    'Punjab Kings': 'KXIP',
    'Delhi Capitals': 'DC'
}

# -------------------------
# 1️⃣ all_season_summary.csv
# -------------------------
summary = pd.read_csv("archive-2/all_season_summary.csv")

# Dates
summary['start_date'] = pd.to_datetime(summary['start_date'], errors='coerce')
summary['end_date'] = pd.to_datetime(summary['end_date'], errors='coerce')

# Numeric
numeric_cols = ['home_overs','away_overs','home_runs','away_runs','home_wickets',
                'away_wickets','home_boundaries','away_boundaries','points']
for col in numeric_cols:
    summary[col] = pd.to_numeric(summary[col], errors='coerce')

# Fill categorical NAs
cat_cols = ['winner','toss_won','pom','home_captain','away_captain','venue_name']
for col in cat_cols:
    summary[col] = summary[col].fillna('Unknown')

# Standardize team names
summary['home_team'] = summary['home_team'].map(team_mapping).fillna(summary['home_team'])
summary['away_team'] = summary['away_team'].map(team_mapping).fillna(summary['away_team'])

# Save
summary.to_csv("all_season_summary_cleaned.csv", index=False)


# -------------------------
# 2️⃣ all_season_details.csv
# -------------------------
details = pd.read_csv("archive-2/all_season_details.csv")

# Numeric columns
num_cols = ['runs','batsman1_runs','batsman1_balls','bowler1_runs','bowler1_wkts',
            'batsman2_runs','batsman2_balls','bowler2_overs','bowler2_maidens',
            'bowler2_runs','bowler2_wkts','wicket_id','wkt_batsman_runs','wkt_batsman_balls']
for col in num_cols:
    details[col] = pd.to_numeric(details[col], errors='coerce')

# Boolean columns
bool_cols = ['isBoundary','isWide','isNoball','isRetiredHurt']
for col in bool_cols:
    details[col] = details[col].astype(bool)

# Player IDs as string (mixed types)
details['batsman2_id'] = details['batsman2_id'].astype(str)
details['bowler2_id'] = details['bowler2_id'].astype(str)

# Drop unnecessary text columns
details.drop(columns=['preText','postText','text','shortText'], inplace=True, errors='ignore')

# Save
details.to_csv("all_season_details_cleaned.csv", index=False)


# -------------------------
# 3️⃣ all_season_batting_card.csv
# -------------------------
batting = pd.read_csv("archive-2/all_season_batting_card.csv")

# Numeric
num_cols = ['runs','ballsFaced','fours','sixes','runningOver','strikeRate']
for col in num_cols:
    batting[col] = pd.to_numeric(batting[col], errors='coerce')

# Booleans
batting['captain'] = batting['captain'].astype(bool)
batting['isNotOut'] = batting['isNotOut'].map({'yes':1,'no':0}).fillna(0).astype(int)

# Fill missing runs/balls with 0
batting['runs'] = batting['runs'].fillna(0)
batting['ballsFaced'] = batting['ballsFaced'].fillna(0)

# Save
batting.to_csv("all_season_batting_card_cleaned.csv", index=False)


# -------------------------
# 4️⃣ all_season_bowling_card.csv
# -------------------------
bowling = pd.read_csv("archive-2/all_season_bowling_card.csv")

# Numeric
num_cols = ['overs','maidens','conceded','wickets','dots','foursConceded','sixesConceded','wides','noballs','economyRate']
for col in num_cols:
    bowling[col] = pd.to_numeric(bowling[col], errors='coerce')

# Boolean
bowling['captain'] = bowling['captain'].astype(bool)

# Fill missing numeric with 0
bowling[num_cols] = bowling[num_cols].fillna(0)

# Save
bowling.to_csv("all_season_bowling_card_cleaned.csv", index=False)


# -------------------------
# 5️⃣ points_table.csv
# -------------------------
points = pd.read_csv("archive-2/points_table.csv")

# Numeric
num_cols = ['matchesplayed','matcheswon','matcheslost','noresult','matchpoints','nrr']
for col in num_cols:
    points[col] = pd.to_numeric(points[col], errors='coerce')

# Split for/against columns
points[['runs_for','overs_for']] = points['for'].str.split('/', expand=True).astype(float)
points[['runs_against','overs_against']] = points['against'].str.split('/', expand=True).astype(float)

# Standardize team names
points['name'] = points['name'].map(team_mapping).fillna(points['name'])
points['short_name'] = points['short_name'].map(team_mapping).fillna(points['short_name'])

# Save
points.to_csv("points_table_cleaned.csv", index=False)

print("All CSVs cleaned and saved successfully!")
