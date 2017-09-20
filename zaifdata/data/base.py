from abc import ABCMeta, abstractmethod
from zaifdata.core import ZaifChartApi
import pandas
import time


class _BaseData(metaclass=ABCMeta):
    _data_styles = ('df', 'dict')

    def __init__(self):
        self.data = None

    @abstractmethod
    def read(self, *args, **kwargs):
        raise NotImplementedError

    def to_dict(self):
        return self.data

    def to_df(self):
        df = pandas.DataFrame(self.data)
        return df

    def to_any_style(self, style):
        if style not in self._data_styles:
            raise Exception("unexpected data style: '{}'".format(style))
        # fixme: define custom exception

        to_style = 'to_' + style
        return getattr(self, to_style)()

    def count(self):
        return len(self.data)


class HistoricalPrices(_BaseData):
    def __init__(self, currency_pair, period):
        super().__init__()
        self.currency_pair = currency_pair
        self.period = period
        self.data_source = ZaifChartApi()

    def read(self, from_, to_):
        self.data = self.data_source.history(currency_pair=self.currency_pair,
                                             period=self.period,
                                             from_sec=from_,
                                             to_sec=to_)
        return self

    def read_by_count(self, count):
        now = int(time.time())

        # Always fetch 'count + 1' data and take only 'count'.
        # This is because the number of data server returns is smaller than expected count by 1
        # when server generate new data.
        from_ = now - _PeriodSec[self.period] * (count + 1)
        self.data = self.data_source.history(currency_pair=self.currency_pair,
                                             period=self.period,
                                             from_sec=from_,
                                             to_sec=now)[-count:]
        return self

#  fixme 1: not calc, but set const
#  fixme 2: define 'period' class
_PeriodSec = {
    '1m': 60,
    '5m': 60 * 5,
    '15m': 60 * 15,
    '30m': 60 * 30,
    '1h': 60 * 60,
    '4h': 60 * 60 * 4,
    '8h': 60 * 60 * 8,
    '12h': 60 * 60 * 12,
    '1d': 60 * 60 * 24,
}
