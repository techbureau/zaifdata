from .base import HistoricalPrices


def DataReader(currency_pair, period, start, end, style='dict'):
    return HistoricalPrices(currency_pair, period).read(start, end).to_any_style(style)


def get_data_by_count(currency_pair, period, count, style='dict'):
    return HistoricalPrices(currency_pair, period).read_by_count(count).to_any_style(style)
