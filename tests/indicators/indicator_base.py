from abc import abstractmethod, ABCMeta


class IndicatorTestMixIn(metaclass=ABCMeta):

    @abstractmethod
    def test_name(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def test_request_data(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def test_request_data_by_period(self, *args, **kwargs):
        raise NotImplementedError
