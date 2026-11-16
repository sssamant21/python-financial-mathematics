"""Section9.1 lab CLI/prose alignment: no imported source helper as oracle.
Usage: python THIS manuscript.md results.json
"""
from pathlib import Path
import sys,json,subprocess,ast,math,re
from decimal import Decimal,localcontext
from fractions import Fraction
if not __debug__:raise RuntimeError('lab checks require assertions enabled')
manuscript=Path(sys.argv[1]) if len(sys.argv)>1 else None;out=Path(sys.argv[2]) if len(sys.argv)>2 else None;records=[]
z=subprocess.run([sys.executable,str(Path(__file__).with_name('section_9_01.py'))],capture_output=True,text=True,timeout=60)
assert z.returncode==0,z.stderr
actual={line.split(':',1)[0]:ast.literal_eval(line.split(':',1)[1].strip()) for line in z.stdout.splitlines()}
def oracle(precision):
 with localcontext() as ctx:
  ctx.prec=precision;D=Decimal;R=D.from_float(.04);H=D.from_float(.0001);T=D(5);V=D(10000)*(-R*T).exp();P=D(20);q=D(400)/(P*P.sqrt());slope=-D(600)/(P*P*P.sqrt())
  return {'Discounted sensitivity':dict(value=float(V),absolute=float(-T*V),normalized_rate=5.,elasticity=float(-R*T)),'1bp shock':dict(first_order=float(-T*V*H),exact=float(D(10000)*(-(R+H)*T).exp()-V)),'Demand':dict(quantity=float(q),absolute=float(slope),elasticity=-1.5),'Portfolio':dict(value=2000.,absolute=20.,elasticity=.5)}
expected=oracle(90);assert expected==oracle(140)
for label,fields in expected.items():
 ok=set(actual[label])==set(fields);records.append(dict(name=label+' schema',kind='CLI schema',passed=ok));assert ok
 for key,want in fields.items():
  got=actual[label][key];ok=math.isclose(got,want,rel_tol=5e-14,abs_tol=1e-12)
  records.append(dict(name=label+' '+key,kind='CLI numerical',actual=got,expected=want,passed=ok))
if manuscript is not None:
 s=manuscript.read_text()
 with localcontext() as ctx:
  ctx.prec=100;V=Decimal(10000)*Decimal('-.2').exp();printed=[('value',format(V.quantize(Decimal('.000001')),'f')),('derivative',format((-5*V).quantize(Decimal('.000001')),'f')),('one bp',format((Decimal('-.0005')*V).quantize(Decimal('.000001')),'f'))]
 for name,want in printed:
  ok=want in s;records.append(dict(name='printed '+name,kind='printed answer',expected=want,found=ok,passed=ok))
 ok='```bash\npython section_9_01.py\npython check_section_9_01.py\n```' in s and r'\`' not in s
 records.append(dict(name='runnable command fence and inline code',kind='static markup',passed=ok))
# Exercise10 exact units are a caller/model derivation,not a native unit conversion API.
for label,a,want in [('one percent of four percent',Fraction(4,100)*Fraction(1,100),Fraction(4,10000)),('one percentage point',Fraction(4,100)+Fraction(1,100),Fraction(5,100))]:
 records.append(dict(name=label,kind='supplemental unit derivation',actual=str(a),expected=str(want),passed=a==want))
result=dict(records=records,passed=sum(x['passed'] for x in records),failed=sum(not x['passed'] for x in records),source_cli=dict(argv=z.args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr),oracle='90/140-digit independent Decimal exp discount references; demand closed form uses sqrt rather than source logarithm/exponential scaling; exact rational units.',limits='Lab default CLI and selected printed answers/static command fence. No comprehensive arbitrary-input,rendered visual,extension,financial/model/platform or independent acceptance.')
result['manuscript_checks_executed']=manuscript is not None
if out is not None:out.write_text(json.dumps(result,indent=2)+'\n')
print(result['passed'],'passed',result['failed'],'failed');raise SystemExit(bool(result['failed']))
