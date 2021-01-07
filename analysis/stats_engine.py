"""
    @file stats_engine.py
    @brief overall statistics engine for player data
    @author Graham Riches
    @details
   
"""

from analysis.skater import Skater
from analysis.stats_types import BasicSkaterStats, AdvancedSkaterStats, SkaterSerializer


class StatsEngine:
    def __init__(self):
        """
        Create a new stats engine object. This contains all the player data over a set of years
        """
        self._skaters = dict()

    def add_basic_skater_from_csv(self, filename: str) -> None:
        """
        Add basic skater data to the engine from a csv file
        :param filename: the csv file containing the data
        :return: None
        """
        data = open(filename, 'r').readlines()

        # ignore the csv header
        for line in data[1:]:
            name, stats = SkaterSerializer.create_basic_stats(line)
            if name in self._skaters:
                self._skaters[name].add_basic_stats(year, stats)
            else:
                skater = Skater(name)
                skater.add_basic_stats(year, stats)
                self._skaters[name] = skater


if __name__ == '__main__':
    engine = StatsEngine()
    years = [2015, 2016, 2017, 2018, 2019]
    for year in years:
        engine.add_basic_skater_from_csv('../data/skaters/basic/{}.csv'.format(year))
    pause = 1
