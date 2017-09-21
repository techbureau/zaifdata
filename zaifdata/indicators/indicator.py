from abc import ABCMeta, abstractmethod
from talib import abstract


class Indicator(metaclass=ABCMeta):
    MAX_COUNT = 1000

    def __init__(self, currency_pair, period):
        self.currency_pair = currency_pair
        self.period = period

    @abstractmethod
    def request_data(self, *args, **kwargs):
        raise NotImplementedError

    def _exec_talib_func(self, *args, **kwargs):
        return abstract.Function(self.name)(*args, **kwargs)

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def _get_required_price_count(self, *args, **kwargs):
        raise NotImplementedError
