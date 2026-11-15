"""Exact policy fences;independent coefficient/remainder half-even oracle."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib,json,hashlib,platform
from decimal import Decimal,Context,localcontext,ROUND_HALF_EVEN,ROUND_HALF_UP,ROUND_UP,Inexact,FloatOperation,DivisionByZero,InvalidOperation,Overflow
from fractions import Fraction
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-21/21.04-numerical-and-decimal-policies.md';raw=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();f=re.findall(r'```python\n(.*?)\n```',raw,re.S);assert len(f)==2;digests=[hashlib.sha256(c.encode()).hexdigest() for c in f];prior=json.loads((BOOK/'qa/chapter-21-policy-resume/results.json').read_text());assert digests==prior['fence_sha256'];assert all(c['returncode']==0 for c in prior['commands']);rows=[];commands=[];supp=[]
def oracle(x):
 sign,digits,exp=x.as_tuple();coef=int(''.join(map(str,digits)));shift=exp+2
 if coef==0:q=0
 elif shift>=0:
  if len(str(coef))+shift>28:return 'InvalidOperation'
  q=coef*10**shift
 else:
  if -shift>len(digits)+2:q=0
  else:
   divisor=10**(-shift);q,rem=divmod(coef,divisor)
   if rem*2>divisor or rem*2==divisor and q%2:q+=1
 if len(str(q))>28:return 'InvalidOperation'
 return Decimal((sign,tuple(map(int,str(q))),-2))
def check(name,fn,want):
 try:a=fn();ok=(type(a) is Decimal and a.as_tuple()==want.as_tuple()) if isinstance(want,Decimal) else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)
 for n,s in zip(['numerical_policy.py','test_numerical_policy.py'],f):(t/n).write_text(s)
 sys.path.insert(0,tmp);m=importlib.import_module('numerical_policy')
 for text in ['0','-0','0.005','0.015','0.025','-0.005','-0.015','-0.025','1.0049','1.0051','-1.0049','-1.0051','12.34','1','1e-100','-1e-100','99999999999999999999999999.99','99999999999999999999999999.995','1e30','1e100']:
  x=Decimal(text);check('independent half-even '+text,lambda x=x:m.round_to_example_cents(x),oracle(x))
 for label,x in [('float',1.005),('integer',1),('bool',True),('text','1.005'),('None',None),('bytes',b'1'),('nan',Decimal('NaN')),('snan',Decimal('sNaN')),('inf',Decimal('Infinity')),('-inf',Decimal('-Infinity'))]:check('reject '+label,lambda x=x:m.round_to_example_cents(x),'ValueError')
 ctx=m.example_context();check('precision',lambda:ctx.prec,28);check('rounding',lambda:ctx.rounding,ROUND_HALF_EVEN);check('Emin',lambda:ctx.Emin,-999999);check('Emax',lambda:ctx.Emax,999999);check('capitals',lambda:ctx.capitals,1);check('clamp',lambda:ctx.clamp,0);check('fresh flags clear',lambda:any(ctx.flags.values()),False);check('three configured traps',lambda:{k for k,v in ctx.traps.items() if v},{DivisionByZero,InvalidOperation,Overflow})
 ctx.prec=3;check('independent context objects',lambda:m.example_context().prec,28)
 with localcontext() as ambient:
  ambient.prec=3;ambient.rounding=ROUND_UP;ambient.traps[Inexact]=True;ambient.traps[FloatOperation]=True;ambient.flags[Inexact]=True;before=ambient.copy()
  check('conflicting caller context tie',lambda:m.round_to_example_cents(Decimal('1.005')),Decimal('1.00'));check('caller precision/rounding restored',lambda:(ambient.prec,ambient.rounding),(before.prec,before.rounding));check('caller flags restored',lambda:ambient.flags==before.flags,True);check('caller traps restored',lambda:ambient.traps==before.traps,True);check('exception path large amount',lambda:m.round_to_example_cents(Decimal('1e100')),'InvalidOperation');check('exception caller flags restored',lambda:ambient.flags==before.flags,True)
 if not REV:
  for label,args in [('optimized reference suite',['-O','-m','unittest','-v','test_numerical_policy']),('quiet import',['-c','import numerical_policy'])]:
   argv=[sys.executable]+args;z=subprocess.run(argv,cwd=t,capture_output=True,text=True);commands.append(dict(label=label,argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 sys.path.pop(0)
with localcontext(Context(prec=30)):
 x=Decimal('.005');cent=Decimal('.01');supp.append(dict(name='half-up stage/negative tie',passed=2*x.quantize(cent,rounding=ROUND_HALF_UP)==Decimal('.02') and (2*x).quantize(cent,rounding=ROUND_HALF_UP)==Decimal('.01') and (-x).quantize(cent,rounding=ROUND_HALF_UP)==Decimal('-.01')));supp.append(dict(name='quantum not increment',passed=Decimal('1.03').quantize(Decimal('.05'))==Decimal('1.03')));supp.append(dict(name='float conversion captures represented input',passed=Decimal(.1)!=Decimal('.1')));supp.append(dict(name='financial rational benchmarks are supplemental',passed=Fraction(110)/(1+Fraction(1,10))==100 and -100+Fraction(110)/(1+Fraction(1,10))==0))
d=dict(selected_revision=REV,python=sys.version,platform=platform.platform(),fence_sha256=digests,source_predicates=rows,supplemental_controls=supp,new_commands=commands,reused_commands=2,reused_revision=prior['source_revision'],existing_unique_methods=12,new_method_invocations=12 if not REV else 0,reused_method_invocations=12,new_historical_unique_methods=0,limits='Integer coefficient/remainder oracle independently derives quantization. Supplemental arithmetic not execution of an integrated financial module. Source-identical prior suite reused;currency/settlement/business policy,resources/platform/model/release/independent acceptance open. F28/F32 and other gaps retained.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',len(supp),'supplemental controls;',len(commands),'new commands;2prior commands reused');assert all(x['passed'] for x in rows+supp) and all(x['returncode']==0 for x in commands)
