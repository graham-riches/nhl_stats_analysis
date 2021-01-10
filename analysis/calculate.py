"""
    @file calculate.py
    @brief main file to crunch all fantasy stats
    @author Graham Riches
    @details
   
"""

import pandas as pd
import json
from analysis.stats_engine import StatsEngine


years = [2015, 2016, 2017, 2018, 2019]
with open('../config/config.json') as json_file:
    config = json.loads(str(json_file.read()))
    stats_categories = config['stats_categories']
    fantasy_categories = config['fantasy_categories']
    positional_adjustments = config['positional_adjustments']
    displays = config['display_categories']


engine = StatsEngine()

# read in the data
for year in years:
    engine.add_basic_skater_from_csv('../data/skaters/basic/{}.csv'.format(year), year)
    engine.add_advanced_skater_from_csv('../data/skaters/advanced/{}.csv'.format(year), year)


# project out 2021 stats, which has a very buggy API at the moment :D requires using 2020 as the year
engine.project_stats(2020)

# drop any players not contained in the last season
engine.constrain_by_year(2019)

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
    result = engine.calculate_fantasy_score(result, fantasy_categories)
    result = result.sort_values(by='fantasy_points', ascending=False)
    result.to_csv('../data/z_score_rankings/{}.csv'.format(year))
