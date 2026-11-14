"""Exact testing-basics source;faulty variant and exact-money references are separate."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=ROOT/'chapter-20/20.01-why-financial-code-must-be-tested.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(REPO))],cwd=REPO,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);rows=[];commands=[]
def check(name,call,expected,tol=0):
    try:actual=call();ok=abs(actual-expected)<=tol if tol else actual==expected
    except Exception as exc:actual=type(exc).__name__;ok=actual==expected
    rows.append(dict(name=name,actual=str(actual),expected=str(expected),tolerance=tol,passed=ok))
with tempfile.TemporaryDirectory() as temp:
    path=Path(temp)/'financial_testing_basics.py';path.write_text(code)
    for label,argv in [('source demo/tests',[sys.executable,str(path)]),('source compilation',[sys.executable,'-m','compileall','-q',str(path)]),('quiet import',[sys.executable,'-c','import financial_testing_basics']),('optimized source validation/tests',[sys.executable,'-O',str(path)])]:
        z=subprocess.run(argv,cwd=temp,capture_output=True,text=True);commands.append(dict(label=label,argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location('testing_reference',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for name,flows,rate,expected in [('known NPV',[-100,110],.1,0.),('PV110',[0,110],.1,100.),('zero rate',[0,100],0.,100.),('negative valid',[0,95],-.05,100.)]:check(name,lambda f=flows,r=rate:m.npv(f,r),expected,1e-10)
    for flows,rate in [([-100,110],.05),([5,-7,9,3],-.1),([0,100,30],.2)]:
        exact=sum((Fraction(c)/(1+Fraction(rate))**t for t,c in enumerate(flows)),Fraction(0));check('independent represented-input NPV '+repr(flows),lambda f=flows,r=rate:m.npv(f,r),float(exact),1e-10)
    check('scaling',lambda:m.npv([-200,220],.05),2*m.npv([-100,110],.05),1e-10)
    check('append zero',lambda:m.npv([-100,110,0],.05),m.npv([-100,110],.05),1e-10)
    check('insert zero shifts later flow',lambda:m.npv([-100,0,110],.1),float(-100+Fraction(110,1)/Fraction(11,10)**2),1e-10)
    check('positive payment monotonicity',lambda:m.npv([0,100],.05)>m.npv([0,100],.06),True)
    check('negative payment direction',lambda:m.npv([0,-100],.05)<m.npv([0,-100],.06),True)
    check('generator flows',lambda:m.npv(iter([-100,110]),.1),0.,1e-10)
    for label,flows,rate in [('empty',[],.1),('rate boundary',[1],-1),('below boundary',[1],-1.1),('NaN flow',[float('nan')],0),('infinite rate',[1],float('inf')),('bool flow',[True],0),('text flow',['1'],0),('oversized flow',[10**1000],0),('oversized rate',[1],10**1000)]:check(label,lambda f=flows,r=rate:m.npv(f,r),'ValueError')
    check('known return',lambda:m.simple_return(100,101.5),.015,1e-16)
    check('zero end',lambda:m.simple_return(100,0),-1.)
    for label,start,end in [('zero start',0,1),('negative end',1,-1),('NaN start',float('nan'),1),('oversized return input',10**1000,1)]:check(label,lambda s=start,e=end:m.simple_return(s,e),'ValueError')
    start=1e308;end=math.nextafter(start,math.inf);expected=float((Fraction(end)-Fraction(start))/Fraction(start));check('near-unity complete return',lambda:m.simple_return(start,end),expected,expected*4e-15)
    check('true final return overflow',lambda:m.simple_return(1e-308,1e308),'ValueError')
    check('one cent across million',lambda:Fraction(1,100)*1000000,Fraction(10000))
    # Deliberately faulty supplemental implementation;published source is not mutated.
    faulty=re.sub(r'def simple_return\(.*?(?=\nclass FinancialTests)', 'def simple_return(start,end):\n    return end-start\n',code,flags=re.S)
    variant=Path(temp)/'faulty_variant.py';variant.write_text(faulty)
    bad=subprocess.run([sys.executable,str(variant),'FinancialTests.test_known_return'],cwd=temp,capture_output=True,text=True)
    restored=subprocess.run([sys.executable,str(path),'FinancialTests.test_known_return'],cwd=temp,capture_output=True,text=True)
    supplement=dict(scope='Existing test on deliberate supplemental faulty copy and unchanged source control;not original-source failure',faulty=dict(returncode=bad.returncode,stdout=bad.stdout,stderr=bad.stderr),source_control=dict(returncode=restored.returncode,stdout=restored.stdout,stderr=restored.stderr))
    if REV is None:(OUT/'faulty_variant.py.txt').write_text(faulty)
d=dict(selected_revision=REV,candidate_based_on='815dc77f8f5accf0166b6e4c107f5d861a86f8c2',python=sys.version,platform=platform.platform(),source_sha256=hashlib.sha256(code.encode()).hexdigest(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),commands=commands,predicates=rows,supplemental_fault_detection=supplement,existing_unique_methods=12,new_historical_unique_methods=0,limits='Annual positional NPV normal-range/return/input scope;NPV extreme discount/sum/underflow/resource behavior not certified;no model/platform/independent acceptance')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates;',sum(not x['passed'] for x in rows),'failed;4 source commands,12 existing methods,expected supplemental fault exit',bad.returncode)
assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in rows) and bad.returncode!=0 and restored.returncode==0
