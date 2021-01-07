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
        self._name = player_name
        self._basic_stats = dict()  # basic stats per season
        self._advanced_stats = dict()  # advanced stats per season

    def add_basic_stats(self, year: int, stats: BasicSkaterStats) -> None:
        """
        Add basic stats by year to the skater object
        :param year: year key to add
        :param stats: basic stats object
        :return: None
        """
        self._basic_stats[year] = stats

    def add_advanced_stats(self, year: int, stats: AdvancedSkaterStats) -> None:
        """
        add advanced stats by year to the skater object
        :param year: year key to add
        :param stats: advanced stats object
        :return: None
        """
        self._advanced_stats[year] = stats

