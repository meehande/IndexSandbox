import abc
import datetime as dt
from src.index_pricing import IndexCalculator
from src.utils.calculation_utils import calculate_vwap, get_n_business_dates, subtract_from_date
from src.data_loading.stock_data_loader import YahooStockDataLoader


class IndexMembersFinder(abc.ABC):
    @abc.abstractmethod
    def find_underlyings(self):
        return []


class SPTSXMembersFinder(IndexMembersFinder):
    def __init__(self, bloomberg_code='SPTSX', index_calculator=IndexCalculator,
                 stock_data_loader=YahooStockDataLoader):
        self.bloomberg_code = bloomberg_code
        self._index_calculator = index_calculator
        self._stock_data_loader = stock_data_loader
        self.min_weight = 0.04 / 100
        self.min_vwap = 1
        self.computation_date = dt.date().today()

    def find_underlyings(self):
        stocks = self._get_all_possible_stocks()
        stocks = self._min_vwap_filter(stocks)
        stocks = self._min_weight_filter(stocks)
        #TODO: minweight criteria mentionds 10-day vwap - need to use? to calc??
        #TODO: liquidity criteria
        return stocks

    def _cap_constituent_weights(self):
        # caps weight to 25%
        # this is in a different index in the family
        pass

    def _get_all_possible_stocks(self):
        """
        :return: all stocks listed on TSX that need to be checked for eligibilty
        """
        # TODO!
        return []

    def _get_ten_day_vwap(self, df):
        last_ten_bus_days = get_n_business_dates(10, end_date=self.computation_date)
        # TODO: this doesn't work exactly right -> depends on type of tradedate
        mask = df['TradeDate'].isin(last_ten_bus_days)
        df[mask] = calculate_vwap(df[mask])
        return df

    def get_qmv(self):
        pass

    def _get_three_month_vwap(self, df):
        last_three_months = subtract_from_date(self.computation_date, months=3)
        mask = df['TradeDate'].isin(last_three_months)
        df[mask] = calculate_vwap(df[mask])
        return df

    def _get_weight(self, df):
        df = self._index_calculator.calculate_market_cap_and_weights(df, self._stock_data_loader)
        return df

    def _get_liquidity(self):
        """
        by float turnover (total number of shares traded in Canada and U.S.1
        in
        the previous 12 months divided by float-adjusted shares outstanding at the end of the period). Liquidity
        must be at least 0.50. For dual-listed stocks, liquidity must also be at least 0.25 when using Canadian
        volume only.
                :return:
        """
        pass

    def _min_weight_filter(self, df):
        return df[df['Weight'] > self.min_weight]

    def _min_vwap_filter(self, df):
        return df[df['VWAP'] > self.min_vwap]
