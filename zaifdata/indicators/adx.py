import pandas as pd
from .indicator import Indicator
from zaifdata.data.prices import get_data_by_count, DataReader


class ADX(Indicator):
    def __init__(self, currency_pair='btc_jpy', period='1d', length=14):
        super().__init__(currency_pair, period)
        self.length = length

    def request_data(self, count=100, style='dict'):
        count = min(count, self.MAX_COUNT)
        price_data = get_data_by_count(currency_pair=self.currency_pair,
                                       period=self.period,
                                       count=self._get_required_price_count(count),
                                       style='df')

        return self._create_adx(price_data, style)

    def request_data_by_period(self, start, end, style='dict'):
        price_data = DataReader(currency_pair=self.currency_pair,
                                period=self.period,
                                start=start,
                                end=end,
                                style='df')

        return self._create_adx(price_data, style)

    def _create_adx(self, price_data, style):
        adx = self._exec_talib_func(price_data,
                                    timeperiod=self.length,
                                    prices=['high', 'low', 'close'])

        formatted_adx = self._formatting(price_data, adx, style)
        return formatted_adx

    @property
    def name(self):
        return 'adx'

    def _get_required_price_count(self, count):
        return 2 * self.length - 1 + count

    def _formatting(self, candlesticks_df, adx, style):
        adx.rename(self.name, inplace=True)
        adx_with_time = pd.concat([candlesticks_df['time'], adx], axis=1)
        adx_with_time.dropna(inplace=True)

        if style == 'df':
            return adx_with_time.reset_index(drop=True)

        dict_adx = adx_with_time.astype(object).to_dict(orient='records')
        return dict_adx
