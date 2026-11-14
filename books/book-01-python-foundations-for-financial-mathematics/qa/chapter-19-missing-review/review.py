"""Exact extracted source commands and supplemental predicates, not acceptance."""
import copy,hashlib,importlib.util,json,os,platform,re,subprocess,sys,tempfile
from decimal import Decimal,InvalidOperation,localcontext
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
REL="chapter-19/19.08-missing-and-invalid-values.md"
REV=sys.argv[1] if len(sys.argv)>1 else None
path=ROOT/REL
text=subprocess.check_output(["git","show",REV+":"+str(path.relative_to(ROOT.parents[1]))],cwd=ROOT.parents[1],text=True) if REV else path.read_text()
code=re.search(r"~~~python\n(.*?)\n~~~",text,re.S).group(1)
rows=[];commands=[]
def check(name,actual,expected):
    rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/"missing_values.py";p.write_text(code)
    for cmd in [[sys.executable,str(p)],[sys.executable,"-m","compileall","-q",str(p)],[sys.executable,"-c","import missing_values"]]:
        z=subprocess.run(cmd,cwd=tmp,text=True,capture_output=True);commands.append(dict(argv=cmd,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location("missing_reference",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for name,row,expected in [("invalid row",[],"invalid_row"),("missing key",{},"missing_key"),("null",{"close":None},"null"),("empty",{"close":""},"empty"),("source marker",{"close":"N/A"},"source_missing"),("whitespace",{"close":"  "},"malformed"),("malformed",{"close":"abc"},"malformed"),("NaN",{"close":"NaN"},"nonfinite"),("sNaN",{"close":"sNaN"},"nonfinite"),("Infinity",{"close":"Infinity"},"nonfinite"),("negative infinity",{"close":"-Infinity"},"nonfinite"),("zero",{"close":"0"},"nonpositive"),("negative price",{"close":"-1"},"nonpositive"),("boolean",{"close":True},"invalid_type"),("float",{"close":100.},"invalid_type"),("Decimal input",{"close":Decimal("100")},"invalid_type"),("bytes",{"close":b"100"},"invalid_type"),("case-sensitive marker",{"close":"n/a"},"malformed"),("padded marker",{"close":" N/A "},"malformed")]:check(name,m.classify_close(row)[0],expected)
    for name,value in [("valid text","100.00"),("padded numeric"," 100.00 "),("exponent numeric","1e2"),("underscored numeric","1_00.00")]:check(name,m.classify_close({"close":value}),("valid",Decimal(value)))
    check("preserved Decimal scale",m.classify_close({"close":"100.00"})[1].as_tuple().exponent,-2)
    synthetic=[{"close":"100.00"},{"close":""},{"close":"102.00"},{"close":"NaN"}];saved=copy.deepcopy(synthetic)
    batch=m.classify_batch(iter(synthetic))
    check("batch counts",(batch['submitted'],len(batch['accepted']),len(batch['rejected']),batch['complete']),(4,2,2,False))
    check("accepted record positions",[x['record_number'] for x in batch['accepted']],[1,3])
    check("rejected reasons",batch['rejected'],[{'record_number':2,'reason':'empty'},{'record_number':4,'reason':'nonfinite'}])
    check("caller rows preserved",synthetic,saved)
    check("empty batch",m.classify_batch([]),dict(accepted=[],rejected=[],submitted=0,complete=True))
    check("no date/currency/key policy",m.classify_close({'close':'100','date':'invalid','currency':'wrong'})[0],'valid')
    check("duplicates not removed",len(m.classify_batch([{'close':'100'},{'close':'100'}])['accepted']),2)
    check("observed interval return",m.simple_return(Decimal('100'),Decimal('102')),Decimal('0.02'))
    check("zero terminal",m.simple_return(Decimal('100'),Decimal('0')),Decimal('-1'))
    check("negative return",m.simple_return(Decimal('100'),Decimal('98')),Decimal('-0.02'))
    check("exact zero",m.simple_return(Decimal('100'),Decimal('100')),Decimal('0'))
    check("near unity standalone",m.simple_return(Decimal('1'),Decimal('1.000000000000000000000000000001')),Decimal('1e-30'))
    with localcontext() as ctx:
        ctx.prec=2
        check("ambient return precision",m.simple_return(Decimal('100'),Decimal('102')),Decimal('0.02'))
        check("parse preserves text at low precision",m.classify_close({'close':'123456.789'})[1],Decimal('123456.789'))
        ctx.traps[InvalidOperation]=False
        check("malformed category independent of caller trap",m.classify_close({'close':'abc'})[0],'malformed')
    for name,start,end in [('zero start',Decimal('0'),Decimal('102')),('negative end',Decimal('100'),Decimal('-1')),('nonfinite start',Decimal('NaN'),Decimal('1')),('wrong return type',100,Decimal('1'))]:
        try:m.simple_return(start,end);actual='returned'
        except Exception as exc:actual=type(exc).__name__
        check(name,actual,'ValueError')
    fixture=OUT/'synthetic-records.json'
    expected=json.loads(fixture.read_text());check('fixture matches demonstration',synthetic,expected)
result=dict(baseline_revision=REV,candidate_based_on='f46c548b68ff7426d6d86effc462e352d77ccb35',manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),extracted_source_sha256=hashlib.sha256(code.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,predicates=rows,existing_reference_methods=12,new_historical_unique_methods=0,scope='Exact-source classification/return execution; supplemental predicates separate from lab,answer,workflow and historical methods;no financial/source/platform/independent acceptance')
file=OUT/('baseline.json' if REV else 'results.json');file.write_text(json.dumps(result,indent=2)+'\n')
failed=sum(not x['passed'] for x in rows);print(len(rows),'supplemental predicates;',failed,'failed;',len(commands),'source commands')
assert all(c['returncode']==0 for c in commands)
assert not failed
