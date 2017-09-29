import unittest
from unittest.mock import MagicMock, patch
from .indicator_base import IndicatorTestMixIn
from zaifdata.indicators.bollinger_bands import BBANDS
from tests.test_data.get_test_data import get_test_price_data
from pandas.util.testing import assert_frame_equal
import pandas as pd


class TestBBands(unittest.TestCase, IndicatorTestMixIn):
    @classmethod
    def setUpClass(cls):
        cls.bands = BBANDS

    def test_name(self):
        self.assertEqual(self.bands.NAME, 'bbands')

    def test_request_data_by_period(self):
        bands = self.bands(currency_pair='kong_coin', period='forever', length='so_long')

        with patch('zaifdata.indicators.bollinger_bands.get_data_by_count',
                   return_value='price_data') as mock_get_data:

    def test_request_data(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    unittest.main()