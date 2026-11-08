"""Refresh five-stock adjusted-close weekly data via yfinance (network needed)."""
import argparse
from datetime import date, timedelta
from pathlib import Path
import pandas as pd
from backtest import TICKERS, read_prices

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--start",default="2019-01-01")
 parser.add_argument("--end",default=(date.today()+timedelta(days=1)).isoformat())
 parser.add_argument("--output",default="weekly_adjusted_prices.csv")
 args=parser.parse_args()
 try:
  import yfinance as yf
 except ImportError as exc:
  raise SystemExit("Install optional dependency: py -m pip install yfinance") from exc
 raw=yf.download(TICKERS,start=args.start,end=args.end,interval="1d",
                 auto_adjust=True,progress=False,threads=False)
 if raw.empty or not isinstance(raw.columns,pd.MultiIndex):
  raise RuntimeError("Missing or unexpected downloaded price data")
 close=raw["Close"].reindex(columns=TICKERS)
 if close.isna().any().any():
  raise ValueError("Missing adjusted closes: investigate before continuing")
 weekly=close.groupby(pd.Grouper(freq="W-FRI")).tail(1)
 if weekly.index[-1].dayofweek!=4: weekly=weekly.iloc[:-1]
 if len(weekly)<60: raise ValueError("Insufficient weekly observations")
 weekly.index.name="Date"
 weekly.to_csv(args.output,float_format="%.6f")
 read_prices(Path(args.output))
 print(f"Saved {len(weekly)} weekly observations to {args.output}")

if __name__=="__main__": main()
