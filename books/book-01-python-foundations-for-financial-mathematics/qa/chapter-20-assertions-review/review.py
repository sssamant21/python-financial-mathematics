"""Execute both exact source fences; supplemental faulty/optimization probes are separate."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from fractions import Fraction
from decimal import Decimal,Context,localcontext,ROUND_HALF_EVEN,Inexact,Rounded,Overflow
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.02-assertions-and-known-value-tests.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();fences=re.findall(r'~~~python\n(.*?)\n~~~',text,re.S);assert len(fences)==2;code=fences[1];commands=[];rows=[]
def check(name,fn,want,tol=0):
 try:a=fn();ok=abs(a-want)<=tol if tol else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=str(a),expected=str(want),tolerance=tol,passed=ok))
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'known_value_tests.py';src.write_text(code);(tmp/'assertion_example.py').write_text(fences[0])
 for label,args in [('assert source',[sys.executable,'assertion_example.py']),('reference tests',[sys.executable,src.name]),('compile both source fences',[sys.executable,'-m','compileall','-q','.']),('quiet import',[sys.executable,'-c','import known_value_tests']),('optimized reference tests',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('known_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for name,flows,rate,want in [('PV110',[0,110],.1,100),('zero NPV',[-100,110],.1,0),('zero rate',[0,100],0,100),('negative rate',[0,95],-.05,100)]:check(name,lambda f=flows,r=rate:m.npv(f,r),want,1e-10)
 for flows,rate in [([5,-7,9],-.1),([-100,110],.05)]:
  want=float(sum((Fraction(x)/(1+Fraction(rate))**i for i,x in enumerate(flows)),Fraction()));check('rational NPV '+repr(flows),lambda f=flows,r=rate:m.npv(f,r),want,1e-10)
 for name,flows,rate in [('empty',[],0),('rate boundary',[1],-1),('NaN flow',[math.nan],0),('bool flow',[True],0),('infinite rate',[1],math.inf),('oversized flow',[10**1000],0),('oversized rate',[1],10**1000)]:check(name,lambda f=flows,r=rate:m.npv(f,r),'ValueError')
 check('scaling',lambda:m.npv([-200,220],.05),2*m.npv([-100,110],.05),1e-10);check('append zero',lambda:m.npv([-100,110,0],.05),m.npv([-100,110],.05),1e-10);check('insert zero differs',lambda:m.npv([-100,0,110],.05)!=m.npv([-100,110],.05),True);check('future monotonic',lambda:m.npv([0,100],.05)>m.npv([0,100],.06),True)
 def reference(s,e):
  # Independent high-precision Decimal evaluation,then declared report rounding.
  with localcontext(Context(prec=150,rounding=ROUND_HALF_EVEN)):exact=(Decimal(e)-Decimal(s))/Decimal(s)
  with localcontext(Context(prec=28,rounding=ROUND_HALF_EVEN)):return +exact
 for s,e in [('100','101.50'),('100','0'),('3','4'),('1','1.00000000000000000000000000001'),('1','0.99999999999999999999999999999'),('1E100','1.00000000000000000000000000001E100')]:check('decimal '+s+' -> '+e,lambda s=s,e=e:m.decimal_return(Decimal(s),Decimal(e)),reference(s,e))
 for name,s,e in [('zero start',Decimal(0),Decimal(1)),('negative end',Decimal(1),Decimal(-1)),('NaN start',Decimal('NaN'),Decimal(1)),('signaling NaN',Decimal('sNaN'),Decimal(1)),('float price',1.,Decimal(1))]:check(name,lambda s=s,e=e:m.decimal_return(s,e),'ValueError')
 def hostile(kind):
  with localcontext() as c:
   c.prec=3;c.Emax=9;c.Emin=-9
   if kind=='trap':c.traps[Inexact]=True;c.traps[Rounded]=True
   if kind=='overflow':c.traps[Overflow]=False;return m.decimal_return(Decimal('1e-20'),Decimal(1))
   return m.decimal_return(Decimal(3),Decimal(4))
 check('caller precision/exponent isolated',lambda:hostile('normal'),reference('3','4'));check('caller traps isolated',lambda:hostile('trap'),reference('3','4'));check('caller overflow disabled isolated',lambda:hostile('overflow'),reference('1e-20','1'))
 check('integer exact assertion',lambda:2+2==4,True);check('near-zero absolute acceptance',lambda:math.isclose(1e-12,0,rel_tol=0,abs_tol=1e-10),True);check('symmetric isclose vs asymmetric sum',lambda:(math.isclose(2,1,rel_tol=.4,abs_tol=.7),abs(2-1)<=.7+.4*abs(1)),(False,True))
 # Controlled mutation and assertion omission illustrate lab contracts,not original-source defects.
 faulty=code.replace('enumerate(flows)','enumerate(flows[1:])');(tmp/'faulty.py').write_text(faulty)
 probes=[]
 for label,args,expected in [('faulty time-zero copy',[sys.executable,'faulty.py','KnownValueTests.test_zero_npv'],1),('source control',[sys.executable,src.name,'KnownValueTests.test_zero_npv'],0),('supplemental assert false normal',[sys.executable,'-c','assert False, "deliberate"'],1),('supplemental assert false optimized',[sys.executable,'-O','-c','assert False, "deliberate"'],0)]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);probes.append(dict(label=label,argv=args,returncode=z.returncode,expected_returncode=expected,stdout=z.stdout,stderr=z.stderr,passed=z.returncode==expected))
 if not REV:(OUT/'faulty_variant.py.txt').write_text(faulty)
d=dict(candidate_based_on='9392004a95ed37258177ee1cf1018d9170cbb3b3',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in fences],commands=commands,predicates=rows,supplemental_probes=probes,existing_unique_methods=12,method_invocations=26,new_historical_unique_methods=0,limits='Selected ordinary NPV/Decimal contracts; broad NPV range, Decimal conversion resource bounds, platform and independent acceptance remain open')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates;',sum(not x['passed'] for x in rows),'failed;',len(commands),'source commands; supplemental probes',all(x['passed'] for x in probes));assert all(x['passed'] for x in rows) and all(x['returncode']==0 for x in commands) and all(x['passed'] for x in probes)
