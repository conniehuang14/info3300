from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
import numpy as np
from datetime import datetime

# Dataset of different chess opening statistics from online Chess site
# Source: https://www.kaggle.com/arashnic/chess-opening-dataset
openings_df = pd.read_csv("/Users/hunter/Downloads/INFO 3300 HW/project 2/high_elo_opening.csv")

# Dataset for analyzing moves of 12 top players, listed names at chess.com/games
# Source: https://www.kaggle.com/liury123/chess-game-from-12-top-players
masters_df = pd.read_csv("/Users/hunter/Downloads/INFO 3300 HW/project 2/game_data.csv")

### Plan - utilize openings as main statistics, add filtering for different rated/skilled players
# openings_df usage: Effectiveness of certain openings, determine next best move after specific opening, player's average skill
# masters_df usage: what openings do highly skilled users tend to use? What openings are best against skilled users vs all?
# Opening move | opening white win odds (online white wins odds) | # opening games used/won (top players white wins) | 


# Find all possible first moves and create output dataset
first_move = openings_df["move1w"].unique()
output_df = pd.DataFrame(index=first_move)

# Construct first move/white winning odds column
# Utilizing aggregation code from https://www.kaggle.com/arashnic/first-moves-analysis?scriptVersionId=48542202
white_1_stats = openings_df.groupby('move1w').agg({'white_wins' : np.sum, 'black_wins':np.sum})
white_1_stats['white_odds'] = white_1_stats['white_wins'] / white_1_stats['black_wins'] 
white_1_stats = white_1_stats.sort_values('white_odds', ascending = False)
for move in first_move:
    output_df.loc[move, 'white_odds'] = white_1_stats.loc[move, 'white_odds'].round(5)

# Construct top player first move count column, base only off wins by color
masters_df = masters_df.loc[masters_df["result"] == "Win"]
masters_df['white_1'] = masters_df.lines.str.split(" 2.").str[0].str.split(" ").str[1]
masters_df['black_1'] = masters_df.lines.str.split(" 2.").str[0].str.split(" ").str[2]
white_1_masters = masters_df.loc[masters_df["color"] == "White"]['white_1'].value_counts()
for move in first_move:
    if move not in white_1_masters:
        output_df.loc[move, 'master_white_use_count'] = 0
    else:
        output_df.loc[move, 'master_white_use_count'] = white_1_masters[move]

# 10 best black responses, top player responses
print(output_df)
for move in first_move:
    # Utilizing aggregation code from https://www.kaggle.com/arashnic/first-moves-analysis?scriptVersionId=48542202
    move_stats = openings_df[openings_df['move1w']==move].groupby('move1b').agg({'white_wins' : np.sum, 'black_wins':np.sum})
    move_stats['white_odds'] = move_stats['white_wins'] / move_stats['black_wins']
    move_stats = move_stats.sort_values('white_odds')



# Convert column types to int for easy handling
#for col in [list of count cols]:
#    output_df[col] = output_df[col].astype('int64')

# export as csv
#output_df.to_csv('processed_chess.csv')