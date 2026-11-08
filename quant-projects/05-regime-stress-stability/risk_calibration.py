"""Leakage-safe ex-post forecast-versus-realized risk diagnostics for Project 05."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

WEEKS_PER_YEAR = 52

def calibrate(frame: pd.DataFrame, horizon: int = 13) -> pd.DataFrame:
    """Score forecast at t against realized weekly volatility over t..t+horizon-1.

    Forward overlapping windows are correlated; they are NOT independent samples.
    Trailing incomplete windows are omitted, never padded.
    """
    required = {"Date", "Scenario", "GrossReturn", "ForecastAnnualVol"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing columns: {sorted(required-set(frame.columns))}")
    if not isinstance(horizon, int) or horizon < 2:
        raise ValueError("horizon must be an integer >= 2")
    output = []
    for scenario, group in frame.groupby("Scenario", sort=True):
        group = group.sort_values("Date")
        dates = pd.to_datetime(group.Date, errors="raise")
        if dates.duplicated().any() or not dates.is_monotonic_increasing:
            raise ValueError("Dates must be strictly increasing per scenario")
        returns = pd.to_numeric(group.GrossReturn, errors="raise").to_numpy(dtype=float)
        forecasts = pd.to_numeric(group.ForecastAnnualVol, errors="raise").to_numpy(dtype=float)
        if (not np.isfinite(returns).all() or not np.isfinite(forecasts).all()
                or (returns <= -1).any() or (forecasts < 0).any()):
            raise ValueError("Returns must be finite and > -100%; forecasts finite and >= 0")
        if len(group) < horizon:
            continue
        for start in range(len(group)-horizon+1):
            realized = float(np.std(returns[start:start+horizon], ddof=1)*np.sqrt(WEEKS_PER_YEAR))
            predicted = float(forecasts[start])
            output.append({"Scenario": scenario, "ForecastDate": dates.iloc[start].date().isoformat(),
                           "RealizedThrough": dates.iloc[start+horizon-1].date().isoformat(),
                           "HorizonWeeks": horizon, "ForecastAnnualVol": predicted,
                           "ForwardRealizedAnnualVol": realized,
                           "ForecastError": predicted-realized,
                           "AbsoluteError": abs(predicted-realized),
                           "SquaredError": (predicted-realized)**2})
    return pd.DataFrame(output, columns=["Scenario", "ForecastDate", "RealizedThrough",
          "HorizonWeeks", "ForecastAnnualVol", "ForwardRealizedAnnualVol",
          "ForecastError", "AbsoluteError", "SquaredError"])

def summarize_calibration(calibration: pd.DataFrame) -> pd.DataFrame:
    """Scenario-wise bias, MAE and RMSE in annual-volatility fraction units."""
    if calibration.empty:
        raise ValueError("No complete forward windows; choose shorter horizon")
    rows=[]
    for scenario, group in calibration.groupby("Scenario", sort=True):
        rows.append({"Scenario":scenario, "CompleteWindows":len(group),
                     "MeanForecastVol":float(group.ForecastAnnualVol.mean()),
                     "MeanRealizedVol":float(group.ForwardRealizedAnnualVol.mean()),
                     "Bias":float(group.ForecastError.mean()),
                     "MAE":float(group.AbsoluteError.mean()),
                     "RMSE":float(np.sqrt(group.SquaredError.mean()))})
    return pd.DataFrame(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weekly", type=Path, default=Path(__file__).parent/"reports"/"weekly_results.csv")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent/"reports")
    parser.add_argument("--horizon", type=int, default=13)
    args=parser.parse_args()
    frame=pd.read_csv(args.weekly)
    detail=calibrate(frame,args.horizon)
    summary=summarize_calibration(detail)
    args.output.mkdir(parents=True,exist_ok=True)
    detail.to_csv(args.output/"risk_calibration_windows.csv",index=False)
    summary.to_csv(args.output/"risk_calibration_summary.csv",index=False)
    print(summary.round(5).to_string(index=False))
    print("Overlapping forward windows: descriptive only; not independent confidence intervals.")

if __name__=="__main__": main()
