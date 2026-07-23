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
