from abc import ABCMeta
import pandas as pd
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count


class _MA(Indicator, metaclass=ABCMeta):
    def __init__(self, currency_pair='btc_jpy', period='1d', length=25):
        super().__init__(currency_pair, period)
        self.length = length

    def request_data(self, count=100, to_epoch_time=None, style='dict'):
        price_data = get_data_by_count(currency_pair=self.currency_pair,
                                       period=self.period,
                                       count=self._get_required_price_count(count),
                                       style='df')

        ma = self._exec_talib_func(price_data, timeperiod=self.length)
        formatted_ma = self._formatting(price_data, ma, style)
        return formatted_ma

    def _get_required_price_count(self, count):
        return count + self.length - 1

    def is_increasing(self):
        previous, last = self.request_data(count=2, style='dict')
        return last[self.name] > previous[self.name]

    def is_decreasing(self):
        previous, last = self.request_data(count=2, style='dict')
        return last[self.name] < previous[self.name]

    def _formatting(self, price_data, ma, style):
        ma.rename(self.name, inplace=True)
        ma_with_time = pd.concat([price_data['time'], ma], axis=1)
        ma_with_time.dropna(inplace=True)

        if style == 'df':
            return ma_with_time.reset_index(drop=True)

        dict_ma = ma_with_time.astype(object).to_dict(orient='records')
        return dict_ma


class EMA(_MA):
    @property
    def name(self):
        return 'ema'


class SMA(_MA):
    @property
    def name(self):
        return 'sma'
