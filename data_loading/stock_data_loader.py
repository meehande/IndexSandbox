import requests
import re
import datetime as dt
import abc
from yahoo_fin import stock_info as si
import pandas as pd
from enum import Enum


class SourceTypes(Enum):
    YAHOO = 'YAHOO'


class StockDataLoader(abc.ABC):
    @abc.abstractmethod
    def get_latest_closing_price(self, ticker):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_market_cap(self, yahoo_ticker):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_ticker(self, company_name, bloomberg_code, exchanges=['TOR'], default='{}.TO'):
        raise NotImplementedError()


class YahooStockDataLoader(StockDataLoader):
    def __init__(self):
        self.price_source = SourceTypes.YAHOO
        self._latest_bus_day = pd.bdate_range(start=dt.date.today() - dt.timedelta(days=5), end=dt.date.today())[-1].date()
        self._ticker_search_url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en"

    def get_latest_closing_price(self, yahoo_ticker):
        try:
            stock_data = si.get_data(yahoo_ticker, start_date=self._latest_bus_day,
                                     end_date=(self._latest_bus_day + dt.timedelta(days=1)))
        except ValueError as ex:
            print('Could not find stock data for: {}'.format(yahoo_ticker))
            raise

        return stock_data.iloc[0].close

    def get_market_cap(self, yahoo_ticker):
        stats = si.get_stats(yahoo_ticker)
        market_cap = stats[stats.Attribute.str.contains('Market Cap')].Value[0]
        return float(re.sub("[A-Z]+", " ", market_cap))

    def get_ticker(self, company_name, bloomberg_code, exchanges=['TOR'], default='{}.TO'):
        url = self._ticker_search_url.format(company_name)
        result = requests.get(url).json()
        possible_listings = result['ResultSet']['Result']
        wanted_listing = [l for l in possible_listings if l['exch'] in exchanges]
        if len(wanted_listing) == 0:
            # print('found: {}/{} listings matching {}'.format(wanted_listing, possible_listings, constituent_name))
            return default.format(bloomberg_code.replace('.', '-'))
        if len(wanted_listing) > 1:
            # print('{} matches for {}'.format(len(wanted_listing), constituent_name))
            # [print(el) for el in wanted_listing]
            pass
        return wanted_listing[0]['symbol']
