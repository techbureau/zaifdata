import pandas as pd
from talib import MA_Type
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count, DataReader


class BBANDS(Indicator):
    def __init__(self, currency_pair='btc_jpy', period='1d', length=25, matype=MA_Type.EMA):
        super().__init__(currency_pair, period)
        self.length = length
        self.matype = matype

    def request_data(self, count=100, lowbd=2, upbd=2, style='dict'):
        count = min(count, self.MAX_COUNT)
        price_data = get_data_by_count(currency_pair=self.currency_pair,
                                       period=self.period,
                                       count=self._get_required_price_count(count),
                                       style='df')

        return self._create_bollinger_bands(price_data, lowbd, upbd, style)

    def request_data_by_period(self, start, end, lowbd=2, upbd=2, style='dict'):
        price_data = DataReader(currency_pair=self.currency_pair,
                                period=self.period,
                                start=start,
                                end=end,
                                style='df')

        return self._create_bollinger_bands(price_data, lowbd, upbd, style)

    def _create_bollinger_bands(self, price_data, lowbd, upbd, style):
        bbands = self._exec_talib_func(price_data,
                                       timeperiod=self.length,
                                       nbdevdn=lowbd,
                                       nbdevup=upbd,
                                       matype=self.matype)

        formatted_bbands = self._formatting(price_data, bbands, style)
        return formatted_bbands

    @property
    def name(self):
        return 'bbands'

    def _get_required_price_count(self, count):
        return self.length + count - 1

    @staticmethod
    def _formatting(candlesticks_df, bbands, style):
        bbands_with_time = pd.concat([candlesticks_df['time'], bbands[['lowerband', 'upperband']]], axis=1)
        bbands_with_time.dropna(inplace=True)

        if style == 'df':
            return bbands_with_time.reset_index(drop=True)

        dict_bands = bbands_with_time.astype(object).to_dict(orient='records')
        return dict_bands
