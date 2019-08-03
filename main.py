from src.data_loading.stock_data_loader import YahooStockDataLoader
from src.data_loading.underlying_loader import IndexUnderlyingCsvLoader
from src.index import Index
from src.index_pricing import IndexCalculator


def main():
    constituents_loader = IndexUnderlyingCsvLoader(r'C:\Users\meeha\PycharmProjects\IndexSandbox\src\data\index_constituents.csv')
    constituents = constituents_loader.load_underlyings()
    sptsx = Index('SPTSX', constituents, 'CAD', index_level=16271.66)  # TODO: get this from somehwere else (or divisor)
    print("Index: {}".format(sptsx))
    calculator = IndexCalculator()
    price_loader = YahooStockDataLoader()
    divisor = calculator.calculate_index_divisor(sptsx, price_loader)
    print("Index Divisor: {}".format(divisor))



if __name__ == '__main__':
    main()
