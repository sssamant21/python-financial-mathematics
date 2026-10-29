from decimal import Decimal as D,localcontext,Underflow,Inexact
from fractions import Fraction as F
import hashlib,json,platform,sys
from pathlib import Path
from reference import signed_present_value,post_usd_cents,scenario_report,finance,SOURCE,CODE
HERE=Path(__file__).resolve().parent

def run():
 checks=[]
 def ck(task,label,actual,expected):checks.append(dict(task=task,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(task,expected,call):
  try:call();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(task,'expected rejection',actual,expected)
 for flow,expected in [('125','100'),('-125','-100'),('0','0')]:ck(1,'signed receipt/payment',signed_present_value(D(flow),periodic_rate=D('.25'),periods=1),D(expected))
 err(1,'TypeError',lambda:signed_present_value('125',periodic_rate=D('.25'),periods=1));err(1,'ValueError',lambda:signed_present_value(D('NaN'),periodic_rate=D('.25'),periods=0));err(1,'ValueError',lambda:finance.present_value(D(-125),periodic_rate=D('.25'),periods=1))
 # Exact positive mathematical growth = (10^-2000)^1000 = 10^-2000000.
 near_minus_one=D((1,(9,)*2000,-2000))
 with localcontext(finance._policy()) as c:
  base=D(1)+near_minus_one;growth=base**1000
  observed=dict(base=str(base),growth=str(growth),underflow=c.flags[Underflow],inexact=c.flags[Inexact])
 ck(2,'positive representable base',base,D('1e-2000'));ck(2,'positive exact factor underflows to zero',growth==0,True);ck(2,'underflow signal',observed['underflow'],True)
 err(2,'ArithmeticError',lambda:finance.accumulation_factor(near_minus_one,periods=1000))
 for raw,expected in [('1.004','1.00'),('1.005','1.01'),('-1.005','-1.01'),('0','0.00')]:ck(3,'final cents HALF_UP',post_usd_cents(D(raw)),D(expected))
 err(3,'ValueError',lambda:post_usd_cents(D('Infinity')));err(3,'ValueError',lambda:post_usd_cents(D('1e25')))
 raw=D('1.005');ck(3,'posting stage changes later arithmetic',(raw*2,post_usd_cents(raw)*2),(D('2.010'),D('2.02')));ck(3,'raw preserved',raw,D('1.005'))
 # Task4 requires documenting a conversion before adding fractional powers.
 ck(4,'independent quarterly equivalent known pair',F(51,50)**4-1,F(8243216,100000000))
 rows=scenario_report(D(1000),[D('.12'),D(0)],frequency=12,periods=12,currency='USD');ck(5,'scenario rows',len(rows),2);ck(5,'monthly conversion',rows[0]['periodic_effective_rate'],D('.01'));ck(5,'FV exact rational',F(rows[0]['future_amount']),F(1000)*F(101,100)**12);ck(5,'zero rate amount',rows[1]['future_amount'],D(1000));ck(5,'metadata counts',(rows[0]['periods'],rows[0]['periods_per_year'],rows[0]['currency']),(12,12,'USD'))
 (HERE/'scenario-report.json').write_text(json.dumps(rows,default=str,indent=2)+'\n')
 out=dict(python=sys.version,platform=platform.platform(),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),canonical_code_sha256=hashlib.sha256(CODE.encode()).hexdigest(),tasks=6,runtime_predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),underflow_probe=observed,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
