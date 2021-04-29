from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
import numpy as np
from datetime import datetime

# Dataset of different chess opening statistics from online Chess site
# Source: https://www.kaggle.com/arashnic/chess-opening-dataset
openings_df = pd.read_csv("high_elo_opening.csv")

# Dataset for analyzing moves of 12 top players, listed names at chess.com/games
# Source: https://www.kaggle.com/liury123/chess-game-from-12-top-players
masters_df = pd.read_csv("game_data.csv")

### Plan - utilize openings as main statistics, add filtering for different rated/skilled players
# openings_df usage: Effectiveness of certain openings, determine next best move after specific opening, player's average skill
# masters_df usage: what openings do highly skilled users tend to use? What openings are best against skilled users vs all?
# Opening move | opening white win odds (online white wins odds) | # opening games used/won (top players white wins) | 


# Find all possible first moves and create output dataset
first_move = openings_df["move1w"].unique()
output_df = pd.DataFrame(index=first_move)

# Construct first move winning odds column, move count column, and percent draw column from online dataset
# Utilizing aggregation code from https://www.kaggle.com/arashnic/first-moves-analysis?scriptVersionId=48542202
white_1_stats = openings_df.groupby('move1w').agg({'num_games': np.sum, 'white_wins' : np.sum, 'black_wins':np.sum, 'perc_draw':np.average})
white_1_stats['white_odds'] = white_1_stats['white_wins'] / white_1_stats['black_wins']
for move in first_move:
    output_df.loc[move, 'online_white_odds'] = white_1_stats.loc[move, 'white_odds'].round(4)
    output_df.loc[move, 'online_w1_move_per_1000'] = (white_1_stats.loc[move, 'num_games'] / white_1_stats['num_games'].sum()).round(7)*1000
    output_df.loc[move, 'online_w1_avg_draw'] = white_1_stats.loc[move, 'perc_draw'].round(4)

# Construct master player first move count (if moving first) and winrate column
masters_df_wins = masters_df.loc[masters_df["result"] == "Win"]
masters_df['white_1'] = masters_df.lines.str.split(" 2.").str[0].str.split(" ").str[1]
masters_df['black_1'] = masters_df.lines.str.split(" 2.").str[0].str.split(" ").str[2]
white_1_masters = masters_df.loc[masters_df["color"] == "White"]['white_1'].value_counts()
master_moves = masters_df.groupby('white_1').agg({'moves': np.average})
for move in first_move:
    if move not in white_1_masters:
        output_df.loc[move, 'master_w1_move_per_1000'] = "N/A"
        output_df.loc[move, 'master_w1_game_length'] = "N/A"

    else:
        output_df.loc[move, 'master_w1_move_per_1000'] = (white_1_masters[move] / white_1_masters.sum()).round(7)*1000
        output_df.loc[move, 'master_w1_game_length'] = master_moves.loc[move, 'moves'].round(4)

# 10 best black responses, top player responses
for move in first_move:
    # Utilizing aggregation code from https://www.kaggle.com/arashnic/first-moves-analysis?scriptVersionId=48542202
    move_stats = openings_df[openings_df['move1w']==move].groupby('move1b').agg({'white_wins' : np.sum, 'black_wins':np.sum})
    move_stats['white_odds'] = move_stats['white_wins'] / move_stats['black_wins']
    move_stats = move_stats.sort_values('white_odds')



# Convert column types to int for easy handling (if needed)
#for col in [list of count cols]:
#    output_df[col] = output_df[col].astype('int64')

# Name axis first_move for referencing in csv
output_df = output_df.rename_axis("first_move")

# export as csv
output_df.to_csv('processed_chess.csv')