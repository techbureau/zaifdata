import json
import inspect
import requests


class ZaifChartApi:
    _API_URL = 'https://zaif.jp/zaif_chart_api/v1/{}'

    def history(self, currency_pair, period, from_sec, to_sec):
        resolution = self._period_to_resolution(period)
        params = {
            'symbol': currency_pair,
            'resolution': resolution,
            'from': from_sec,
            'to': to_sec
        }

        return self._execute_api(inspect.currentframe().f_code.co_name, params)

    def _execute_api(self, func_name, params=None):
        url = self._API_URL.format(func_name)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        ohlc_data = json.loads(json.loads(response.text), parse_constant=str)['ohlc_data']
        return list(map(self._time_digits_adjust, ohlc_data))

    @staticmethod
    def _period_to_resolution(period):
        conversion_table = {
            '1m': '1',
            '5m': '5',
            '15m': '15',
            '30m': '30',
            '1h': '60',
            '4h': '240',
            '8h': '480',
            '12h': '720',
            '1d': 'D',
        }
        resolution = conversion_table.get(period, None)
        if not resolution:
            raise ValueError('error: Unexpected period')
        return resolution

    @staticmethod
    def _time_digits_adjust(an_olhc_data):
        an_olhc_data['time'] = str(int(an_olhc_data['time'] / 1000))
        return an_olhc_data
