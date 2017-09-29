def get_test_price_data():
    import os
    import pandas as pd

    file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'xem_jpy_4h_1495119600_1496674800.csv')
    df = pd.read_csv(file)
    return df
