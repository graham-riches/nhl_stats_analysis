"""
    @file stats_types.py
    @brief contains basic NHL stats type objects
    @author Graham Riches
    @details
    This contains class definitions for basic and advanced player stats as well as factory methods for deserializing
    data into these object types
"""
from datetime import datetime


class BasicSkaterStats:
    fields = ['team', 'position', 'games_played', 'goals', 'assists', 'pts', 'plus_minus',
              'penalty_mins', 'shots_on_goal', 'game_winning_goals', 'power_play_goals',
              'power_play_assists', 'short_handed_goals', 'short_handed_assists', 'hits', 'blocked_shots']

    def __init__(self, stats: list):
        """
        Construct a BasicSkaterStats object. This contains standard fantasy categories and converts the data types into a
        dictionary with proper data types (int, etc.)
        :param stats: list of strings of stats fields
        """
        types = [str, str]
        types.extend([int for i in range(len(self.fields) - len(types))])
        self.stats = dict()
        for idx, key in enumerate(self.fields):
            try:
                self.stats[key] = types[idx](stats[idx])
            except Exception as ce:
                print('Basic Stats Error: {}'.format(ce))
                self.stats[key] = types[idx]()


class AdvancedSkaterStats:
    fields = ['age', 'cf', 'ca', 'c_pct', 'c_pct_rel', 'ff', 'fa', 'f_pct', 'f_pct_rel', 'sh_pct', 'sv_pct',
              'pdo', 'off_zone_starts', 'def_zone_starts', 'toi_60', 'toi_ev', 'takeaways', 'giveaways',
              'ev_plus_minus', 'shot_attempts', 'shot_through_pct']

    def __init__(self, stats: list):
        """
        Construct a new AdvancedSkaterStats object. This contains advanced information like Corsi, Fenwick, PDO, etc.
        :param stats: list of stats
        """
        types = [int, float, float, float, float, float, float, float, float, float, float,
                 float, float, float, str, str, int, int,
                 float, int, float]
        self.stats = dict()
        for idx, key in enumerate(self.fields):
            try:
                self.stats[key] = types[idx](stats[idx])
            except Exception as ce:
                print('Advanced Stats Error: {}'.format(ce))
                self.stats[key] = types[idx]()


class SkaterSerializer:
    """
    Factory method class for creating stats objects from serial text data.
    """
    @staticmethod
    def create_basic_stats(csv_line: str) -> tuple:
        """
        Create a basic stats object from a csv line
        :param csv_line: csv data
        :return: new tuple of (player_name, BasicSkaterStats)
        """
        tokens = csv_line.split(',')
        player_name = tokens[0]
        return player_name, BasicSkaterStats(tokens[1:])

    @staticmethod
    def create_advanced_stats(csv_line: str) -> tuple:
        """
        Create an advanced stats object from a csv line
        :param csv_line: the line of data
        :return: new tuple of (player_name, AdvancedSkaterStats)
        """
        tokens = csv_line.split(',')
        player_name = tokens[1].split('\\')[0]
        tokens_of_interest = [tokens[2]]
        tokens_of_interest.extend(tokens[6:])
        return player_name, AdvancedSkaterStats(tokens_of_interest)

    @staticmethod
    def get_all_stat_fields() -> list:
        fields = []
        fields.extend(BasicSkaterStats.fields)
        fields.extend(AdvancedSkaterStats.fields)
        return fields


if __name__ == '__main__':
    adv = open('../data/skaters/advanced/2019.csv', 'r').readlines()
    name, data = SkaterSerializer.create_advanced_stats(adv[1])
