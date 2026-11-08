# Data policy — Project 04

The historical backtesting exercise previously used weekly adjusted prices for AAPL, JNJ, JPM, PG, NEE, from 2019-01-04 through 2026-05-29, sampled from [this public dataset](https://github.com/S-Gijbile-19/AlphaPulse-Investment-Risk-Monitor/blob/main/data/clean/master_prices.csv).

That public repository does **not** provide a recognized license granting redistribution of the stock price snapshot. Therefore the full CSV is deliberately **not** republished here.

To execute an independent new historical backtest, run `py -m pip install yfinance`, `py download_prices.py`, and then `py backtest.py`. Data vendors may adjust historic values, and refreshed results will differ from the reference output and dates.

The included `historical_risk_validation_report.csv` is a **dated reference result** from the earlier study, not a claim that the missing upstream data is bundled or that the results cover November 2026.

Do not redistribute live market-provider data without checking its terms and provenance.
