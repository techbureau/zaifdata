import unittest
import zaifdata.data.prices as zdp
import pandas as pd
from pandas.util.testing import assert_frame_equal
import csv
import os
from decimal import Decimal


# fixme: cleaner code!
class TestPrices(unittest.TestCase):
    def test_price_dict(self):
        currency_pair = 'xem_jpy'
        period = '4h'
        start = 1495119600
        end = 1496674800

        data_from_web = zdp.DataReader(currency_pair, period, start, end)
        file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'data/xem_jpy_4h_1495119600_1496674800.csv')
        web = {
            'time': 0,
            'volume': 0,
            'average': 0,
            'open': 0,
            'high': 0,
            'low': 0,
            'close': 0,
        }
        for row in data_from_web:
            web['time'] += Decimal(row['time'])
            web['volume'] += Decimal(row['volume'])
            web['average'] += Decimal(row['average'])
            web['open'] += Decimal(row['open'])
            web['high'] += Decimal(row['high'])
            web['low'] += Decimal(row['low'])
            web['close'] += Decimal(row['close'])

        data_from_csv = {
            'time': 0,
            'volume': 0,
            'average': 0,
            'open': 0,
            'high': 0,
            'low': 0,
            'close': 0,
        }
        with open(file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_from_csv['time'] += Decimal(row['time'])
                data_from_csv['volume'] += Decimal(row['volume'])
                data_from_csv['average'] += Decimal(row['average'])
                data_from_csv['open'] += Decimal(row['open'])
                data_from_csv['high'] += Decimal(row['high'])
                data_from_csv['low'] += Decimal(row['low'])
                data_from_csv['close'] += Decimal(row['close'])

        self.assertDictEqual(web, data_from_csv)

    def test_price_df(self):
        currency_pair = 'xem_jpy'
        period = '4h'
        start = 1495119600
        end = 1496674800

        df_from_web = zdp.DataReader(currency_pair, period, start, end, style='df')
        file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'data/xem_jpy_4h_1495119600_1496674800.csv')
        df_from_csv = pd.read_csv(file)

        # pandas compare dataframes only when columns are same order
        df_from_web.sort_index(axis=1, inplace=True)
        df_from_csv.sort_index(axis=1, inplace=True)

        assert_frame_equal(df_from_web, df_from_csv)


if __name__ == '__main__':
    unittest.main()
