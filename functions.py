import pandas as pd


def getting_currency_series(ticker, df):
    filtered = df[df["Currency"] == ticker]
    filtered["Date"] = pd.to_datetime(filtered["Date"])
    filtered.set_index("Date", inplace=True)
    return filtered["currency_price"]


def getting_dates(df, direction):
    filtered = df[df["direction"] == direction]
    filtered["Dates"] = pd.to_datetime(filtered["Dates"])
    return filtered["Dates"]


def get_window_returns(dates, currency):
    currency_return = currency.pct_change().dropna()
    window_totals = []

    for date in dates:
        pos = currency_return.index.get_indexer([date], method="nearest")[0]
        window = currency_return.iloc[pos: pos + 4]
        window_totals.append(window.sum())
    return window_totals
