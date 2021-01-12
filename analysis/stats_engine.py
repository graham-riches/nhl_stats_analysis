"""
    @file stats_engine.py
    @brief overall statistics engine for player data
    @author Graham Riches
    @details
   
"""
import numpy as np
import pandas as pd
from analysis.skater import Skater
from analysis.stats_types import  SkaterSerializer


class StatsEngine:
    def __init__(self):
        """
        Create a new stats engine object. This contains all the player data over a set of years
        """
        self.skaters = dict()

    @staticmethod
    def read_from_csv(filename: str, parser: callable, year: int) -> None:
        """
        Read data from a csv and apply a parser function to each element.
        :param filename: file to read data from
        :param parser: callable function to parse each line entry
        :param year: the year of the stats
        :return: None
        """
        lines = open(filename, 'r').readlines()
        for line in lines[1:]:
            parser(line, year)

    def basic_skater_parser(self, line: str, year: int) -> None:
        """
        parse a line from a basic skater file
        :param line: the line to parse
        :param year: the year of the data
        :return: None
        """
        name, stats = SkaterSerializer.create_basic_stats(line)
        if name in self.skaters:
            self.skaters[name].add_basic_stats(year, stats)
        else:
            skater = Skater(name)
            skater.add_basic_stats(year, stats)
            self.skaters[name] = skater

    def advanced_skater_parser(self, line: str, year: int) -> None:
        """
        parse a line from an advanced skater stats file
        :param line: line to parse
        :param year: the year of the data
        :return: None
        """
        name, stats = SkaterSerializer.create_advanced_stats(line)
        if name in self.skaters:
            self.skaters[name].add_advanced_stats(year, stats)
        else:
            skater = Skater(name)
            skater.add_advanced_stats(year, stats)
            self.skaters[name] = skater

    def add_advanced_skater_from_csv(self, filename: str, year: int) -> None:
        """
        Add advanced skater data to the stats engine from a csv file
        :param filename: the csv file containing advanced stat data
        :param year: the year of the data
        :return: None
        """
        self.read_from_csv(filename, self.advanced_skater_parser, year)

    def add_basic_skater_from_csv(self, filename: str, year: int) -> None:
        """
        Add basic skater data to the engine from a csv file
        :param filename: the csv file containing the data
        :param year: the year of the data
        :return: None
        """
        self.read_from_csv(filename, self.basic_skater_parser, year)

    def constrain_by_year(self, year: int) -> None:
        """
        drop all players that do not have data from a specific year
        :param year: the year to check
        :return: None
        """
        drop_list = list()
        for player, skater in self.skaters.items():
            if year not in skater.basic_stats.keys() and year not in skater.advanced_stats.keys():
                drop_list.append(player)
        for player in drop_list:
            del self.skaters[player]

    def drop_by_games_played(self, games_played: int) -> None:
        """
        For each player, drop any seasons that they did not play at least "games_player" games
        :param games_played: threshold games played
        :return:
        """
        for player, skater in self.skaters.items():
            drop_list = list()
            for season in skater.basic_stats.keys():
                if skater.basic_stats[season].stats['games_played'] < games_played:
                    drop_list.append(season)
            for season in drop_list:
                try:
                    del skater.basic_stats[season]
                    del skater.advanced_stats[season]
                except KeyError as ke:
                    pass

    def get_stats_by_year(self, year: int) -> pd.DataFrame:
        """
        get a set of player data by year with combined basic and advanced stats
        :param year: the year to get data for
        :return:
        """
        columns = SkaterSerializer.get_all_stat_fields()
        header = ['player_name'] + columns
        stats = []
        for name, skater in self.skaters.items():
            try:
                data = skater.get_stats_by_year(year)
                stats.append([name] + [data[column] for column in columns])
            except KeyError as ce:
                print('{} stats not available for player: {}'.format(ce, name))
        record = pd.DataFrame.from_records(stats, columns=header)
        record.index = record['player_name']
        return record

    def project_stats(self, season: int, model: callable) -> None:
        """
        project each players stats for a given seasn
        :param season: the season to project
        :param model: projection model callable that reduces a collection of stats into a new value
        :return: None
        """
        for player, skater in self.skaters.items():
            skater.project_basic_stats(season, model)
            skater.project_advanced_stats(season, model)

    @staticmethod
    def keep_categories(df: pd.DataFrame, categories: list) -> pd.DataFrame:
        """
        keep a set of categories in a rankings dataframe
        :param df: the raw dataframe
        :param categories: set of categories
        :return: dataframe with only categories as columns
        """
        new_df = df.loc[:, categories]
        return new_df

    @staticmethod
    def filter_by_category(df: pd.DataFrame, category: str, predicate: callable) -> pd.DataFrame:
        """
        apply a filtering operation to a dataframe column
        :param df: dataframe to filter
        :param category: category to filter on
        :param predicate: filter predicate for the column
        :return: modified dataframe
        """
        series = df[category].to_list()
        return df[list(map(predicate, series))]

    @staticmethod
    def calculate_z_score_rankings(df: pd.DataFrame, categories: list) -> pd.DataFrame:
        """
        calculate the z-score rankings on dataframe of states and return a new dataframe with the z_scores concatenated
        :param df: original dataframe
        :param categories: the categories of the data to parse
        :return: dataframe with z_score rankings
        """
        games_played = df['games_played'].to_numpy()
        data = df.to_numpy()
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        mean_subtracted = np.subtract(data, mean)
        for idx, val in enumerate(mean):
            mean_subtracted[:, idx] = np.divide(mean_subtracted[:, idx], games_played)
        z_scores = np.divide(mean_subtracted, std)
        for idx, category in enumerate(categories):
            df['{}_z'.format(category)] = z_scores[:, idx]
        return df

    @staticmethod
    def apply_positional_adjustment(df: pd.DataFrame, categories: list, adjustments: dict) -> pd.DataFrame:
        """
        apply a multiplier correction to a category based on position.
        :param df: the raw dataframe
        :param categories: list of categories to filter the DF with
        :param adjustments: dictionary of positional adjustments
        :return: modified dataframe
        """
        adjusted_categories = ['{}_adj'.format(category) for category in categories]
        fantasy_df = df.loc[:, categories]
        for idx, category in enumerate(adjusted_categories):
            fantasy_df[category] = df[categories[idx]]

        for index, row in fantasy_df.iterrows():
            player_data = df.loc[index]
            modifiers = adjustments[player_data['position']]
            for idx, weight in enumerate(modifiers):
                row[adjusted_categories[idx]] = row[adjusted_categories[idx]] * weight
        for category in adjusted_categories:
            df[category] = fantasy_df[category]
        return df

    @staticmethod
    def calculate_fantasy_score(df: pd.DataFrame, categories: list, calculate_z_based: bool = False) -> pd.DataFrame:
        """
        calculate an overall fantasy score based on a set of categories
        :param df: the raw dataframe
        :param categories: list of categories
        :param calculate_z_based: option to also calculate a z-score based fantasy score
        :return: dataframe with fantasy points
        """
        adj_categories = ['{}_adj'.format(category) for category in categories]
        z_categories = ['{}_z'.format(category) for category in categories]

        if calculate_z_based:
            category_sets = {'fantasy_points': adj_categories, 'fantasy_points_z': z_categories}
        else:
            category_sets = {'fantasy_points': adj_categories}

        for field, cs in category_sets.items():
            fp_df = df.loc[:, cs]
            data = fp_df.to_numpy()
            points = np.sum(data, axis=1)
            df[field] = points
        return df
