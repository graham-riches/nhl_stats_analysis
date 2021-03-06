"""
    @file convert_rankings.py
    @brief convert raw rankings to a more useful csv format
    @author Graham Riches
    @details
    each function just takes in a line, and returns cleaned up data in the format:
    Rank,Player,Positions,Team
   
"""
import re


def clean_fantasy_file(input_file: str, output_file: str, parser: callable) -> None:
    with open(output_file, 'w') as file:
        file.write('Rank,Player,Team,Positions\n')
        file.writelines(list(map(parser, open(input_file).readlines())))


def clean_dobber_line(line: str) -> str:
    matches = re.findall(r'(\d+)\s([\w .\'-]+)', line)
    return '{},{},,\n'.format(matches[0][0], matches[0][1])


def clean_nhl_line(line: str) -> str:
    new_line = line.replace('/', ' ').replace(', ', ',').replace('\n', '')
    matches = re.findall(r'(\d+).\s([\w\s.\'-]+),([\w\s]+),([\w\s]+)', new_line)
    return '{}\n'.format(','.join(match for match in matches[0]))


def clean_yahoo_line(line: str) -> str:
    new_line = line.replace(',', ' ')
    matches = re.findall(r'(\d+)\s([\w .\'-]+)\s\((\w+)\s-\s([\w\s]+)\)', new_line)
    return '{}\n'.format(','.join(match for match in matches[0]))


def clean_fantasy_pro_line(line: str) -> str:
    new_line = line.replace('"', '')
    items = new_line.split(',')
    return '{}\n'.format(','.join(item for item in items[0:4]))


if __name__ == '__main__':
    file_parsers = {'dobber': clean_dobber_line, 'fantasy_pro': clean_fantasy_pro_line,
                    'nhl': clean_nhl_line, 'yahoo': clean_yahoo_line}

    for file, function in file_parsers.items():
        input_path = '../data/rankings/{}.txt'.format(file)
        output_path = '../data/curated_rankings/{}_rankings.csv'.format(file)
        clean_fantasy_file(input_path, output_path, function)