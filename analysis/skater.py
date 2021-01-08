"""
    @file skater.py
    @brief class for containing and managing skater data
    @author Graham Riches
    @details
   
"""

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

    def project_stats(self, last_seasons: list,) -> BasicSkaterStats:
        """
        project the next season of stats based on a sequence of prior seasons
        :param last_seasons:
        :return:
        """
        pass
