"""Prepared exact-source checkpoint;not compiled or executed during preparation."""
from pathlib import Path
import re,sys,json,tempfile,subprocess,importlib.util,hashlib
from decimal import Decimal
q=Path(__file__).resolve().parent
baseline="--baseline" in sys.argv
path=q/"baseline-source.txt" if baseline else q.parents[1]/"chapter-19/19.14-chapter-project-financial-data-pipeline.md"
text=path.read_text();code=re.search(r"~~~python\n(.*?)\n~~~",text,re.S).group(1)
commands=[];rows=[]
def check(name,call,expected):
    try:actual=call()
    except Exception as exc:actual=type(exc).__name__
    rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
with tempfile.TemporaryDirectory() as temp:
    p=Path(temp)/"financial_data_pipeline.py";p.write_text(code)
    for cmd in [[sys.executable,str(p)],[sys.executable,"-m","compileall","-q",str(p)],[sys.executable,"-c","import financial_data_pipeline"]]:
        z=subprocess.run(cmd,cwd=temp,text=True,capture_output=True)
        commands.append(dict(argv=cmd,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location("project_reference",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    raw=m.example();cutoff="2026-01-07T12:00:00Z"
    check("nominal return",lambda:Decimal(json.loads(m.run_pipeline(raw,cutoff)[0])["simple_return"]),Decimal(".015"))
    check("early cutoff",lambda:m.run_pipeline(raw,"2026-01-06T21:00:00Z"),"ValueError")
    check("equal cutoff",lambda:Decimal(json.loads(m.run_pipeline(raw,"2026-01-06T22:00:00Z")[0])["simple_return"]),Decimal(".015"))
    d=json.loads(raw);d[0]["close"]="1";d[1]["close"]="1.000000000000000000000000000001"
    check("complete near-unity",lambda:Decimal(json.loads(m.run_pipeline(json.dumps(d).encode(),cutoff)[0])["simple_return"]),Decimal("1e-30"))
    for v in ["2026-01-07T12:00:00+01:60","2026-01-07T12:00:00-01:60","2026-01-07T12:00:00+00:99","0001-01-01T00:00:00+00:01","9999-12-31T23:59:59-00:01"]:
        check("timestamp "+v,lambda v=v:m.instant(v),"ValueError")
result=dict(source_revision="66ae5eaf6d8c0ea6fcd301407001c13bdab46341",baseline=baseline,source_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,predicates=rows,scope="Initial baseline only;full formal lab and branch/context/resource review remains")
(q/("baseline-runtime.json" if baseline else "runtime.json")).write_text(json.dumps(result,indent=2)+"\n")
assert all(x["returncode"]==0 for x in commands) and all(x["passed"] for x in rows)
