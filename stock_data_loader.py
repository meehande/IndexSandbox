import requests
from yahoo_fin import stock_info as si
import pandas as pd
import re
import datetime as dt
import abc
from enum import Enum


class SourceTypes(Enum):
    YAHOO = 'YAHOO'


class StockPriceLoader(abc.ABC):
    @abc.abstractmethod
    def get_latest_closing_price(self, ticker):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_market_cap(self, yahoo_ticker):
        raise NotImplementedError()


class YahooStockPriceLoader(StockPriceLoader):
    def __init__(self):
        self.price_source = SourceTypes.YAHOO

    def get_latest_closing_price(self, yahoo_ticker):
        last_bus_day = pd.bdate_range(start=dt.date.today() - dt.timedelta(days=5), end=dt.date.today())[-1]
        stock_data = si.get_data(yahoo_ticker, start_date=last_bus_day.date(), end_date=(last_bus_day + 1).date())
        return stock_data.iloc[0].close

    def get_market_cap(self, yahoo_ticker):
        stats = si.get_stats(yahoo_ticker)
        market_cap = stats[stats.Attribute.str.contains('Market Cap')].Value[0]
        return float(re.sub("[A-Z]+", " ", market_cap))


def get_daily_stock_price_data(stock_search_term, exchanges, start_date='2019-08-01', end_date='2019-08-02'):
    # need to strip Inc. from search term
    yahoo_formatted_ticker = get_yahoo_ticker(stock_search_term, exchanges)
    stock_data = si.get_data(yahoo_formatted_ticker, start_date=start_date, end_date=end_date)
    return stock_data


def get_latest_closing_price(ticker):
    last_bus_day = pd.bdate_range(start=dt.date.today() - dt.timedelta(days=5), end=dt.date.today())[-1]
    stock_data = si.get_data(ticker, start_date=(last_bus_day).date(), end_date=(last_bus_day+1).date())
    return stock_data.iloc[0].close


def get_yahoo_ticker(constituent_name, bloomberg_code, exchanges=['TOR'], default='{}.TO'):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(constituent_name)
    result = requests.get(url).json()
    possible_listings = result['ResultSet']['Result']
    wanted_listing = [l for l in possible_listings if l['exch'] in exchanges]
    if (len(wanted_listing) == 0):
        #print('found: {}/{} listings matching {}'.format(wanted_listing, possible_listings, constituent_name))
        return default.format(bloomberg_code)
    if len(wanted_listing) > 1:
        #print('{} matches for {}'.format(len(wanted_listing), constituent_name))
        #[print(el) for el in wanted_listing]
        pass
    return wanted_listing[0]['symbol']


class TestIndexConstituentLoader(object):
    def __init__(self, constituent_csv):
        self._input_file = constituent_csv
        self._data_start_line = 'Constituent Name,Symbol'
        to_remove = ['Limited', 'Inc.', 'Ltd.', 'Corp.', 'Corporation', 'Investment Trust']
        self._remove_from_company_regex = re.compile('|'.join(to_remove))

    def load_constituents_with_price_data(self):
        raw_df = self._parse_input_data()
        formatted = self._format_input_data(raw_df)
        formatted_with_ticker = self._fill_yahoo_ticker(formatted)
        #with_closing_price = self._fill_closing_price(formatted_with_ticker)
        return formatted_with_ticker

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
        return raw_data

    def _fill_yahoo_ticker(self, df):
        col_name = '{}Ticker'.format(SourceTypes.YAHOO)
        df[col_name] = df.apply(lambda x: get_yahoo_ticker(x['SearchData'], x['Symbol']), axis=1)
        return df

    def _format_company_name_for_search(self, company_name):
        return self._remove_from_company_regex.split(company_name)[0]

    def _fill_closing_price(self, df):
        df['ClosingPrice'] = df['YahooTicker'].apply(get_latest_closing_price)
        return df


def main():
    loader = TestIndexConstituentLoader(r'C:\Users\meeha\PycharmProjects\IndexSandbox\src\data\index_constituents.csv')
    res = loader._parse_input_data()
    formatted = loader._format_input_data(res)
    formatted_with_ticker = loader._fill_yahoo_ticker(formatted)
    with_closing_price = loader._fill_closing_price(formatted_with_ticker)
    print('here')



if __name__ == '__main__':
    main()
