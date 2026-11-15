from pathlib import Path
import subprocess,sys,tempfile,re,json,hashlib,platform,importlib
from decimal import Decimal,localcontext,ROUND_UP,Inexact
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];pin='835777284697e2a6ce3f7fdc27dcd7efa3666e4e';rel='books/book-01-python-foundations-for-financial-mathematics/chapter-21/21.04-numerical-and-decimal-policies.md';raw=subprocess.check_output(['git','show',pin+':'+rel],cwd=ROOT,text=True);f=re.findall(r'```python\n(.*?)\n```',raw,re.S);assert len(f)==2;commands=[]
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)
 for n,s in zip(['numerical_policy.py','test_numerical_policy.py'],f):(t/n).write_text(s)
 for args in [['-m','unittest','-v','test_numerical_policy'],['-m','compileall','-q','numerical_policy.py','test_numerical_policy.py']]:
  argv=[sys.executable]+args;z=subprocess.run(argv,cwd=t,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 sys.path.insert(0,tmp);m=importlib.import_module('numerical_policy')
 with localcontext() as ctx:
  ctx.prec=3;ctx.rounding=ROUND_UP;ctx.traps[Inexact]=True;before=ctx.copy();values=[str(m.round_to_example_cents(Decimal(x))) for x in ['1.005','1.015','-1.005']];unchanged=ctx.prec==before.prec and ctx.rounding==before.rounding and ctx.flags==before.flags and ctx.traps==before.traps
 try:m.round_to_example_cents(Decimal('1e100'));large='returned'
 except Exception as e:large=type(e).__name__
 observations=[dict(name='half-even ties under conflicting ambient context',actual=values,expected=['1.00','1.02','-1.00'],passed=values==['1.00','1.02','-1.00']),dict(name='ambient settings/flags/traps preserved',passed=unchanged),dict(name='declared large coefficient limit',actual=large,expected='InvalidOperation',passed=large=='InvalidOperation')]
 d=dict(source_revision=pin,source_sha256=hashlib.sha256(raw.encode()).hexdigest(),fence_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in f],python=sys.version,platform=platform.platform(),commands=commands,observations=observations,existing_unique_methods=12,method_invocations=12,new_historical_unique_methods=0,limits='Partial source runtime only;40answers/12lab/fullcontext/exception/conversion policy review pending. Large coefficient rejection documented,notnewdefect. No currency/settlement/platform/release/independent acceptance.')
(OUT/'results.json').write_text(json.dumps(d,indent=2)+'\n');assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in observations);print('2source commands/12methods/3policy observations pass;formal21.4pending')
