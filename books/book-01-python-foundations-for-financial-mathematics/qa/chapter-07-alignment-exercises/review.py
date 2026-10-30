"""Section7.1 local prompts, unchanged source and labelled renderer supplement."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd
from renderer import render
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
    checks=[];commands=[]
    def ck(section,label,a,x):checks.append(dict(section=section,label=label,actual=repr(a),expected=repr(x),status='PASS' if a==x else 'FAIL'))
    def reject(section,label,fn):
        try:fn();actual='no exception';detail=''
        except Exception as error:actual=type(error).__name__;detail=traceback.format_exc()
        ck(section,label,actual,'ValueError');checks[-1]['expected_exception_trace']=detail
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    def command(section,label,args,cwd,expected=None,count=None,environment=False):
        r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
        counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
        if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))
        if expected is not None:
            normalize=lambda s:[' '.join(line.split()) for line in s.splitlines()]
            ok=ok and normalize(r.stdout)==normalize(expected) and r.stderr==''
        if environment:
            v=json.loads(r.stdout);ok=ok and (v['python'],v['pandas'],v['numpy'])==('3.12.14','2.2.3','2.3.5') and r.stderr==''
        commands.append(dict(section=section,label=label,args=args,cwd_role='lab directory' if label=='quiet import' else 'parent directory',returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
    source=BOOK/'chapter-07/7.01-why-pandas.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==5
    program,test=blocks[3:5];expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-alignment-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_71';lab.mkdir()
        for name,code in [('alignment.py',program),('test_alignment.py',test)]:
            (lab/name).write_text(code);compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_71/alignment.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_71','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_71'],parent,expected='')
        ck('ALL','two source listings unchanged',{n:sha((lab/n).read_bytes())for n in ('alignment.py','test_alignment.py')},{'alignment.py':sha(program.encode()),'test_alignment.py':sha(test.encode())})
        m=types.ModuleType('exact_alignment');exec(compile(program,str(source),'exec'),m.__dict__)
        w=pd.Series([.6,.3,.1],index=['ALPHA','BETA','CASH']);r=pd.Series([0.,.1,-.05],index=['CASH','ALPHA','BETA']);wc=w.copy(deep=True);rc=r.copy(deep=True)
        base,total=m.contributions(w,r);expected_total=F(3,5)*F(1,10)+F(3,10)*F(-1,20)+F(1,10)*0
        for order in [('ALPHA','BETA','CASH'),('BETA','CASH','ALPHA'),('BETA','ALPHA','CASH')]:
            frame,t=m.contributions(w,r.reindex(list(order)))
            ck('E1','permutation '+','.join(order),(abs(t-float(expected_total))<=1e-12,frame.index.tolist(),frame.equals(base)),(True,w.index.tolist(),True))
        wrong_terms=[F(3,5)*0,F(3,10)*F(1,10),F(1,10)*F(-1,20)]
        ck('E2','manual wrong pair contributions',list(map(float,wrong_terms)),[0.,.03,-.005])
        ck('E2','exact wrong positional total',float(sum(wrong_terms)),.025)
        ck('E2','NumPy shape-valid positional error observed',abs(float(w.to_numpy()@r.to_numpy())-float(sum(wrong_terms)))<=1e-12,True)
        ck('E2','aligned versus unaligned gap',float(expected_total-sum(wrong_terms)),.02)
        missing=r.drop('BETA');reject('E3','missing BETA rejected before partial aggregation',lambda:m.contributions(w,missing))
        partial=w*missing
        ck('E3','missing negative contribution conceals oversized partial result',(pd.isna(partial.loc['BETA']),abs(partial.sum()-float(F(3,50)))<=1e-12),(True,True))
        extra=pd.concat([r,pd.Series([.02],index=['OTHER'])]);reject('E4','unexpected source asset rejected',lambda:m.contributions(w,extra))
        ck('E4','discarding unexpected source would conceal mismatch',m.contributions(w,extra.reindex(w.index))[1],total)
        nanr=r.copy();nanr.loc['BETA']=np.nan;unguarded=w*nanr
        ck('E5','default sum skips unknown contribution',abs(unguarded.sum()-float(F(3,50)))<=1e-12,True)
        ck('E5','strict sum exposes unknown contribution',pd.isna(unguarded.sum(skipna=False)),True)
        reject('E5','validated function rejects supplied NaN',lambda:m.contributions(w,nanr))
        duplicate=r.copy();duplicate.index=['CASH','ALPHA','ALPHA'];reject('E6','duplicate return labels rejected',lambda:m.contributions(w,duplicate))
        dupw=w.copy();dupw.index=['ALPHA','ALPHA','CASH'];reject('E6','duplicate weight labels rejected',lambda:m.contributions(dupw,r))
        ck('E6','pandas object may carry duplicate labels',duplicate.index.is_unique,False)
        before=base.copy(deep=True);rendered=render(base,total)
        expected_render='ALPHA: weight 60.00%; return 10.00%; contribution 6.00 pp\nBETA: weight 30.00%; return -5.00%; contribution -1.50 pp\nCASH: weight 10.00%; return 0.00%; contribution 0.00 pp\nPortfolio price return: 4.50%; contributions 4.50 pp\n'
        ck('E8','renderer matches independently derived percentage points',rendered,expected_render)
        ck('E8','renderer preserves numeric report',base.equals(before),True)
        ck('E8','stored fractions not overwritten as percentage points',bool(np.allclose(base['contribution'],[float(F(3,50)),float(F(-3,200)),0.],rtol=0,atol=1e-12)),True)
        ck('E8','source report remains numeric',[str(x)for x in base.dtypes],['float64']*3)
        ck('ALL','all source calls preserve inputs',(w.equals(wc),r.equals(rc)),(True,True))
        (HERE/'rendered.txt').write_text(rendered)
        snapshot=dict(scope='unchanged source result stores numeric fractions;percentage points are display only',source_sha256=sha(source.read_bytes()),report=base.reset_index(names='asset').to_dict(orient='records'),portfolio_price_return=total)
        (HERE/'numeric-report.json').write_text(json.dumps(snapshot,indent=2,allow_nan=False)+'\n')
        # Separate supplemental caller exercises renderer beside exact original module.
        (lab/'renderer.py').write_bytes((HERE/'renderer.py').read_bytes())
        demo="import pandas as pd\nfrom alignment import contributions\nfrom renderer import render\nw=pd.Series([.6,.3,.1],index=['ALPHA','BETA','CASH'])\nr=pd.Series([0.,.1,-.05],index=['CASH','ALPHA','BETA'])\nframe,total=contributions(w,r)\nprint(render(frame,total),end='')\n"
        (lab/'render_demo.py').write_text(demo);command('E8','supplemental renderer caller',['pandas_lab_71/render_demo.py'],parent,expected=expected_render)
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),renderer_sha256=sha((HERE/'renderer.py').read_bytes()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='E1-6 exact source calls and mechanical contrasts;E7 metadata design only;E8 supplemental renderer,no manuscript change')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
