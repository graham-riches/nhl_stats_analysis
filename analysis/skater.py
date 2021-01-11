"""
    @file skater.py
    @brief class for containing and managing skater data
    @author Graham Riches
    @details
   
"""
import numpy as np
from analysis.stats_types import BasicSkaterStats, AdvancedSkaterStats, SkaterSerializer


class Skater:
    def __init__(self, player_name: str):
        """
        Create a new skater object. This contains two dictionaries which contain year index basic and advanced
        player stats respectively
        :param player_name: name of the player
        """
        self.name = player_name
        self.basic_stats = dict()  # basic stats per season
        self.advanced_stats = dict()  # advanced stats per season

    def add_basic_stats(self, year: int, stats: BasicSkaterStats) -> None:
        """
        Add basic stats by year to the skater object
        :param year: year key to add
        :param stats: basic stats object
        :return: None
        """
        self.basic_stats[year] = stats

    def add_advanced_stats(self, year: int, stats: AdvancedSkaterStats) -> None:
        """
        add advanced stats by year to the skater object
        :param year: year key to add
        :param stats: advanced stats object
        :return: None
        """
        self.advanced_stats[year] = stats

    def get_stats_by_year(self, year: int) -> dict:
        """
        get all player stats combined for a specific season
        :param year: the year to get stats for
        :return:
        """
        basic_stats = self.basic_stats[year]
        advanced_stats = self.advanced_stats[year]
        return {**basic_stats.stats, **advanced_stats.stats}

    def project_basic_stats(self, project_season: int, projection: callable) -> None:
        """
        project a skater's basic stats for a new season
        :param project_season: the season to project
        :param projection: callable that takes a collection and produces a new value
        :return:
        """
        seasons = list(self.basic_stats.keys())
        seasons.sort(reverse=True)
        if project_season - 1 not in seasons:
            print('ERROR: player {} missing stats information for {}'.format(self.name, project_season - 1))
            return
        data = list()
        for season in seasons:
            data.append([val for key, val in self.basic_stats[season].stats.items()])

        # average the data across the seasons now
        new_data = list()
        for idx in range(len(BasicSkaterStats.fields)):
            fields = [x.pop(0) for x in data]
            try:
                new_data.append(projection(fields))
            except Exception as ce:
                new_data.append(fields[0])
        self.basic_stats[project_season] = BasicSkaterStats(new_data)

    def project_advanced_stats(self, project_season: int, projection: callable) -> None:
        """
        project the next season of advanced stats based on historical data
        :param project_season: the year to project. Requires player data from the previous season
        :param projection: callable that takes a colleciton and produces a new value
        :return:
        """
        seasons = list(self.advanced_stats.keys())
        seasons.sort(reverse=True)
        if project_season - 1 not in seasons:
            print('ERROR: player {} missing stats information for {}'.format(self.name, project_season - 1))
            return
        data = list()
        for season in seasons:
            data.append([val for key, val in self.advanced_stats[season].stats.items()])
        # average the data across the seasons now
        new_data = list()
        for idx in range(len(AdvancedSkaterStats.fields)):
            fields = [x.pop(0) for x in data]
            try:
                new_data.append(np.average(fields))
            except Exception as ce:
                new_data.append(fields[0])
        self.advanced_stats[project_season] = AdvancedSkaterStats(new_data)
