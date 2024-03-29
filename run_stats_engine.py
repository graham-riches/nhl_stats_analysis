"""
    @file run_stats_engine.py
    @brief main file to crunch all fantasy stats
    @author Graham Riches
    @details
   
"""

import pandas as pd
import json
from functools import partial
from analysis.stats_engine import StatsEngine
from analysis.projections import weighted_average_with_experience_adjustment
from analysis.colors import TerminalColors

years = [2015, 2016, 2017, 2018, 2019, 2020]
with open('config/config.json') as json_file:
    config = json.loads(str(json_file.read()))
    stats_categories = config['stats_categories']
    fantasy_categories = config['fantasy_categories']
    positional_adjustments = config['positional_adjustments']
    displays = config['display_categories']

# stats engine to hold all the skater data
engine = StatsEngine()

# read in the data
for year in years:
    engine.add_basic_skater_from_csv('data/skaters/basic/{}.csv'.format(year), year)
    engine.add_advanced_skater_from_csv('data/skaters/advanced/{}.csv'.format(year), year)

# drop any player season without a threshold limit of games played
engine.drop_by_games_played(25)

# set seasonal weighting to more heavily weight recent performances
projection = partial(weighted_average_with_experience_adjustment, 82,
                     [4.0, 3.0, 2.0, 1.0, 1.0, 1.0],
                     [1.0, 1.10, 1.15, 1.0, 1.0, 1.0, 1.0])
engine.project_stats(2021, projection)

# drop any players not contained in the last season (retired, etc.)
engine.constrain_by_year(2020)

# add the new season to the list
years.append(2021)

# do some filtering and ranking and store the result in a new csv
for year in years:
    all_fields = displays + stats_categories
    df = engine.get_stats_by_year(year)
    df = engine.keep_categories(df, all_fields)
    display_df = engine.keep_categories(df, displays)
    stats_df = engine.keep_categories(df, stats_categories)
    stats_df = engine.filter_by_category(stats_df, 'games_played', lambda gp: gp > 35)
    stats_df = engine.calculate_z_score_rankings(stats_df, stats_categories)
    result = pd.concat([display_df, stats_df], axis=1)
    result = engine.filter_by_category(result, 'games_played', lambda gp: gp > 35)
    result = engine.apply_positional_adjustment(result, fantasy_categories, positional_adjustments)
    result = engine.calculate_fantasy_score(result, fantasy_categories, calculate_z_based=True)
    result = result.sort_values(by='fantasy_points_z', ascending=False)
    result.to_csv('data/z_score_rankings/{}.csv'.format(year))

print('\n\n' + TerminalColors.BLUE + 'Projected 2021/2022 stats ...\n' + TerminalColors.END)

df_new = pd.read_csv('data/z_score_rankings/2021.csv')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
columns = ['player_name', 'position']
columns.extend(fantasy_categories)
columns.append('fantasy_points_z')
print(df_new[columns][0:100])

