import pandas as pd
from talib import MA_Type
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count, DataReader


class BBANDS(Indicator):
    NAME = 'bbands'

    def __init__(self, currency_pair='btc_jpy', period='1d', length=25, matype=MA_Type.EMA):
        super().__init__(currency_pair, period)
        self.length = length
        self.matype = matype

    @staticmethod
    def _get_required_price_count(length, count):
        return length + count - 1

    @staticmethod
    def _formatting(candlesticks_df, bbands, style):
        bbands_with_time = pd.concat([candlesticks_df['time'], bbands[['lowerband', 'upperband']]], axis=1)
        bbands_with_time.dropna(inplace=True)

        if style == 'df':
            return bbands_with_time.reset_index(drop=True)
        elif style == 'dict':
            dict_bands = bbands_with_time.astype(object).to_dict(orient='records')
            return dict_bands
        else:
            raise ValueError('not supported style')

    @classmethod
    def create_data_from_prices(cls, price_data_df, lowbd=2, upbd=2, length=25, matype=MA_Type.EMA, style='dict'):
        bbands = cls._exec_talib_func(price_data_df,
                                      timeperiod=length,
                                      nbdevdn=lowbd,
                                      nbdevup=upbd,
                                      matype=matype)

        formatted_bbands = cls._formatting(price_data_df, bbands, style)
        return formatted_bbands

    def request_data(self, count=100, lowbd=2, upbd=2, style='dict'):
        count = min(count, self.MAX_COUNT)
        price_data = get_data_by_count(currency_pair=self.currency_pair,
                                       period=self.period,
                                       count=self._get_required_price_count(self.length, count),
                                       style='df')

        return self.create_data_from_prices(price_data, lowbd, upbd, self.length, self.matype, style)

    def request_data_by_period(self, start, end, lowbd=2, upbd=2, style='dict'):
        price_data = DataReader(currency_pair=self.currency_pair,
                                period=self.period,
                                start=start,
                                end=end,
                                style='df')

        return self.create_data_from_prices(price_data, lowbd, upbd, self.length, self.matype, style)
