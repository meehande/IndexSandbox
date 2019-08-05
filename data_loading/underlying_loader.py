import re
import pandas as pd
from src.data_loading.stock_data_loader import SourceTypes


class IndexUnderlyingCsvLoader(object):
    def __init__(self, constituent_csv, data_loader):
        self._input_file = constituent_csv
        self._data_start_line = 'Constituent Name,Symbol'
        self._data_loader = data_loader
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

    def _format_and_fill(self, raw_data):
        raw_data['SearchData'] = raw_data['CompanyName'].apply(self._format_company_name_for_search)
        raw_data['{}Ticker'.format(SourceTypes.YAHOO)] = raw_data.apply(lambda x:
                                                                        self._data_loader.get_ticker(x['SearchData'],
                                                                                         x['Symbol']), axis=1)
        raw_data['{}Ticker'.format(SourceTypes.DUMMY)] = raw_data.apply(lambda x:
                                                                        self._data_loader.get_ticker(
                                                                            x['SearchData'],
                                                                            x['Symbol']), axis=1)
        return raw_data

    def _format_company_name_for_search(self, company_name):
        return self._remove_from_company_regex.split(company_name)[0]


def main():
    loader = IndexUnderlyingCsvLoader(r'C:\Users\meeha\PycharmProjects\IndexSandbox\src\data\index_constituents.csv')
    res = loader.load_underlyings()
    print('Dataframe Result: {}'.format(res.columns))


if __name__ == '__main__':
    main()
