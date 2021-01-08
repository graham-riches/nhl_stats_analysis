"""
    @file calculate.py
    @brief main file to crunch all fantasy stats
    @author Graham Riches
    @details
   
"""

import json
from analysis.stats_engine import StatsEngine


years = [2015, 2016, 2017, 2018, 2019]
with open('../config/categories.json') as json_file:
    categories = json.loads(str(json_file.read()))

engine = StatsEngine()

# read in the data
for year in years:
    engine.add_basic_skater_from_csv('../data/skaters/basic/{}.csv'.format(year), year)
    engine.add_advanced_skater_from_csv('../data/skaters/advanced/{}.csv'.format(year), year)

# drop any players not contained in the last season
engine.constrain_by_year(2019)

for year in years:
    df = engine.get_stats_by_year(year)
    df = engine.keep_categories(df, categories)
    df = engine.filter_by_category(df, 'games_played', lambda gp: gp > 35)
    df = engine.calculate_z_score_rankings(df, categories)
    df.to_csv('../data/z_score_rankings/{}.csv'.format(year))
