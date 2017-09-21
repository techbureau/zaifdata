import unittest
from unittest.mock import Mock
from zaifdata.data_source import ZaifChartApi
import time


class TestDataSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = ZaifChartApi()

    def test_history(self):
        now = int(time.time())
        month_ago = int(time.time()) - 1 * 60 * 60 * 24 * 30
        self.api._execute_api = Mock()
        params = {
            'currency_pair': 'xem_jpy',
            'period': '1d',
            'from_sec': month_ago,
            'to_sec': now
        }
        self.api.history(**params)

        expected_param = {
            'symbol': 'xem_jpy',
            'resolution': 'D',
            'from': month_ago,
            'to': now
        }
        self.api._execute_api.assert_called_once_with('history', expected_param)


if __name__ == '__main__':
    unittest.main()
