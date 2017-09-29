import unittest
from zaifdata.data.base import HistoricalPrices
from unittest.mock import MagicMock
import pandas as pd
from io import StringIO
from pandas.util.testing import assert_frame_equal


PRICE_DATA = [
    {
        'volume': '4253.614',
        'average': '420927.53250048',
        'high': '437255.0',
        'low': '411310.0',
        'time': '1506265200',
        'close': '433610.0',
        'open': '414130.0'
    },
    {
        'volume': '6671.8122',
        'average': '434898.60618978',
        'high': '441000.0',
        'low': '428100.0',
        'time': '1506351600',
        'close': '434325.0',
        'open': '433500.0'
     },
    {
        'volume': '6259.7373',
        'average': '438888.76842683',
        'high': '453980.0', 'low': '429435.0',
        'time': '1506438000',
        'close': '449385.0',
        'open': '434320.0'
     },
    {
        'volume': '7957.6315',
        'average': '465605.5389669',
        'high': '490000.0',
        'low': '446505.0',
        'time': '1506524400',
        'close': '463995.0',
        'open': '449390.0'
    },
    {
        'volume': '5922.9558',
        'average': '462400.35321013',
        'high': '468700.0',
        'low': '447665.0',
        'time': '1506610800',
        'close': '450020.0',
        'open': '463955.0'
    }
]

PRICE_DATA_DF = StringIO("""average,close,high,low,open,time,volume
420927.532500,433610.0,437255.0,411310.0,414130.0,1506265200,4253.6140
434898.606190,434325.0,441000.0,428100.0,433500.0,1506351600,6671.8122
438888.768427,449385.0,453980.0,429435.0,434320.0,1506438000,6259.7373
465605.538967,463995.0,490000.0,446505.0,449390.0,1506524400,7957.6315
462400.353210,450020.0,468700.0,447665.0,463955.0,1506610800,5922.9558
""")


class TestHistoricalPrices(unittest.TestCase):

    def setUp(self):
        self.historical_prices = HistoricalPrices(currency_pair='test_jpy',
                                                  period='test')

    def test_read(self):
        history_mock = MagicMock()
        self.historical_prices.data_source.history = history_mock
        self.historical_prices.read(from_=0,
                                    to_=100)

        history_mock.assert_called_once_with(
            currency_pair='test_jpy',
            period='test',
            from_sec=0,
            to_sec=100
        )

    def test_read_by_count(self):
        history_mock = MagicMock(return_value=PRICE_DATA)
        self.historical_prices.data_source.history = history_mock
        self.historical_prices._calc_from_sec = MagicMock(return_value=0)  # return_value is irrelevant to test
        self.historical_prices.read_by_count(count=1)

        self.assertListEqual(
            self.historical_prices.data,
            [{
                'volume': '5922.9558',
                'average': '462400.35321013',
                'high': '468700.0',
                'low': '447665.0',
                'time': '1506610800',
                'close': '450020.0',
                'open': '463955.0'
                }]
        )

    def test_to_df(self):
        self.historical_prices.data = PRICE_DATA
        price_df = self.historical_prices.to_df()
        self.assertIsInstance(price_df, pd.DataFrame)

        try:
            expected = pd.read_csv(PRICE_DATA_DF, sep=',')
            assert_frame_equal(price_df, expected)
        except pd.errors.EmptyDataError:
            pass

    def to_dict(self):
        self.historical_prices.data = PRICE_DATA
        self.assertListEqual(self.historical_prices.to_dict(), PRICE_DATA)

    def test_count(self):
        self.historical_prices.data = PRICE_DATA
        self.assertEqual(self.historical_prices.count(), 5)

    def test_to_any_style(self):

        self.historical_prices.to_df = MagicMock(return_value='df')
        self.historical_prices.to_dict = MagicMock(return_value='dict')

        styles = ('dict', 'df', 'wrong_style')

        for style in styles:
            with self.subTest(style=style):
                if style in ('dict', 'df'):
                    self.assertEqual(self.historical_prices.to_any_style(style), style)
                self.assertRaises(ValueError)

if __name__ == '__main__':
    unittest.main()
