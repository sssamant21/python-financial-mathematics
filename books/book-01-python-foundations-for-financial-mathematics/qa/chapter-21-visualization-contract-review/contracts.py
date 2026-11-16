"""Scoped source plot contracts; no installed-package or visual certification."""
from pathlib import Path
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
from fractions import Fraction
import json,sys,math
import matplotlib,matplotlib.pyplot as plt,matplotlib.dates as dates
from financial_toolkit import plot_price_series
UTC=timezone.utc;T1=datetime(2025,1,2,16,tzinfo=UTC);T2=T1+timedelta(days=1);rows=[]
def add(case,actual,expected):
 rows.append(dict(case=case,actual=repr(actual),expected=repr(expected),passed=actual==expected))
def call(times=None,prices=None,instrument='EXAMPLE',currency='USD',basis='Unadjusted'):
 return plot_price_series([T1,T2] if times is None else times,[100.,110.] if prices is None else prices,instrument,currency,basis)
def outcome(**kwargs):
 try:
  f,a=call(**kwargs);plt.close(f);return 'returned'
 except Exception as e:return type(e).__name__
start=set(plt.get_fignums());times=[T1,T2];prices=[100.,110.];f,a=call(times=times,prices=prices)
add('one new figure',len(set(plt.get_fignums())-start),1);add('caller figure ownership',plt.fignum_exists(f.number),True);add('returned axis ownership',a.figure is f,True);add('one plotted line',len(a.lines),1);line=a.lines[0];add('untransformed prices',list(line.get_ydata()),prices);add('marker',line.get_marker(),'o');add('line label',line.get_label(),'EXAMPLE');add('title',a.get_title(),'EXAMPLE — Unadjusted price');add('x units',a.get_xlabel(),'Observation time (UTC)');add('y units',a.get_ylabel(),'Price (USD)');add('grid',any(l.get_visible() for l in a.get_xgridlines()),True);add('time instants in UTC',[x.astimezone(UTC) for x in line.get_xdata()],[T1,T2]);add('formatter timezone',a.xaxis.get_major_formatter().tz,UTC);add('input ownership',times==[T1,T2] and prices==[100.,110.],True);add('independent day difference',float(dates.date2num(line.get_xdata())[1]-dates.date2num(line.get_xdata())[0]),1.);add('price-return interpretation',math.isclose(float(Fraction(prices[1])/Fraction(prices[0])-1),.1,abs_tol=1e-15),True);plt.close(f);add('caller closes figure',set(plt.get_fignums()),start)
for name,kwargs in [('tuple input',dict(times=(T1,T2),prices=(100.,110.))),('generator times',dict(times=iter([T1,T2]))),('too short',dict(times=[T1],prices=[1.])),('different lengths',dict(prices=[1.])),('integer price',dict(prices=[1.,2])),('bool price',dict(prices=[1.,True])),('zero price',dict(prices=[1.,0.])),('negative price',dict(prices=[1.,-1.])),('nan price',dict(prices=[1.,math.nan])),('infinite price',dict(prices=[1.,math.inf])),('naive time',dict(times=[T1.replace(tzinfo=None),T2])),('reversed time',dict(times=[T2,T1])),('duplicate instant',dict(times=[T1,T1.astimezone(timezone(timedelta(hours=2)))])),('label padding',dict(instrument=' EXAMPLE')),('empty basis',dict(basis='')),('lower currency',dict(currency='usd')),('structural currency only',dict(currency='ZZZ')),('UTC lower range',dict(times=[datetime.min.replace(tzinfo=timezone(timedelta(hours=1))),T2])),('UTC upper range',dict(times=[T1,datetime.max.replace(tzinfo=timezone(timedelta(hours=-1)))]))]:
 add(name,outcome(**kwargs),'returned' if name in ('tuple input','structural currency only') else 'ValueError')
z=ZoneInfo('America/New_York');u=datetime(2025,11,2,1,30,tzinfo=z,fold=0);v=datetime(2025,11,2,1,15,tzinfo=z,fold=1)
add('DST fold UTC order',outcome(times=[u,v]),'returned');add('DST reverse UTC order',outcome(times=[v,u]),'ValueError')
t=[T1+timedelta(seconds=i) for i in range(10000)];add('point cap accepted',outcome(times=t,prices=[1.]*len(t)),'returned');add('over cap rejected',outcome(times=t+[T2],prices=[1.]*(len(t)+1)),'ValueError');add('no leaked probe figures',set(plt.get_fignums()),start)
d=dict(predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),matplotlib=matplotlib.__version__,backend=matplotlib.get_backend(),limits='Source-injected Agg structure/input/lifecycle checks. No wheel,interactive/browser/notebook/platform,accessibility or financial/data/model acceptance. UTC extreme exceptions count as one contract defect exposed at two boundaries; structural ZZZ acceptance is not currency authentication.')
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
