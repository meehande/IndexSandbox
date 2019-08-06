import numpy as np
from src.data_loading.stock_data_loader import SourceTypes


class IndexCalculator(object):
    def calculate_market_cap_and_weights(self, index):
        calculation_df = index.underlyings
        total_market_cap = calculation_df['MarketCap'].sum()
        calculation_df['Weight'] = calculation_df['MarketCap'] / total_market_cap
        return calculation_df

    def calculate_index_level(self, index):
        constituent_prices = self.calculate_market_cap_and_weights(index)
        total_market_cap = np.sum(constituent_prices['MarketCap'])
        return total_market_cap/index.divisor

    def calculate_index_divisor(self, index):
        constituent_prices = self.calculate_market_cap_and_weights(index)
        total_market_cap = np.sum(constituent_prices['MarketCap'])
        return total_market_cap / index.level



