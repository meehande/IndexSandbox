import numpy as np
from src.data_loading.stock_data_loader import SourceTypes


class IndexCalculator(object):
    def calculate_market_cap_and_weights(self, index, price_loader):
        ticker_col = '{}Ticker'.format(price_loader.price_source)
        calculation_df = index.underlyings[[ticker_col]]
        calculation_df['ClosingPrice'] = calculation_df[ticker_col].apply(price_loader.get_latest_closing_price)
        calculation_df['MarketCap'] = calculation_df[ticker_col].apply(price_loader.get_market_cap)
        total_market_cap = calculation_df['MarketCap'].sum()
        calculation_df['Weight'] = calculation_df['MarketCap'] / total_market_cap
        return calculation_df

    def calculate_index_level(self, index, price_loader):
        constituent_prices = self.calculate_market_cap_and_weights(index, price_loader)
        total_market_cap = np.sum(constituent_prices['MarketCap'])
        return total_market_cap/index.divisor

    def calculate_index_divisor(self, index, price_loader):
        constituent_prices = self.calculate_market_cap_and_weights(index, price_loader)
        total_market_cap = np.sum(constituent_prices['MarketCap'])
        return total_market_cap / index.level



