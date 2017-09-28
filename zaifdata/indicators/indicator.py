from abc import ABCMeta, abstractmethod
from talib import abstract


class Indicator(metaclass=ABCMeta):
    MAX_COUNT = 1000
    NAME = None

    def __init__(self, currency_pair, period):
        self.currency_pair = currency_pair
        self.period = period

    @classmethod
    def _exec_talib_func(cls, *args, **kwargs):
        return abstract.Function(cls.NAME)(*args, **kwargs)

    @classmethod
    @abstractmethod
    def create_data_from_prices(cls, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _get_required_price_count(arg, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def request_data(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def request_data_by_period(self, *args, **kwargs):
        raise NotImplementedError
