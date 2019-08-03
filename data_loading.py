import abc


class IndexDataLoader(abc.ABC):
    @abc.abstractmethod
    def get_index_underlyings(self, index_bloomberg):
        return []

    @abc.abstractmethod
    def get_index_currency(self, index_bloomberg):
        return ''


class LocalDataLoader(IndexDataLoader):
    def get_underlyings(self, index_bloomberg):
        pass

    def get_currency(self, index_bloomberg):
        pass
