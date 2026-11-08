import numpy as np
import pandas as pd
import pytest
from risk_calibration import calibrate, summarize_calibration

def fixture(n=20):
    return pd.DataFrame({"Date":pd.date_range("2020-01-03",periods=n,freq="W-FRI"),
                         "Scenario":["base"]*n,
                         "GrossReturn":np.tile([.01,-.01],n//2),
                         "ForecastAnnualVol":[.1]*n})

def test_forward_windows_and_manual_variance():
    c=calibrate(fixture(),4)
    assert len(c)==17
    assert c.iloc[0].ForecastDate=="2020-01-03"
    assert c.iloc[0].RealizedThrough=="2020-01-24"
    assert np.isclose(c.iloc[0].ForwardRealizedAnnualVol,np.std([.01,-.01,.01,-.01],ddof=1)*np.sqrt(52))

def test_future_changes_do_not_change_earlier_complete_windows():
    p=fixture()
    before=calibrate(p.iloc[:12],4)
    p.loc[12:,"GrossReturn"]=-.2
    after=calibrate(p,4)
    pd.testing.assert_frame_equal(before,after.iloc[:len(before)].reset_index(drop=True))

def test_incomplete_tail_is_excluded():
    assert len(calibrate(fixture(),13))==8
    assert calibrate(fixture(4),5).empty

def test_summary_math():
    c=calibrate(fixture(),4)
    summary=summarize_calibration(c)
    assert summary.iloc[0].CompleteWindows==17
    assert np.isclose(summary.iloc[0].RMSE,np.sqrt(np.mean(c.ForecastError**2)))
    assert summary.iloc[0].RMSE>=summary.iloc[0].MAE

def test_invalid_inputs():
    p=fixture()
    with pytest.raises(ValueError): calibrate(p,1)
    with pytest.raises(ValueError): calibrate(p.drop(columns=["Scenario"]))
    p.loc[0,"ForecastAnnualVol"]=-1
    with pytest.raises(ValueError): calibrate(p)
    with pytest.raises(ValueError): summarize_calibration(pd.DataFrame())

def test_scenario_isolation():
    p=fixture(20)
    q=p.copy();q["Scenario"]="stress";q["ForecastAnnualVol"]=.3
    c=calibrate(pd.concat([p,q],ignore_index=True),4)
    s=summarize_calibration(c)
    assert len(s)==2 and set(s.Scenario)=={"base","stress"}
    assert s.loc[s.Scenario=="stress","MeanForecastVol"].iloc[0]==.3
