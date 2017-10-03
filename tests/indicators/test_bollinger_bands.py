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
        bands = self.bands(currency_pair='kong_coin', period='forever', matype='test', length='so_long')
        bands.create_data_from_prices = MagicMock()

        with patch('zaifdata.indicators.bollinger_bands.DataReader',
                   return_value='price_data') as mock_get_data:
            bands.request_data_by_period(start=0, end=100, style='dict')
            mock_get_data.assert_called_once_with(currency_pair='kong_coin',
                                                  period='forever',
                                                  start=0,
                                                  end=100,
                                                  style='df')

            bands.create_data_from_prices.assert_called_once_with('price_data', 2, 2, 'so_long', 'test', 'dict')

    def test_request_data(self):
        bands = self.bands(currency_pair='kong_coin', period='forever', matype='test', length=20)
        bands.create_data_from_prices = MagicMock()

        with patch('zaifdata.indicators.bollinger_bands.get_data_by_count',
                   return_value='price_data') as mock_get_data:
            bands.request_data(count=20, style='dict')
            mock_get_data.assert_called_once_with(currency_pair='kong_coin',
                                                  period='forever',
                                                  count=39,
                                                  style='df')

            bands.create_data_from_prices.assert_called_once_with('price_data', 2, 2, 20, 'test', 'dict')

    def test_create_bands_df_data_from_prices(self):
        price_data = get_test_price_data()
        self.assertListEqual(self.bands.create_data_from_prices(
            price_data_df=price_data,
            length=105),
            [
                {'upperband': 35.35302638099354, 'time': 1496617200, 'lowerband': 18.564164095196958},
                {'upperband': 35.2722508483616, 'time': 1496631600, 'lowerband': 18.623860562240395},
                {'upperband': 35.226874519065156, 'time': 1496646000, 'lowerband': 18.615725355487747},
                {'upperband': 35.20458122661314, 'time': 1496660400, 'lowerband': 18.58325261257084},
                {'upperband': 35.181145611872665, 'time': 1496674800, 'lowerband': 18.554087588836147}
            ]
        )

    def test_create_bands_dict_data_from_prices(self):
        price_data = get_test_price_data()

        self.assertListEqual(self.bands.create_data_from_prices(
            price_data_df=price_data,
            length=105),
            [
                {'upperband': 35.35302638099354, 'time': 1496617200, 'lowerband': 18.564164095196958},
                {'upperband': 35.2722508483616, 'time': 1496631600, 'lowerband': 18.623860562240395},
                {'upperband': 35.226874519065156, 'time': 1496646000, 'lowerband': 18.615725355487747},
                {'upperband': 35.20458122661314, 'time': 1496660400, 'lowerband': 18.58325261257084},
                {'upperband': 35.181145611872665, 'time': 1496674800, 'lowerband': 18.554087588836147}
            ]
        )


if __name__ == '__main__':
    unittest.main()