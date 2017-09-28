import pandas as pd
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count, DataReader


class ADX(Indicator):
    NAME = 'adx'

    def __init__(self, currency_pair='btc_jpy', period='1d', length=14):
        super().__init__(currency_pair, period)
        self.length = length

    @staticmethod
    def _get_required_price_count(length, count):
        return 2 * length - 1 + count

    @classmethod
    def create_data_from_prices(cls, price_data_df, length=14, style='dict'):
        adx = cls._exec_talib_func(price_data_df,
                                   timeperiod=length,
                                   prices=['high', 'low', 'close'])

        formatted_adx = cls._formatting(price_data_df, adx, style)
        return formatted_adx

    @classmethod
    def _formatting(cls, candlesticks_df, adx, style):
        adx.rename(cls.NAME, inplace=True)
        adx_with_time = pd.concat([candlesticks_df['time'], adx], axis=1)
        adx_with_time.dropna(inplace=True)

        if style == 'df':
            return adx_with_time.reset_index(drop=True)
        elif style == 'dict':
            dict_adx = adx_with_time.astype(object).to_dict(orient='records')
            return dict_adx
        else:
            raise Exception

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


