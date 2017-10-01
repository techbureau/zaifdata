import unittest
from unittest.mock import MagicMock, patch
from .indicator_base import IndicatorTestMixIn
from zaifdata.indicators.moving_average import EMA, SMA
from tests.test_data.get_test_data import get_test_price_data
from pandas.util.testing import assert_frame_equal
import pandas as pd


class TestMA(unittest.TestCase, IndicatorTestMixIn):
    @classmethod
    def setUpClass(cls):
        cls.ema = EMA
        cls.sma = SMA

    def test_name(self):
        ema_name = self.ema.NAME
        sma_name = self.sma.NAME
        self.assertEqual((ema_name, sma_name), ('ema', 'sma'))

    def test_request_data(self):
        ema = self.ema(currency_pair='test_jpy', period='1m', length=12)
        sma = self.sma(currency_pair='test_jpy', period='1m', length=12)

        for ma in [ema, sma]:
            with self.subTest(ma=ma):
                ma.create_data_from_prices = MagicMock()
                with patch('zaifdata.indicators.moving_average.get_data_by_count',
                           return_value='price_data') as mock_get_data:
                    ma.request_data(count=100, style='dict')
                    mock_get_data.assert_called_once_with(currency_pair='test_jpy',
                                                          period='1m',
                                                          count=111,
                                                          style='df')

                    ma.create_data_from_prices.assert_called_once_with('price_data', 12, 'dict')

    def test_request_data_by_period(self):
        ema = self.ema(currency_pair='test_jpy', period='1m', length=12)
        sma = self.sma(currency_pair='test_jpy', period='1m', length=12)

        for ma in [ema, sma]:
            with self.subTest(ma=ma):
                ma.create_data_from_prices = MagicMock()
                with patch('zaifdata.indicators.moving_average.DataReader',
                           return_value='price_data') as mock_get_data:
                    ma.request_data_by_period(start=0, end=100, style='dict')

                    mock_get_data.assert_called_once_with(currency_pair='test_jpy',
                                                          period='1m',
                                                          start=0,
                                                          end=100,
                                                          style='df')
                    ma.create_data_from_prices.assert_called_once_with('price_data', 12, 'dict')

    def test_create_ema_dict_data_from_prices(self):
        price_data = get_test_price_data()
        self.assertListEqual(self.ema.create_data_from_prices(
            price_data=price_data,
            length=100,
            style='dict'),
            [
                {'time': 1496545200, 'ema': 27.08150000000001},
                {'time': 1496559600, 'ema': 27.027414851485158},
                {'time': 1496574000, 'ema': 26.97835713165377},
                {'time': 1496588400, 'ema': 26.931260950828943},
                {'time': 1496602800, 'ema': 26.879356773584806},
                {'time': 1496617200, 'ema': 26.836046738464315},
                {'time': 1496631600, 'ema': 26.827412149583832},
                {'time': 1496646000, 'ema': 26.801720819889102},
                {'time': 1496660400, 'ema': 26.775350110584366},
                {'time': 1496674800, 'ema': 26.75009565294903},
             ]
        )

    def test_create_ema_df_data_from_prices(self):
        price_data = get_test_price_data()
        ema_from_test_data = self.ema.create_data_from_prices(price_data=price_data,
                                                              length=100,
                                                              style='df')
        ema_from_expected = pd.DataFrame(
                [
                    {'time': 1496545200, 'ema': 27.08150000000001},
                    {'time': 1496559600, 'ema': 27.027414851485158},
                    {'time': 1496574000, 'ema': 26.97835713165377},
                    {'time': 1496588400, 'ema': 26.931260950828943},
                    {'time': 1496602800, 'ema': 26.879356773584806},
                    {'time': 1496617200, 'ema': 26.836046738464315},
                    {'time': 1496631600, 'ema': 26.827412149583832},
                    {'time': 1496646000, 'ema': 26.801720819889102},
                    {'time': 1496660400, 'ema': 26.775350110584366},
                    {'time': 1496674800, 'ema': 26.75009565294903},
                ]
            )
        ema_from_test_data.sort_index(axis=1, inplace=True)
        ema_from_expected.sort_index(axis=1, inplace=True)

        assert_frame_equal(ema_from_test_data, ema_from_expected)

    def test_create_sma_dict_data_from_prices(self):
        price_data = get_test_price_data()
        self.assertListEqual(self.sma.create_data_from_prices(
            price_data=price_data,
            length=100,
            style='dict'),
            [
                {'time': 1496545200, 'sma': 27.08150000000001},
                {'time': 1496559600, 'sma': 27.111002000000006},
                {'time': 1496574000, 'sma': 27.11850100000001},
                {'time': 1496588400, 'sma': 27.09850100000001},
                {'time': 1496602800, 'sma': 27.06160200000001},
                {'time': 1496617200, 'sma': 27.003524000000013},
                {'time': 1496631600, 'sma': 26.98452400000001},
                {'time': 1496646000, 'sma': 26.961724000000014},
                {'time': 1496660400, 'sma': 26.950924000000008},
                {'time': 1496674800, 'sma': 26.94592400000001}
            ]
        )

    def test_create_sma_df_data_from_prices(self):
        price_data = get_test_price_data()

        sma_from_test_data = self.sma.create_data_from_prices(price_data=price_data,
                                                              length=100,
                                                              style='df')
        sma_from_expected = pd.DataFrame(
                [
                    {'time': 1496545200, 'sma': 27.08150000000001},
                    {'time': 1496559600, 'sma': 27.111002000000006},
                    {'time': 1496574000, 'sma': 27.11850100000001},
                    {'time': 1496588400, 'sma': 27.09850100000001},
                    {'time': 1496602800, 'sma': 27.06160200000001},
                    {'time': 1496617200, 'sma': 27.003524000000013},
                    {'time': 1496631600, 'sma': 26.98452400000001},
                    {'time': 1496646000, 'sma': 26.961724000000014},
                    {'time': 1496660400, 'sma': 26.950924000000008},
                    {'time': 1496674800, 'sma': 26.94592400000001}
                ]
            )

        sma_from_test_data.sort_index(axis=1, inplace=True)
        sma_from_expected.sort_index(axis=1, inplace=True)

        assert_frame_equal(sma_from_test_data, sma_from_expected)

if __name__ == '__main__':
    unittest.main()
