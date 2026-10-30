"""Retained-input, numerical-policy and strict JSON contract checks for 17.9."""
from fractions import Fraction as F
import json
import math
from pathlib import Path
import subprocess
import sys
import section_17_09 as lab


def near(actual,expected):
    expected=float(expected)
    assert abs(actual-expected)<=4*math.ulp(expected),(actual,expected)


def check():
    financial_cases=(((0.75,0.25),(0.25,0.75),128.0,25.0),
                     ((0.5,0.5),(0.5,0.5),1e308,1e308),
                     ((1.0,0.0),(0.0,1.0),0.5,0.0),
                     ((0.25,0.75),(0.75,0.25),2**-20,2**10))
    fields=0
    for w,old,capital,bps in financial_cases:
        report=lab.financial_report(w,old,capital,bps)
        assert report['inputs']=={'target_weights':w,'current_weights':old,
                                  'capital':capital,'cost_bps':bps}
        assert report['weight_sum_tolerance']==1e-10
        assert report['expected_returns']==(0.08,0.05)
        assert report['return_period']=='annual'
        assert report['monetary_unit']=='same unspecified currency as capital'
        # Dyadic weight changes/capital make these selected trade products exact.
        trades=tuple(F(capital)*(F(a)-F(b)) for a,b in zip(w,old))
        gross=sum(abs(z) for z in trades)
        turnover=sum(abs(F(a)-F(b)) for a,b in zip(w,old))
        ret=F(w[0])*F(2,25)+F(w[1])*F(1,20)
        for actual,ref in zip(report['signed_trades'],trades):near(actual,ref);fields+=1
        for key,ref in (('gross_traded_notional',gross),('gross_turnover',turnover),
                        ('modeled_transaction_cost',gross*F(bps)/10000),('expected_return',ret)):
            near(report[key],ref);fields+=1
        loaded=json.loads(json.dumps(report,allow_nan=False,sort_keys=True))
        assert loaded['inputs']['target_weights']==list(w)
        assert loaded['inputs']['capital']==capital
    norms=('primal_violation','dual_violation','stationarity_norm','complementarity_norm')
    certs=0
    for tol in (0.0,1e-12,0.125):
        for w,lam,m in (((0.5,0.5),0.0,(0.0,0.0,0.0,0.0)),
                        ((0.0,1.0),-0.18,(0.0,0.0,0.16,0.0))):
            report=lab.verify_candidate(w,lam,m,(1.0,1.0),tol)
            assert report['inputs']=={'weights':w,'lambda':lam,'multipliers':m,'caps':(1.0,1.0)}
            assert report['tolerance']==tol
            assert report['tolerance_policy']=='single absolute threshold across all four residual norms'
            assert report['passes']==all(report[k]<=tol for k in norms)
            assert set(report['residual_units'])==set(norms)
            certs+=1
    result=lab.assessment()
    assert result['report_schema_version']==1
    model=result['model']
    assert model['covariance']==((0.04,0.01),(0.01,0.09))
    assert model['expected_returns']==(0.08,0.05)
    assert model['asset_order']==('asset_1','asset_2')
    assert model['data_provenance']=='synthetic fixed manuscript coefficients; no market data ingested'
    assert model['period']=='annual' and model['objective']=='minimum variance; return and transaction cost excluded'
    first=json.dumps(result,allow_nan=False,sort_keys=True,separators=(',',':'))
    second=json.dumps(lab.assessment(),allow_nan=False,sort_keys=True,separators=(',',':'))
    assert first==second
    parsed=json.loads(first)
    assert json.dumps(parsed,allow_nan=False,sort_keys=True,separators=(',',':'))==first
    outputs=[subprocess.run([sys.executable,'section_17_09.py'],cwd=Path(__file__).parent,
                           text=True,capture_output=True,timeout=15,check=True).stdout for _ in range(2)]
    assert outputs[0]==outputs[1] and json.loads(outputs[0])==parsed
    return {'financial_input_sets':len(financial_cases),'independent_financial_fields':fields,
            'certificate_policy_cases':certs,'separate_process_outputs':len(outputs),
            'canonical_json_roundtrip':True,'scope':'selected fixed synthetic model; no external data validation'}


if __name__=='__main__':
    print(json.dumps(check(),sort_keys=True,allow_nan=False))
