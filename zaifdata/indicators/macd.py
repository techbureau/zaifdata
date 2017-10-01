import pandas as pd
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count, DataReader


class MACD(Indicator):
    NAME = 'macd'

    def __init__(self, currency_pair='btc_jpy', period='1d', short=12, long=26, signal=9):
        super().__init__(currency_pair, period)
        self.short = short
        self.long = long
        self.signal = signal

    @staticmethod
    def _formatting(candlesticks_df, macd, style):
        macd_with_time = pd.concat([candlesticks_df['time'], macd], axis=1)
        macd_with_time.dropna(inplace=True)
        if style == 'df':
            return macd_with_time.reset_index(drop=True)
        elif style == 'dict':
            dict_macd = macd_with_time.astype(object).to_dict(orient='records')
            return dict_macd
        else:
            raise ValueError('not supported style')

    @staticmethod
    def _get_required_price_count(long, signal, count):
        return count + long + signal - 2

    @classmethod
    def create_data_from_prices(cls, price_data_df, short, long, signal, style='dict'):
        macd = cls._exec_talib_func(price_data_df,
                                    price='close',
                                    fastperiod=short,
                                    slowperiod=long,
                                    signalperiod=signal)

        formatted_macd = cls._formatting(price_data_df, macd, style)
        return formatted_macd

    def request_data(self, count=100, style='dict'):
        count = min(count, self.MAX_COUNT)
        price_data = get_data_by_count(currency_pair=self.currency_pair,
                                       period=self.period,
                                       count=self._get_required_price_count(count),
                                       style='df')

        return self.create_data_from_prices(price_data, self.short, self.long, self.signal, style)

    def request_data_by_period(self, start, end, style='dict'):
        price_data = DataReader(currency_pair=self.currency_pair,
                                period=self.period,
                                start=start,
                                end=end,
                                style='df')

        return self.create_data_from_prices(price_data, self.short, self.long, self.signal, style)
