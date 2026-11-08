import numpy as np
import pandas as pd
import pytest
from tail_risk import rolling_risk, breach_summary, synthetic_returns

def test_reproducible_and_training_is_past_only():
    data = synthetic_returns(90)
    a = rolling_risk(data, lookback=52, bootstrap=100)
    b = rolling_risk(data, lookback=52, bootstrap=100)
    pd.testing.assert_frame_equal(a, b)
    assert len(a) == 38
    assert (a.TrainingEndDate < a.Date).all()

def test_no_future_leakage():
    data = synthetic_returns(100)
    a = rolling_risk(data.iloc[:80], bootstrap=100)
    modified = data.copy()
    modified.loc[80:, 'Return'] = -0.40
    b = rolling_risk(modified, bootstrap=100)
    pd.testing.assert_frame_equal(a, b.iloc[:len(a)].reset_index(drop=True))

def test_known_historical_var_and_cvar():
    data = pd.DataFrame({'Date': pd.date_range('2020-01-03', periods=21, freq='W-FRI'),
                         'Return': np.r_[np.linspace(-.2, .2, 20), -.3]})
    scored = rolling_risk(data, lookback=20, bootstrap=100)
    expected = -np.quantile(data.Return.iloc[:20], .05)
    assert np.isclose(scored.HistoricalVaR95.iloc[0], expected)
    assert np.isclose(scored.HistoricalCVaR95.iloc[0], .2)
    assert scored.HistoricalBreach.iloc[0] == 1

def test_breach_summary():
    scored = rolling_risk(synthetic_returns(90), bootstrap=100)
    s = breach_summary(scored)
    assert len(s) == 2
    assert ((s.BinomialPValue >= 0) & (s.BinomialPValue <= 1)).all()

@pytest.mark.parametrize('data', [pd.DataFrame({'Date': ['2020-01-01']*60, 'Return': [.01]*60}),
                                  pd.DataFrame({'Date': pd.date_range('2020-01-03', periods=60, freq='W-FRI'), 'Return': [-1.0]*60})])
def test_invalid_data_rejected(data):
    with pytest.raises(ValueError):
        rolling_risk(data, bootstrap=100)

def test_short_history_rejected():
    with pytest.raises(ValueError):
        rolling_risk(synthetic_returns(60), lookback=60, bootstrap=100)
