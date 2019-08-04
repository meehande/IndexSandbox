from src.data_loading.stock_data_loader import YahooStockDataLoader
from src.data_loading.underlying_loader import IndexUnderlyingCsvLoader
from src.index import Index
from src.index_pricing import IndexCalculator


def main():
    underlyings_csv = r'C:\Users\meeha\PycharmProjects\IndexSandbox\src\data\index_constituents.csv'
    calculator = IndexCalculator()
    price_loader = YahooStockDataLoader()
    constituents_loader = IndexUnderlyingCsvLoader(underlyings_csv, price_loader)
    constituents = constituents_loader.load_underlyings()
    sptsx = Index('SPTSX', constituents, 'CAD', index_level=16271.66)  # TODO: get this from somehwere else (or divisor)
    print("Index: {}".format(sptsx))
    divisor = calculator.calculate_index_divisor(sptsx, price_loader)
    print("Index Divisor: {}".format(divisor))


if __name__ == '__main__':
    main()
