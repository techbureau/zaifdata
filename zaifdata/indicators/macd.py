import pandas as pd
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count


class MACD(Indicator):
    def __init__(self, currency_pair='btc_jpy', period='1d', short=12, long=26, signal=9):
        super().__init__(currency_pair, period)
        self.short = short
        self.long = long
        self.signal = signal

    def request_data(self, count=100, to_epoch_time=None, style='dict'):
        price_data = get_data_by_count(currency_pair=self.currency_pair,
                                       period=self.period,
                                       count=self._get_required_price_count(count),
                                       style='df')

        macd = self._exec_talib_func(price_data,
                                     price='close',
                                     fastperiod=self.short,
                                     slowperiod=self.long,
                                     signalperiod=self.signal)

        formatted_macd = self._formatting(price_data, macd, style)
        return formatted_macd

    @property
    def name(self):
        return 'macd'

    def _get_required_price_count(self, count):
        return count + self.long + self.signal - 2

    @staticmethod
    def _formatting(candlesticks_df, macd, style):
        macd_with_time = pd.concat([candlesticks_df['time'], macd], axis=1)
        macd_with_time.dropna(inplace=True)
        if style == 'df':
            return macd_with_time.reset_index(drop=True)

        dict_macd = macd_with_time.astype(object).to_dict(orient='records')
        return dict_macd