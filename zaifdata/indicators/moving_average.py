from abc import ABCMeta
import pandas as pd
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count, DataReader


class _MA(Indicator, metaclass=ABCMeta):
    def __init__(self, currency_pair='btc_jpy', period='1d', length=25):
        super().__init__(currency_pair, period)
        self.length = length

    @staticmethod
    def _get_required_price_count(length, count):
        return count + length - 1

    @classmethod
    def _formatting(cls, price_data, ma, style):
        ma.rename(cls.NAME, inplace=True)
        ma_with_time = pd.concat([price_data['time'], ma], axis=1)
        ma_with_time.dropna(inplace=True)

        if style == 'df':
            return ma_with_time.reset_index(drop=True)
        elif style == 'dict':
            dict_ma = ma_with_time.astype(object).to_dict(orient='records')
            return dict_ma
        else:
            raise ValueError('not supported style')

    @classmethod
    def create_data_from_prices(cls, price_data, length, style):
        ma = cls._exec_talib_func(price_data, timeperiod=length)
        formatted_ma = cls._formatting(price_data, ma, style)
        return formatted_ma

    def request_data(self, count=100, style='dict'):
        count = min(count, self.MAX_COUNT)
        price_data = get_data_by_count(currency_pair=self.currency_pair,
                                       period=self.period,
                                       count=self._get_required_price_count(self.length, count),
                                       style='df')

        return self.create_data_from_prices(price_data, self.length, style)

    def request_data_by_period(self, start, end, style='dict'):
        price_data = DataReader(currency_pair=self.currency_pair,
                                period=self.period,
                                start=start,
                                end=end,
                                style='df')

        return self.create_data_from_prices(price_data, self.length, style)

    def is_increasing(self):
        previous, last = self.request_data(count=2, style='dict')
        return last[self.NAME] > previous[self.NAME]

    def is_decreasing(self):
        previous, last = self.request_data(count=2, style='dict')
        return last[self.NAME] < previous[self.NAME]


class EMA(_MA):
    NAME = 'ema'


class SMA(_MA):
    NAME = 'sma'
