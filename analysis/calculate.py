"""
    @file calculate.py
    @brief main file to crunch all fantasy stats
    @author Graham Riches
    @details
   
"""

import json
from analysis.stats_engine import StatsEngine, calculate_z_score_rankings

with open('../config/categories.json') as json_file:
    categories = json.loads(str(json_file.read()))
engine = StatsEngine()

years = [2015]
for year in years:
    engine.add_basic_skater_from_csv('../data/skaters/basic/{}.csv'.format(year), year)
    engine.add_advanced_skater_from_csv('../data/skaters/advanced/{}.csv'.format(year), year)
    df = None
    new_df = None
    df = engine.get_stats_by_year(year)
    new_df = df.loc[:, categories]
    new_df = calculate_z_score_rankings(new_df, categories)
    new_df.to_csv('../data/z_score_rankings/{}.csv'.format(year))
