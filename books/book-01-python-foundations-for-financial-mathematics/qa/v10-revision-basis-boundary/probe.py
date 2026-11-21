"""Native price eligibility versus supplemental revision/basis/freshness context."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
from fractions import Fraction as F
import financial_toolkit.validation as validation
import json,sys,math,hashlib,platform
rows=[];observations=[]
def ck(name,actual,want):
 ok=actual==want if isinstance(want,(str,bool)) else math.isclose(float(actual),float(want),rel_tol=5e-13,abs_tol=0);rows.append(dict(name=name,actual=actual,expected=str(want),passed=ok))
def rejected(name,fn):
 try:fn();actual='returned'
 except Exception as e:actual=type(e).__name__
 ck(name,actual,'ValueError')
assert Path(validation.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
t0=datetime(2026,1,1,tzinfo=timezone.utc);t1=t0+timedelta(days=1);old_cutoff=t0+timedelta(days=2);new_cutoff=t0+timedelta(days=4)
def record(price,event,available=None):return dict(instrument='XYZ',currency='USD',price=price,observed_at=event,available_at=event if available is None else available,source='fictional-source')
first=record(100.,t0);v1=record(125.,t1);v2=record(150.,t1,t0+timedelta(days=3))
ck('v1 eligible by old cutoff',validation.validated_price_return(first,v1,old_cutoff),F(1,4))
rejected('later revision unavailable at old cutoff',lambda:validation.validated_price_return(first,v2,old_cutoff))
ck('older version remains natively eligible at new cutoff',validation.validated_price_return(first,v1,new_cutoff),F(1,4))
ck('newer version eligible at new cutoff',validation.validated_price_return(first,v2,new_cutoff),F(1,2))
versions=[dict(version='v1',basis='raw',record=v1),dict(version='v2',basis='raw',record=v2)]
# Supplemental explicitly chosen fixture policy, not a native revision-selection API.
def latest_available(cutoff):return max((x for x in versions if x['record']['available_at']<=cutoff),key=lambda x:x['record']['available_at'])
ck('caller latest-at-old version',latest_available(old_cutoff)['version'],'v1')
ck('caller latest-at-new version',latest_available(new_cutoff)['version'],'v2')
ck('caller-selected old return',validation.validated_price_return(first,latest_available(old_cutoff)['record'],old_cutoff),F(1,4))
ck('caller-selected new return',validation.validated_price_return(first,latest_available(new_cutoff)['record'],new_cutoff),F(1,2))
extra=v1.copy();extra['revision_id']='v1';rejected('native schema rejects revision key',lambda:validation.validate_price_record(extra,old_cutoff))
# Supplied availability is not authenticated by structural validation.
backdated=v2.copy();backdated['available_at']=t1
ck('backdated supplied metadata passes structural rules',validation.validated_price_return(first,backdated,old_cutoff),F(1,2))
raw_second=record(125.,t1);adjusted_second=record(62.5,t1);adjusted_first=record(50.,t0)
ck('raw/raw fictional return',validation.validated_price_return(first,raw_second,old_cutoff),F(1,4))
ck('mixed basis still natively eligible',validation.validated_price_return(first,adjusted_second,old_cutoff),F(-3,8))
ck('consistent adjusted basis fictional return',validation.validated_price_return(adjusted_first,adjusted_second,old_cutoff),F(1,4))
extra=v1.copy();extra['price_basis']='adjusted';rejected('native schema rejects basis key',lambda:validation.validate_price_record(extra,old_cutoff))
stale0=record(100.,datetime(2000,1,1,tzinfo=timezone.utc));stale1=record(125.,datetime(2000,1,2,tzinfo=timezone.utc))
ck('very old pair still natively eligible',validation.validated_price_return(stale0,stale1,old_cutoff),F(1,4))
ck('caller one-day freshness would reject stale observation',old_cutoff-stale1['observed_at']>timedelta(days=1),True)
observations=[dict(scope='Supplemental fixture policy',statement='latest_available selects maximum supplied availability among eligible fixture versions; not a native revision-history/authentication implementation or accepted real-source policy.'),dict(scope='Native schema limit',statement='Multiple versions can individually pass. A caller must retain version/adjustment provenance externally; added keys are rejected by the exact native schema.'),dict(scope='Conceptual supplied-metadata limit',statement='Backdating a fictional supplied availability field can pass schema/time rules. The validator cannot authenticate real source publication/revision times.'),dict(scope='Fictional split/basis example',statement='The two-for-one adjusted example illustrates raw/adjusted mixing; source labels do not authenticate price basis or corporate-action treatment. No real data or model calibration accepted.'),dict(scope='Freshness policy',statement='One-day threshold is an illustrative caller decision, not a native limit or a proposed universal market policy. Structural eligibility is not current-data/model suitability.')]
result=dict(python=platform.python_version(),platform=platform.platform(),rows=rows,observations=observations,fixture_versions=versions,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),installed_modules={validation.__name__:dict(path=validation.__file__,sha256=hashlib.sha256(Path(validation.__file__).read_bytes()).hexdigest())},scope='Selected installed revision/basis/freshness boundary; caller selection separate; no source authentication, calibration or independent acceptance')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
