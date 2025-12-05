# data_loader.py  reads in a CSV file, calculates variance over windows, and saves to parquet
# reads prices from a column called "Price"
import yfinance as yf
import pandas as pd
import numpy as np
from pathlib import Path

HORIZONS = 5*(np.arange(26)+1)   # does 1 to 26 weeks, can also do [5, 10, 20, 40, 80, 160]

all_data = []
TICKERS = ["Model"]
for ticker in TICKERS:
    df = pd.read_csv("variance_timeseries.csv")
    price = df["Price"]
    
    ret = np.log(price).diff().dropna().values

    rows = []
    scale = np.sqrt(252)

    for T in HORIZONS:
        i = 0
        while i + T <= len(ret):
            window = ret[i:i+T]     # T points
            if len(window) < T * 0.8:
                break

            x = window.sum()   # total price change over the period
            sigma = np.std(window, ddof=0) * scale  # use np.std to get std over period, ddof=1 means divisor is N-1
            z_raw = x / np.sqrt(T / 252.0)

            # REJECT BAD WINDOWS
            if not (np.isfinite(sigma) and sigma > 0 and np.isfinite(z_raw)):
                i += T
                continue

            rows.append({          # append row of data for this period
                "ticker": ticker,
                "date": price.index[i + T - 1],   # row number
                "T": T,
                "z_raw": float(z_raw),
                "sigma": float(sigma)
            })
            i += T

    if not rows:
        print(" [no data]")
        continue

    df = pd.DataFrame(rows)

    # CLEAN BEFORE DE-MEANING 
    df = df[np.isfinite(df['z_raw']) & np.isfinite(df['sigma']) & (df['sigma'] > 0)]

    # NOW de-mean safely, this step groups by ticker and T, and subtracts the group mean 
    df["z"] = df.groupby(["ticker", "T"])["z_raw"].transform(lambda g: g - g.mean())

    df = df.drop(columns="z_raw")
    df = df.dropna().reset_index(drop=True)  # Final clean

    print(f" → {len(df)} clean windows")
    all_data.append(df)

full = pd.concat(all_data, ignore_index=True)


n = len(full) // 3

# Save to file
full.to_parquet("dataset.parquet", compression=None)
print("Done! 1 file created")
