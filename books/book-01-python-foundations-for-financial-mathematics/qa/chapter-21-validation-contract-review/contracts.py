"""Source/installed validation contracts; UTC range expectations are explicit."""
from datetime import datetime,timedelta,timezone,tzinfo
from zoneinfo import ZoneInfo,TZPATH
from dataclasses import FrozenInstanceError
from fractions import Fraction
from pathlib import Path
import json,sys,math
from financial_toolkit import validate_price_record,validated_price_return,PriceObservation,simple_price_return
UTC=timezone.utc;T1=datetime(2025,1,2,16,tzinfo=UTC);T2=datetime(2025,1,3,16,tzinfo=UTC);CUT=T2+timedelta(hours=2)
def record(price=100.,observed=T1,available=T1,**changes):
 d=dict(instrument='EXAMPLE',currency='USD',price=price,observed_at=observed,available_at=available,source='synthetic');d.update(changes);return d
rows=[]
def add(case,got,want,kind='contract'):
 ok=got==want if isinstance(want,(str,bool)) else math.isclose(got,want,rel_tol=5e-14,abs_tol=1e-12)
 rows.append(dict(case=case,actual=repr(got),expected=repr(want),kind=kind,passed=ok))
def call(fn):
 try:return fn()
 except Exception as e:return type(e).__name__
for start,end in [(100.,110.),(100.,90.),(100.,100.),(1e-200,1.1e-200),(1e200,1.1e200)]:
 a=validated_price_return(record(start),record(end,T2,T2),CUT);want=float(Fraction(end)/Fraction(start)-1);add(f'validated rational return {start} to {end}',a,want,'numeric')
for name,change in [('missing source',lambda d:d.pop('source')),('extra field',lambda d:d.update(extra='x')),('integer price',lambda d:d.update(price=100)),('boolean price',lambda d:d.update(price=True)),('zero price',lambda d:d.update(price=0.)),('negative price',lambda d:d.update(price=-1.)),('nan price',lambda d:d.update(price=math.nan)),('infinite price',lambda d:d.update(price=math.inf)),('instrument spaces',lambda d:d.update(instrument=' EXAMPLE')),('empty source',lambda d:d.update(source='')),('lowercase currency',lambda d:d.update(currency='usd')),('unicode currency',lambda d:d.update(currency='U\u0405D')),('naive observed',lambda d:d.update(observed_at=T1.replace(tzinfo=None))),('naive available',lambda d:d.update(available_at=T1.replace(tzinfo=None))),('reversed availability',lambda d:d.update(available_at=T1-timedelta(microseconds=1))),('future availability',lambda d:d.update(available_at=CUT+timedelta(microseconds=1)))]:
 d=record();change(d);add(name,call(lambda:validate_price_record(d,CUT)),'ValueError')
for name,d,cut in [('none record',None,CUT),('naive cutoff',record(),CUT.replace(tzinfo=None)),('none cutoff',record(),None)]:add(name,call(lambda:validate_price_record(d,cut)),'ValueError')
a=validate_price_record(record(available=CUT),CUT);add('availability equality accepted',a.available_at==CUT,True)
a=validate_price_record(record(available=CUT-timedelta(microseconds=1)),CUT);add('availability just before accepted',a.available_at<CUT,True)
for label,second in [('instrument mismatch',record(110.,T2,T2,instrument='OTHER')),('currency mismatch',record(110.,T2,T2,currency='EUR')),('equal observation time',record(110.,T1,T1)),('decreasing observation time',record(110.,T1-timedelta(seconds=1),T1)),('zero ending price narrower layer',record(0.,T2,T2))]:add(label,call(lambda:validated_price_return(record(),second,CUT)),'ValueError')
add('lower-level total-loss domain',simple_price_return(100.,0.),-1.)
a=validated_price_return(record(),record(110.,T2,T2,source='other-source'),CUT);add('different source labels deliberately accepted',a,.1)
a=validate_price_record(record(currency='ZZZ'),CUT);add('currency format not ISO authentication',a.currency,'ZZZ')
plus=timezone(timedelta(hours=5,minutes=30));a=validate_price_record(record(observed=T1.astimezone(plus),available=T1),CUT);add('equivalent offsets accepted',a.observed_at==T1,True);add('provided timezone preserved',a.observed_at.tzinfo is plus,True)
# Explicit UTC instants independently specify the repeated-hour chronology.
z=ZoneInfo('America/New_York');first=datetime(2025,11,2,1,30,tzinfo=z,fold=0);second=datetime(2025,11,2,1,15,tzinfo=z,fold=1);cut=datetime(2025,11,2,8,tzinfo=UTC)
add('DST first UTC reference',first.astimezone(UTC)==datetime(2025,11,2,5,30,tzinfo=UTC),True);add('DST second UTC reference',second.astimezone(UTC)==datetime(2025,11,2,6,15,tzinfo=UTC),True);add('DST fold pair by instant',validated_price_return(record(100.,first,first),record(110.,second,second),cut),.1)
add('DST reversed availability',call(lambda:validate_price_record(record(observed=second,available=first),cut)),'ValueError')
d=record();before=d.copy();a=validate_price_record(d,CUT);add('dictionary ownership',d==before,True);add('frozen record type',type(a)is PriceObservation,True)
try:a.price=2.;kind='mutable'
except Exception as e:kind=type(e).__name__
add('ordinary frozen assignment',kind,'FrozenInstanceError')
# Local instants beyond Python's representable UTC range are invalid inputs
# to a UTC-comparison API; the documented category is ValueError.
lo=datetime.min.replace(tzinfo=timezone(timedelta(hours=1)));hi=datetime.max.replace(tzinfo=timezone(-timedelta(hours=1)))
for label,dt in [('UTC lower range',lo),('UTC upper range',hi)]:add(label,call(lambda:validate_price_record(record(observed=dt,available=dt),dt)),'ValueError','UTC range/exception contract')
add('extreme finite price ratio overflow',call(lambda:validated_price_return(record(1e-308),record(1e308,T2,T2),CUT)),'ValueError')
# These demonstrate limits, not failures or extra predicates.
observations=[dict(case='revision/freshness not authenticated',actual=repr(validate_price_record(record(source='unverified-revision'),CUT)),status='OPEN broader F32/source/adjustment/freshness/version-history design; structural pass is not authenticity'),dict(case='nonexistent local wall time',actual=repr(validate_price_record(record(observed=datetime(2025,3,9,2,30,tzinfo=z),available=datetime(2025,3,9,8,tzinfo=UTC)),datetime(2025,3,10,tzinfo=UTC))),status='Local-time parsing/resolution belongs to upstream boundary; no nonexistent-time certification')]
d=dict(source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),timezone_search_path=list(TZPATH),observations=observations,limits='Selected exact source validation contracts on this Python/Linux tzdb. Frozen record not audit proof; F28/F32, custom tzinfo policies, source revisions, freshness, adjusted basis and platform/independent acceptance remain open. No formal40-answer/12-lab/wheel acceptance claimed by this source probe.')
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
