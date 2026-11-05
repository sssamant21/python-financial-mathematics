"""Twenty Chapter 9 answers: exact suites, observed source assertions, independent oracles."""
import ast,hashlib,io,json,math,platform,re,subprocess,sys,tempfile,types,unittest
from decimal import Decimal as D,localcontext
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-09/9.17-exercises-and-applied-problems.md'
    project=BOOK/'chapter-09/9.16-chapter-project-time-value-of-money-engine.md'
    def extract(p):
        code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',p.read_bytes(),re.M|re.S)
        return code
    code=extract(source);capstone=extract(project);commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,actual,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(actual,float(expected),abs_tol=atol,rel_tol=rtol),actual=actual,reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    with tempfile.TemporaryDirectory(prefix='book1-917-') as tmp:
        Path(tmp,'chapter09_reference_checks.py').write_bytes(code);Path(tmp,'tvm_engine.py').write_bytes(capstone)
        for label,args,count in [('exact twenty reference methods',['chapter09_reference_checks.py'],20),('exact compilation',['-m','compileall','-q','chapter09_reference_checks.py'],None),('separate corrected capstone integration',['tvm_engine.py'],12)]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);actual=int(match[1]) if match else None
            ok=p.returncode==0 and (actual==count and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if count else not(p.stdout or p.stderr))
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,methods=actual,returncode=p.returncode,passed=ok))
    m=types.ModuleType('exact_chapter_nine');exec(compile(code,str(source),'exec'),m.__dict__)
    observed={}
    for name in ('assertAlmostEqual','assertEqual','assertGreater'):
        original=getattr(unittest.TestCase,name)
        def wrap(self,*args,_original=original,_name=name,**kwargs):
            observed.setdefault(self._testMethodName,[]).append(dict(assertion=_name,actual=args[0],expected=args[1]))
            return _original(self,*args,**kwargs)
        setattr(m.ChapterNineChecks,name,wrap)
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(m.ChapterNineChecks))
    (HERE/'observer.log').write_text(stream.getvalue())
    ck('same twenty observer methods',result.wasSuccessful() and result.testsRun==20,methods=result.testsRun)
    with localcontext() as ctx:
        ctx.prec=100
        rational={1:F(5500)*F(25,27),2:F(0),3:F(2950),4:F(2500)*F(53,50)**3,5:F(8000)*F(20,21)**4,6:F(3000)*F(26,25)**5,7:F(100,107)**3,8:F(100)*F(10,11)+F(200)*F(10,11)**2,9:-1000+F(600)*F(10,11)+F(600)*F(10,11)**2,10:F(101,100)**12-1,11:F(1000)*F(201,200)**12,13:F(1,10),16:F(2000),17:F(1000)*F(19,20)**2,18:F(0),19:F(3),20:-1000+F(400)*F(150,151)**12+F(500)*F(150,151)**24+F(300)*F(150,151)**36}
        expected={i:D(f.numerator)/D(f.denominator) for i,f in rational.items()}
        expected[12]=D(1500)*D('.1').exp();expected[14]=D(2).ln()/D('1.08').ln();expected[15]=12*((D('1.10').ln()/12).exp()-1)
        continuous=D('1.10').ln()
        expected_records={i:str(x) for i,x in expected.items()}
    for i in range(1,21):
        actual=observed['test_%02d'%i][0]['actual']
        close('P%02d observed exact source value'%i,actual,expected[i])
    # Full literal timeline from the exact source AST, beyond the weak first-coordinate source assertion.
    tree=ast.parse(code);method=next(x for x in ast.walk(tree) if isinstance(x,ast.FunctionDef) and x.name=='test_02')
    timeline=ast.literal_eval(next(x for x in ast.walk(method) if isinstance(x,ast.List)))
    ck('P02 full source timeline',timeline==[(0,-2000),(1,900),(3,1400)],actual=timeline)
    close('P01 premium over immediate receipt',observed['test_01'][0]['actual']-5000,expected[1]-5000)
    ck('P14 first complete annual credit is10',F(27,25)**9<2<=F(27,25)**10)
    ck('P15 continuous quote rounded percent',round(float(continuous)*100,6)==9.531018,decimal_reference=str(continuous))
    ck('P15 nominal quote rounded percent',round(float(expected[15])*100,4)==9.5690)
    close('P19 first signed amount',observed['test_19'][1]['actual'],-1000)
    # Literal rows executed by the source csv parser are supplied in the exact source test.
    csv_call=next(x for x in ast.walk(tree) if isinstance(x,ast.Constant) and isinstance(x.value,str) and x.value.startswith('year,amount'))
    ck('P19 complete source CSV literal',csv_call.value=='year,amount\n0,-1000\n1,400\n2,800\n')
    p20=source.read_text().split('### Problem 20')[1].split('## Practical verification lab')[0]
    output=re.search(r'(?:≈|=)\s*([+-]?[\d,]+(?:\.\d+)?)\s*USD',p20)
    ck('P20 prompt requests evaluated numeric NPV',output is not None and abs(float(output[1].replace(',',''))-float(expected[20]))<=5e-5,expected=str(expected[20]),numeric_answer_found=output[1] if output else None)
    # Limits: reference helpers are fixed-fixture checks, not validated arbitrary-input APIs.
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),project_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),commands=commands,checks=checks,observed_assertions=observed,independent_expectations=expected_records,chapter_wide_answer_records=20,section_workflows_added=0,local_prompt_records_added=0,existing_method_invocations_final=20+result.testsRun+12,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
