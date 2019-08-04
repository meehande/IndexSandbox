import abc


class Index(object):
    def __init__(self, bloomberg_code, underlyings, currency, index_level=None, index_divisor=None):
        self.bbg = bloomberg_code  # 'SPTSX'
        self.underlyings = underlyings  # df with all different representations?
        self.divisor = index_divisor  # should this be in this class?
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


class IndexMembersFinder(abc.ABC):
    @abc.abstractmethod
    def find_underlyings(self):
        return []


class IndexMethodologyBuilder(abc.ABC):
    def __init__(self, member_finder):
        self._member_finder = member_finder

    @abc.abstractmethod
    def find_underlyings(self):
        return []


class SPTSXMembersFinder(IndexMembersFinder):
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


class IndexMethodologyBuilderFactory(object):
    _INDEX_TO_MEMBER_FINDER = {'SPTSX': SPTSXMembersFinder}

    def get_index_builder(self, bloomberg_code):
        member_finder = self._INDEX_TO_MEMBER_FINDER.get(bloomberg_code)
        if member_finder is None:
            raise NotImplementedError('No MemberFinder defined for {}'.format(bloomberg_code))





