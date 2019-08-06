import abc
from src.index_methodology.index_membership_evaluator import SPTSXMembersFinder


class IndexMethodologyBuilder(abc.ABC):
    def __init__(self, member_finder):
        self._member_finder = member_finder

    @abc.abstractmethod
    def find_underlyings(self):
        raise NotImplementedError()


class IndexMethodologyBuilderFactory(object):
    _INDEX_TO_MEMBER_FINDER = {'SPTSX': SPTSXMembersFinder}

    def get_index_builder(self, bloomberg_code):
        member_finder = self._INDEX_TO_MEMBER_FINDER.get(bloomberg_code)
        if member_finder is None:
            raise NotImplementedError('No MemberFinder defined for {}'.format(bloomberg_code))
        return IndexMethodologyBuilder(member_finder)


