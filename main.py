from src.stock_data_loader import TestIndexConstituentLoader, YahooStockPriceLoader
from src.index import Index
from src.index_pricing import IndexCalculator


def main():
    constituents_loader = TestIndexConstituentLoader(r'C:\Users\meeha\PycharmProjects\IndexSandbox\src\data\index_constituents.csv')
    constituents = constituents_loader.load_constituents_with_price_data()
    sptsx = Index('SPTSX', constituents, 'CAD', index_level=16271.66)  # TODO: get this from somehwere else (or divisor)
    print("Index: {}".format(sptsx))
    calculator = IndexCalculator()
    price_loader = YahooStockPriceLoader()
    divisor = calculator.calculate_index_divisor(sptsx, price_loader)
    print("Index Divisor: {}".format(divisor))



if __name__ == '__main__':
    main()
