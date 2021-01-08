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
        drop_list = []
        for player, skater in self.skaters.items():
            if year not in skater.basic_stats.keys() and year not in skater.advanced_stats.keys():
                drop_list.append(player)
        for player in drop_list:
            del self.skaters[player]

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
        results = list(map(predicate, series))
        new_df = df[results]
        return new_df

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



