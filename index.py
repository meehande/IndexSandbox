import abc


class Index(object):
    def __init__(self, bloomberg_code, underlyings, currency, index_level=None, index_divisor=None):
        self.bbg = bloomberg_code  # 'SPTSX'
        self.underlyings = underlyings  # df with all different representations?
        self.divisor = index_divisor # should this be in this class?
        self.level = index_level
        self.currency = currency

    def __str__(self):
        return 'BloombergCode: {} | ' \
               'Divisor: {} | ' \
               'Level: {} | ' \
               'Currency: {} '.format(self.bbg,
                                      self.divisor,
                                      self.level,
                                      self.currency)


class IndexBuilder(object):
    def __init__(self, data_loader):
        self._data_loader = data_loader

    def build_index(self, index_bloomberg):
        currency = self._data_loader.get_currency(index_bloomberg)
        underlyings = self._data_loader.get_underlyings()
        index = Index(index_bloomberg, underlyings, currency)




class IndexConstituentsFinder(abc.ABC):
    @abc.abstractmethod
    def find_underlyings(self):
        return []


class SPXTSXCompositeConstituentsFinder(IndexConstituentsFinder):
    def __init__(self, bloomberg_code='SPTSX'):
        self.bloomberg_code = bloomberg_code

    def find_underlyings(self):

        return super.find_underlyings()

    def _cap_constituent_weights(self):
        # caps weight to 25%
        # this is in a different index in the family
        pass

    def get_constituents(self):
        pass







