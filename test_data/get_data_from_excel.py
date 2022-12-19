import logging
from pathlib import Path

import pandas as pd


def excel_reader(file_name, sheet_name):
    file_path = f'{Path(__file__).parent}\\{file_name}'
    df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)
    return df


def get_row_data(excel_name, sheet_name):
    data = []
    for index, row in excel_reader(excel_name, sheet_name).iterrows():
        row = row.fillna('')
        data.append(row)
    return data


def preprocess_data_in_row(raw_series):
    row = raw_series.fillna('')
    for index, value in row.items():
        logging.info('Creating fake data: %s', index)
        if 'chars' in value:
            num_chars = int(value.replace(' chars', ''))
            if num_chars == 1:
                row = row.replace([value], 'C')
            name_str = 'allenlee'
            multi = num_chars // len(name_str)
            remain = num_chars % len(name_str)
            new_data_str = name_str * multi + name_str[:remain]
            row = row.replace([value], new_data_str)
        elif index == 'Title' and value != '':
            row = row.replace([value], 'allenlee_' + value)
    return row
