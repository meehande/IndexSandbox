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





