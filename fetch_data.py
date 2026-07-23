import pandas as pd
from dotenv import load_dotenv
import os
from fredapi import Fred
import yfinance as yf
import sqlite3

load_dotenv()
api_key = os.getenv("FRED_API_KEY")

folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder, "fed_em_currencies.db")
connection = sqlite3.connect(db_path)

fred = Fred(api_key=api_key)
data = fred.get_series(
    'DFEDTARU', observation_start="2008-01-01", observation_end="2026-07-23")

diff = data.diff()

diff_pos = diff[(diff > 0) & (diff.isna() == False)]
diff_neg = diff[(diff < 0) & (diff.isna() == False)]

diff_pos_dates = diff_pos.index
diff_neg_dates = diff_neg.index

diff_pos_dates_minus_one = diff_pos_dates - pd.Timedelta(days=1)
diff_neg_dates_minus_one = diff_neg_dates - pd.Timedelta(days=1)

dates_pos_df = pd.DataFrame(diff_pos_dates_minus_one)

dates_pos_df.rename(columns={0: "Dates"}, inplace=True)
dates_pos_df["direction"] = "hike"
dates_neg_df = pd.DataFrame(diff_neg_dates_minus_one)
dates_neg_df.rename(columns={0: "Dates"}, inplace=True)
dates_neg_df["direction"] = "cut"

dates_df_list = [dates_pos_df, dates_neg_df]
dates_merged_df = pd.concat(dates_df_list).reset_index(drop=True)

tickers_list = ["USDBRL=X", "USDZAR=X", "USDINR=X", "USDMXN=X"]
df_list = []

for ticker in tickers_list:
    df = yf.download(ticker, start="2008-01-01", end="2026-07-23")
    df = df["Close"].squeeze().reset_index()
    df["Date"] = pd.to_datetime(df["Date"])
    df.rename(columns={ticker: "currency_price"}, inplace=True)
    df["Currency"] = ticker
    df_list.append(df)

df_merged = pd.concat(df_list)

df_dxy = yf.download("DX-Y.NYB", start="2008-01-01", end="2026-07-23")
df_dxy = df_dxy["Close"].squeeze().reset_index()
df_dxy["Date"] = pd.to_datetime(df_dxy["Date"])
df_dxy.rename(columns={"DX-Y.NYB": "DXY"}, inplace=True)

dates_merged_df.to_sql("dates_df", connection,
                       if_exists="replace", index=False)
df_merged.to_sql("currency_df", connection, if_exists="replace", index=False)
df_dxy.to_sql("dxy_df", connection, if_exists="replace", index=False)
