import pandas as pd
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count, DataReader


class RSI(Indicator):
    NAME = 'rsi'

    def __init__(self, currency_pair='btc_jpy', period='1d', length=14):
        super().__init__(currency_pair, period)
        self.length = length

    @staticmethod
    def _get_required_price_count(length, count):
        return count + length

    @classmethod
    def _formatting(cls, candlesticks, rsi, style):
        rsi.rename(cls.NAME, inplace=True)
        rsi_with_time = pd.concat([candlesticks['time'], rsi], axis=1)
        rsi_with_time.dropna(inplace=True)

        if style == 'df':
            return rsi_with_time.reset_index(drop=True)
        elif style == 'dict':
            dict_rsi = rsi_with_time.astype(object).to_dict(orient='records')
            return dict_rsi
        else:
            raise ValueError('not supported style')

    @classmethod
    def create_data_from_prices(cls, price_data_df, length, style):
        rsi = cls._exec_talib_func(price_data_df, price='close', timeperiod=length)
        formatted_rsi = cls._formatting(price_data_df, rsi, style)
        return formatted_rsi

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
