"""
    @file convert_rankings.py
    @brief convert raw rankings to a more useful csv format
    @author Graham Riches
    @details
   
"""


def clean_dobber_line(line: str) -> str:
    new_line = line.strip('\t ').replace('\t', ',')
    return new_line


def clean_nhl_line(line: str) -> str:
    new_line = line.replace('. ', ',').replace(', ', ',')
    return new_line


def clean_fantasy_pro_line(line: str) -> str:
    new_line = line.replace('"', '')
    return new_line


if __name__ == '__main__':
    dobber_lines = open('../data/rankings/dobber.txt').readlines()
    with open('../data/curated_rankings/dobber_rankings.csv', 'w') as file:
        file.writelines(list(map(clean_dobber_line, dobber_lines)))

    nhl_lines = open('../data/rankings/nhl_com.txt').readlines()
    with open('../data/curated_rankings/nhl_rankings.csv', 'w') as file:
        file.writelines(list(map(clean_nhl_line, nhl_lines)))

    fpro_lines = open('../data/rankings/fantasy_pro.csv').readlines()
    with open('../data/curated_rankings/fantasy_pro_rankings.csv', 'w') as file:
        file.writelines(list(map(clean_fantasy_pro_line, fpro_lines)))
