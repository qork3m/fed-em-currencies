import pandas as pd
import os
import sqlite3
from functions import getting_currency_series, getting_dates
import matplotlib.pyplot as plt

folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder, "fed_em_currencies.db")
connection = sqlite3.connect(db_path)

try:
    print("Trying to fetch the data from database")
    df_currencies = pd.read_sql("SELECT * FROM currency_df", connection)
    df_dates = pd.read_sql("SELECT * FROM dates_df", connection)
    print("Successful")
except Exception:
    print("Run the file named 'fetch_data.py' to create a database.")
    exit()

df_dates_hike = getting_dates(df_dates, "hike")
df_dates_cut = getting_dates(df_dates, "cut")

df_brl = getting_currency_series("USDBRL=X", df_currencies)
df_zar = getting_currency_series("USDZAR=X", df_currencies)
df_inr = getting_currency_series("USDINR=X", df_currencies)
df_mxn = getting_currency_series("USDMXN=X", df_currencies)


series_list = [df_brl, df_zar, df_inr, df_mxn]
labels = ["BRL", "ZAR", "INR", "MXN"]

fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(14, 12), sharex=True)

for ax, series, label in zip(axes, series_list, labels):
    ax.plot(series.index, series.values, color="black", linewidth=1)

    for date in df_dates_hike:
        ax.axvline(x=date, color="green", linestyle="--",
                   linewidth=1, alpha=0.5)

    for date in df_dates_cut:
        ax.axvline(x=date, color="red", linestyle="--", linewidth=1, alpha=0.5)

    ax.set_title(f"USD/{label}", fontsize=11, fontweight="bold", loc="left")
    ax.set_ylabel("Rate")

fig.suptitle("EM Currencies vs USD Around Fed Rate Decisions (green = hike, red = cut)",
             fontsize=14, fontweight="bold")

plt.tight_layout()
plt.savefig(os.path.join(folder, "em_currencies.png"),
            dpi=150, bbox_inches="tight")
plt.show()
