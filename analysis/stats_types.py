"""
    @file stats_types.py
    @brief contains basic NHL stats type objects
    @author Graham Riches
    @details
    This contains class definitions for basic and advanced player stats as well as factory methods for deserializing
    data into these object types
"""


class BasicSkaterStats:
    def __init__(self, stats: list):
        """
        Construct a BasicStats object. This contains standard fantasy categories and converts the data types into a
        dictionary with proper data types (int, etc.)
        :param stats: list of strings of stats fields
        """
        fields = ['team', 'position', 'games_played', 'goals', 'assists', 'pts', 'plus_minus',
                  'penalty_mins', 'shots_on_goal', 'game_winning_goals', 'power_play_goals',
                  'power_play_assists', 'short_handed_goals', 'short_handed_assists', 'hits', 'blocked_shots']
        types = [str, str]
        types.extend([int for i in range(len(fields) - len(types))])
        self._stats = {key: types[idx](stats[idx]) for idx, key in enumerate(fields)}


class AdvancedSkaterStats:
    def __init__(self):
        self._stats = dict()


class SkaterSerializer:
    @staticmethod
    def create_basic_stats(csv_line: str) -> tuple:
        tokens = csv_line.split(',')
        player_name = tokens[0]
        return player_name, BasicSkaterStats(tokens[1:])

    @staticmethod
    def create_advanced_stats(csv_line: str) -> AdvancedSkaterStats:
        pass
