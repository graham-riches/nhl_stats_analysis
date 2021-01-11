"""
    @file projections.py
    @brief set of functions for creating new seasonal projections
    @author Graham Riches
    @details
   
"""
import numpy as np


def weighted_average(weights: list, stats: list) -> float:
    """
    take a list of stats and output a predicted value
    :param weights: seasonal weights
    :param stats: list of seasonal stats in a specific category sorted from newest to oldest (i.e. [2019, 2018, ...])
    :return: predicted next season value
    """
    return np.divide(np.sum([x[0] * x[1] for x in zip(weights, stats)]), np.sum(weights[0:len(stats)]))

