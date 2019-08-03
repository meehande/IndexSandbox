import re
import pandas as pd
from src.data_loading.stock_data_loader import SourceTypes, get_yahoo_ticker


class IndexUnderlyingCsvLoader(object):
    def __init__(self, constituent_csv):
        self._input_file = constituent_csv
        self._data_start_line = 'Constituent Name,Symbol'
        to_remove = ['Limited', 'Inc.', 'Ltd.', 'Corp.', 'Corporation', 'Investment Trust']
        self._remove_from_company_regex = re.compile('|'.join(to_remove))

    def load_underlyings(self):
        raw_df = self._parse_input_data()
        formatted = self._format_and_fill(raw_df)
        return formatted

    def _parse_input_data(self):
        preamble_finished = False
        res_lil = []
        with open(self._input_file, 'r') as f:
            for line in f:
                if preamble_finished:
                    res_lil.append(line.strip('\n').split(','))
                elif self._data_start_line in line:
                    preamble_finished = True
        return pd.DataFrame(res_lil, columns=['CompanyName', 'Symbol'])

    def _format_input_data(self, raw_data):
        raw_data['SearchData'] = raw_data['CompanyName'].apply(self._format_company_name_for_search)
        raw_data['{}Ticker'.format(SourceTypes.YAHOO)] = raw_data.apply(lambda x:
                                                                        get_yahoo_ticker(x['SearchData'],
                                                                                         x['Symbol']), axis=1)
        return raw_data


def main():
    loader = IndexUnderlyingCsvLoader(r'C:\Users\meeha\PycharmProjects\IndexSandbox\src\data\index_constituents.csv')
    res = loader.load_underlyings()
    print('Dataframe Result: {}'.format(res.columns))


if __name__ == '__main__':
    main()
