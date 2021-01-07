"""
    @file aggregate_rankings.py
    @brief combine all the curated rankings into one combined ranking
    @author Graham Riches
    @details
   
"""

import pandas as pd
import numpy as np

files = ['dobber_rankings', 'fantasy_pro_rankings', 'nhl_rankings']

if __name__ == '__main__':
    rankings_map = dict()

    for file in files:
        df = pd.read_csv('../data/curated_rankings/{}.csv'.format(file))

        for idx, row in df.iterrows():
            if row['Player'] in rankings_map:
                rankings_map[row['Player']].append(float(row['Rank']))
            else:
                rankings_map[row['Player']] = [float(row['Rank'])]
        print('hey')

    aggregated_rankings = pd.DataFrame.from_dict(rankings_map, orient='index', columns=['dobber_hockey', 'fantasy_pro',
                                                                                        'nhl.com'])
    aggregated_rankings['average_ranking'] = aggregated_rankings.mean(axis=1)
    aggregated_rankings['highest_ranking'] = aggregated_rankings.min(axis=1)
    aggregated_rankings['lowest_ranking'] = aggregated_rankings.max(axis=1, skipna=False)
    aggregated_rankings = aggregated_rankings.sort_values(by=['average_ranking'])
    print(aggregated_rankings.to_string())

