import unittest
from unittest.mock import MagicMock
from zaifdata.data_source import ZaifChartApi
import time


class TestDataSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = ZaifChartApi()

    def test_history(self):
        now = int(time.time())
        month_ago = int(time.time()) - 1 * 60 * 60 * 24 * 30
        self.api._execute_api = MagicMock()
        params = {
            'currency_pair': 'TEST',
            'period': '1d',
            'from_sec': month_ago,
            'to_sec': now
        }
        self.api.history(**params)

        expected_param = {
            'symbol': 'TEST',
            'resolution': 'D',
            'from': month_ago,
            'to': now
        }
        self.api._execute_api.assert_called_once_with('history', expected_param)

    def test_convert_resolution(self):
        periods = [
            '1m',
            '5m',
            '15m',
            '30m',
            '1h',
            '4h',
            '8h',
            '12h',
            '1d',
        ]

        resolutions = [
            '1',
            '5',
            '15',
            '30',
            '60',
            '240',
            '480',
            '720',
            'D',
        ]

        for i in range(len(periods)):
            with self.subTest(i=i):
                self.assertEqual(self.api._period_to_resolution(periods[i]),
                                 resolutions[i])

if __name__ == '__main__':
    unittest.main()
