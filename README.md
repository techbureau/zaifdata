# zaifdata

:blue_book: Data Reader for zaif Exchange


## Features

* Support all currency_pairs in Zaif Exchange
* Able to calc technical indicators
* Fetch data both by `count` and `datetime`

## Installation

```python
$ pip install zaifdata
```

If you want use technical indicators,  
run the command below after installation

```bash
install_talib
```

This repo internally use ta_lib to calculate technicals

## How to use

### Get historical prices

```python
from zaifdata.data.prices import DataReader, get_data_by_count
import time

now = int(time.time()) # use 'int' value
yesterday = now - 86400


DataReader(currency_pair='xem_jpy', period='8h', start=yesterday, end=now)
"""
[
    {'low': '24.4001', 'close': '24.45', 'time': '1506265200', 'open': '24.7', 'high': '24.85', 'average': '24.59263445', 'volume': '560982.5'}, 
    {'low': '24.3', 'close': '24.89', 'time': '1506294000', 'open': '24.45', 'high': '24.9', 'average': '24.69664484', 'volume': '1062381.8'},
    {'low': '24.8', 'close': '24.8', 'time': '1506322800', 'open': '24.8103', 'high': '24.9', 'average': '24.84771633', 'volume': '144757.2'}
 ]
"""

# you can specify 'style' to select format of return values ('dict' or 'df')

DataReader(currency_pair='xem_jpy', period='8h', start=yesterday, end=now, style='df')

"""
     average    close   high      low     open        time     volume
0  24.592634  24.4500  24.85  24.4001  24.7000  1506265200   560982.5
1  24.696645  24.8900  24.90  24.3000  24.4500  1506294000  1062381.8
2  24.846116  24.8989  24.90  24.8000  24.8103  1506322800   149786.0
"""
```

Or you can use `get_data_by_count` method if you want to specify the number of values


```python
from zaifdata.data.prices import get_data_by_count

get_data_by_count(currency_pair='btc_jpy', period='30m', count=2)

"""
[
    {'volume': '134.9155', 'low': '421450.0', 'high': '423000.0', 'average': '422022.55839766', 'close': '422275.0', 'open': '421710.0', 'time': '1506322800'},
    {'volume': '14.548', 'low': '422025.0', 'high': '422975.0', 'average': '422504.70470168', 'close': '422390.0', 'open': '422170.0', 'time': '1506324600'}
]
"""
```

### Get technical indicators

```python
from zaifdata.indicators import EMA, SMA, BBANDS, RSI, MACD, ADX
import time

now = int(time.time()) 
ema = EMA(currency_pair='btc_jpy', period='1h')
ema.request_data(count=3, style='df')


"""
         time            ema
0  1506315600  415684.200000
1  1506319200  416148.876923
2  1506322800  416680.501775
"""
```

Available (`EMA`, `SMA`, `BBANDS`, `RSI`, `MACD`, `ADX`)