"""
    @file projections.py
    @brief set of functions for creating new seasonal projections
    @author Graham Riches
    @details
   
"""
import numpy as np


def weighted_average(games_played: int, weights: list, stats: list) -> float:
    """
    take a list of stats and output a predicted value
    :param games_played: how many games to project
    :param weights: seasonal weights
    :param stats: list of seasonal stats in a specific category sorted from newest to oldest (i.e. [2019, 2018, ...])
    :return: predicted next season value
    """
    return np.divide(np.sum([x[0] * x[1] for x in zip(weights, stats)]), np.sum(weights[0:len(stats)])) * games_played


def weighted_average_with_experience_adjustment(games_played: int, average_weights: list,
                                                seasonal_progression_weights: list, stats: list) -> float:
    """
    Performs a weighted average stat projection based on historical data, but also includes productivity multipliers
    based on the number of seasons played. For example, players that have already played 5+ seasons are unlikely to
    see a large productivity bump, while players entering their second or third NHL season are likely to see a
    substantial experience based projection that is heavily downplayed by a simple historical weighted average model.
    :param games_played: total number of games to project
    :param average_weights: weighted averaging coefficients
    :param seasonal_progression_weights: list of seasonal experience weights to add to projections. Considered as a list
           of number of seasons played. I.e. [1.1, 1.2, 1.3, 1.0, 1.0, 1.0] would provide a 10% projection boost to
           players that are entering their sophomore season, a 20% boost to players entering their third season, and a
           30% boost to players entering their fourth season.
    :param stats: list of the stat category over seasons
    :return:
    """
    progression_multiplier = seasonal_progression_weights[len(stats) - 1]
    base_projection = np.divide(np.sum([x[0] * x[1] for x in zip(average_weights, stats)]), np.sum(average_weights[0:len(stats)]))
    return base_projection * games_played * progression_multiplier
