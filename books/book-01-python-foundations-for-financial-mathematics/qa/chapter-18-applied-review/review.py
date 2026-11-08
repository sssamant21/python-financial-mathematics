from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
import re,tempfile,subprocess,sys,importlib.util,math,json,hashlib,platform
ROOT=Path(__file__).resolve().parents[4];BOOK=ROOT/'books/book-01-python-foundations-for-financial-mathematics'
def run():
    section=BOOK/'chapter-18/18.15-exercises-and-applied-problems.md';linked=BOOK/'chapter-18/18.14-chapter-project-monte-carlo-financial-simulator.md';text=section.read_text();source=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);project=re.search(r'~~~python\n(.*?)\n~~~',linked.read_text(),re.S).group(1);rows=[];commands=[]
    def check(name,actual,expected,approx=False):
        rows.append(dict(name=name,actual=repr(actual),expected=repr(expected),passed=math.isclose(actual,expected,rel_tol=1e-12,abs_tol=0) if approx else actual==expected))
    for name,actual,expected in [('E1',F(90,2)+F(110,2),100),('E2',F(6,10)*110+F(4,10)*90,102),('E3',F(90+110*3,4),105),('E4',F(1,4),F(25,100)),('E9',.75>=.75,True),('E11',F(110-100,100),F(1,10)),('E13',100*F(11,10)*F(9,10),99),('E14',F(-100,100),-1),('E18',F(100)*20/21,F(2000,21)),('E19',100-2,98),('E20',F(1,4),F(1,4)),('E21',F(1,4)*400+F(1,4)*400,200),('E23',math.sqrt(200/40000),math.sqrt(200/10000)/2),('E25',F(400+400,2),400),('E26 lower',F('100.1')-F('1.96')*F('.2'),F('99.708')),('E26 upper',F('100.1')+F('1.96')*F('.2'),F('100.492')),('E28',1000*F('.001'),1),('E31',F(1,12),F(1,12)),('E32',F('.05')-F('.2')**2/2,F('.03')),('E35',F('.6')*F('.10')+F('.4')*F('-.05'),F('.04')),('E36',F('.6')**2*F('.2')**2+F('.4')**2*F('.1')**2+2*F('.6')*F('.4')*F('.25')*F('.2')*F('.1'),F('.0184')),('E38',100-80,20),('E43',100000*253*8,202400000),('E44',divmod(100001,10000),(10,1)),('E47',F('.6')*F('-.2')+F('.4')*F('-.1'),F('-.16')),('E48',100*(F('1.05')-F('1.10')),-5)]:check(name,actual,expected)
    for precision in [80,120]:
        with localcontext() as ctx:
            ctx.prec=precision
            for name,actual,expected in [('E12',math.log(1.1),float(Decimal('1.1').ln())),('E16',100*math.exp(.06),float(Decimal(100)*Decimal('.06').exp())),('E17',100*math.exp(.04),float(Decimal(100)*Decimal('.04').exp())),('E22',math.sqrt(200/10000),float((Decimal(200)/10000).sqrt())),('E33',100*math.exp(.05),float(Decimal(100)*Decimal('.05').exp()))]:check(name+' decimal '+str(precision),actual,expected,True)
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp);(temp/'exercise_snippet.py').write_text(source);p=temp/'monte_carlo_financial_simulator.py';p.write_text(project)
        for args in [[sys.executable,'exercise_snippet.py'],[sys.executable,p.name],[sys.executable,'-m','compileall','-q','exercise_snippet.py',p.name]]:
            result=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr));assert result.returncode==0
        spec=importlib.util.spec_from_file_location('project',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        for alpha,v,e in [(.75,20,40),(.625,20,100/3),(.8,40,40)]:
            var,es=m.empirical_risk([-10,0,20,40],alpha);check('E39-42 VaR '+str(alpha),var,v);check('E39-42 ES '+str(alpha),es,e,True)
        replications=[]
        for seed in [42,7]:
            xs=m.sample_values(10000,seed);record=m.report(xs,100,.75);mean=sum(map(F,xs))/len(xs);variance=sum((F(x)-mean)**2 for x in xs)/(len(xs)-1);check('lab sample mean '+str(seed),record['mean_terminal'],float(mean),True);check('lab sample SE '+str(seed),record['standard_error_mean'],math.sqrt(float(variance)/len(xs)),True);replications.append(dict(seed=seed,report=record))
        out=dict(executable_source_revision=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),source_sha256=hashlib.sha256(section.read_bytes()).hexdigest(),linked_source_sha256=hashlib.sha256(linked.read_bytes()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,supplemental_predicates=rows,replications=replications,existing_unique_methods_rerun=12,new_historical_methods=0,limits='50 chapter-wide answer records/12 lab records, not added to560 local answers; source/supplemental/conceptual scopes distinct; no confidence coverage/model/platform/independent acceptance')
        (Path(__file__).parent/'results.json').write_text(json.dumps(out,indent=2)+'\n');assert all(row['passed'] for row in rows);print(len(rows),'predicates;3 source commands;12 linked existing methods passed')
if __name__=='__main__':run()
