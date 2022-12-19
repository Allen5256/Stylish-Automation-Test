import logging

import pandas as pd
import pymysql


class SQLObject:
    def __init__(self, settings):
        self.__db_settings = settings

        self._connection = pymysql.connect(**self.__db_settings)

    def select_data_as_df(self, cols, table, **kwargs):
        target_cols_str = ', '.join(cols)
        where_condition = kwargs.get('where_condition')
        page_index = kwargs.get('page_index')
        count = kwargs.get('count')

        if where_condition is not None:
            if page_index is not None and count is not None:
                start_line = page_index * count
                command = f'SELECT {target_cols_str} FROM {table} WHERE {where_condition} LIMIT {start_line}, {count}'
            else:
                command = f'SELECT {target_cols_str} FROM {table} WHERE {where_condition}'
        else:
            command = f'SELECT {target_cols_str} FROM {table}'

        logging.info('%s', command)
        result_df = pd.read_sql_query(command, self._connection, index_col=kwargs.get('index_col'))
        return result_df

    def disconnect(self):
        self._connection.close()
