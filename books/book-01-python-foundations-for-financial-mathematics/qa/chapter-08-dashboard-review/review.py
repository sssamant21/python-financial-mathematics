"""Exact Section 8.13 project, with rational and byte-level QA oracles."""
import hashlib, importlib.util, json, os, platform, re, shutil, subprocess, sys, tempfile
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-08/8.13-chapter-project-financial-analytics-dashboard.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    raw=SOURCE.read_bytes()
    blocks=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',raw,re.M|re.S)
    fixture,=re.findall(rb'^\x60\x60\x60csv\n(.*?)^\x60\x60\x60',raw,re.M|re.S)
    assert len(blocks)==3
    program,tests,verify=blocks
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    env={k:v for k,v in os.environ.items() if k not in ('PYTHONPATH','PYTHONHOME')}
    def command(label,args,lab,expected=None,methods=None):
        p=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,env=env,capture_output=True,text=True,timeout=120)
        match=re.search(r'Ran (\d+) tests?',p.stderr)
        count=int(match[1]) if match else None
        ok=p.returncode==0
        if expected is not None:ok=ok and p.stdout==expected and not p.stderr
        if methods is not None:ok=ok and count==methods and bool(re.search(r'^OK\s*$',p.stderr,re.M))
        commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,
                             methods=count,passed=ok))
    with tempfile.TemporaryDirectory(prefix='book1-dashboard-') as tmp:
        lab=Path(tmp)/'visualization_lab_813';lab.mkdir()
        for name,body in [('dashboard.py',program),('test_dashboard.py',tests),('verify_outputs.py',verify),('prices.csv',fixture)]:
            (lab/name).write_bytes(body)
        command('documented unittest',['-m','unittest','-v'],lab,methods=16)
        expected=('Price coverage: 11/12\nComplete return pairs: 3/5\nFull strict linked paths: 1/2\n'
                  f'Input SHA-256: {sha(fixture)}\nSaved dashboard, audit tables, and evidence to output/run01\n')
        command('documented demonstration',['dashboard.py','--input','prices.csv','--out','output/run01'],lab,expected=expected)
        command('documented compile',['-m','compileall','-q','.'],lab,expected='')
        command('optional exact evidence verifier',['verify_outputs.py'],lab,expected='All recorded output digests match.\n')
        out=lab/'output/run01';e=json.loads((out/'evidence.json').read_text())
        ck('fixture publication digest',sha(fixture)=='0f9ec721d779423c2505a6c7788b81d60fba107e8347c7891c1f4973c006f27c')
        ck('code and input evidence identify consumed listings',e['code_sha256']==sha(program) and e['input_sha256']==sha(fixture))
        ck('all six output hashes recomputed independently',len(e['output_sha256'])==6 and all(sha((out/n).read_bytes())==s for n,s in e['output_sha256'].items()))
        for p in out.iterdir():
            if p.suffix in ('.csv','.json'):shutil.copyfile(p,HERE/p.name)
        shutil.copyfile(out/'dashboard.png',HERE/'dashboard.png')
        spec=importlib.util.spec_from_file_location('exact_dashboard',lab/'dashboard.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        grid=pd.date_range('2026-01-01T00:00:00Z',periods=6,freq='D')
        prices,_=m.load_prices(lab/'prices.csv',grid);result=m.analyze(prices)
        ref_prices=np.array([[100,200],[110,202],[99,204],[np.nan,206],[108,208],[108,210]],dtype=float)
        ck('every aligned price and gap',np.array_equal(prices.to_numpy(),ref_prices,equal_nan=True))
        simple=np.array([[np.nan,np.nan],[.1,float(F(202,200)-1)],[-.1,float(F(204,202)-1)],
                         [np.nan,float(F(206,204)-1)],[np.nan,float(F(208,206)-1)],[0,float(F(210,208)-1)]])
        ck('every adjacent return rational oracle',np.allclose(result['returns'],simple,atol=1e-12,rtol=0,equal_nan=True))
        ck('strict linked ALPHA blocks after first missing ratio',
           np.allclose(result['linked'].ALPHA,[0,.1,-.01,np.nan,np.nan,np.nan],atol=1e-12,rtol=0,equal_nan=True))
        ck('strict linked BETA matches independent endpoint ratios at every row',
           np.allclose(result['linked'].BETA,[float(F(x,200)-1) for x in [200,202,204,206,208,210]],atol=1e-12,rtol=0))
        ck('endpoint-only and full-path releases distinct',
           e['assets'][0]['final_strict_linked'] is None and abs(e['assets'][0]['endpoint_only_change']-.08)<1e-12
           and abs(e['assets'][1]['final_strict_linked']-.05)<1e-12)
        ck('pair endpoints exactly Jan2 Jan3 Jan6',
           result['pairs'].index.equals(grid[[1,2,5]]))
        lines=fixture.splitlines(keepends=True)
        reverse=lines[0]+b''.join(lines[:0:-1])
        rev=lab/'reverse.csv';rev.write_bytes(reverse)
        rp,rm=m.load_prices(rev,grid);rr=m.analyze(rp)
        ck('reversed bytes differ but financial products unchanged',rm['input_sha256']!=e['input_sha256'] and
           all(rr[k].equals(result[k]) for k in ('prices','returns','linked','pairs','indexed')) and rr['report']==result['report'])
        duplicate=lab/'duplicate.csv';duplicate.write_bytes(fixture+lines[1])
        target=lab/'rejected'
        try:m.run(duplicate,target,grid)
        except ValueError as error:ck('duplicate rejected before report directory creation',not target.exists(),error=str(error))
        else:ck('duplicate rejected before report directory creation',False)
        full=lab/'complete.csv';full.write_bytes(fixture+b'2026-01-04T00:00:00Z,ALPHA,USD,105\n')
        fp,_=m.load_prices(full,grid);fr=m.analyze(fp)
        ck('separate complete fixture releases two paths and all pairs',fr['report']['full_linked_paths']==2 and fr['report']['complete_pair_intervals']==5
           and abs(fr['linked'].ALPHA.iloc[-1]-float(F(108,100)-1))<1e-12)
        absent=lab/'absent.csv';absent.write_bytes(b''.join(line for line in lines if not line.startswith(b'2026-01-03')))
        ap,_=m.load_prices(absent,grid)
        ck('independent schedule retains wholly absent instant',len(ap)==6 and ap.iloc[2].isna().all())
        fig,axes=m.build_dashboard(result)
        try:
            ck('price and linked artists preserve distinct gaps',
               np.isnan(axes[0,0].lines[0].get_ydata()).tolist()==[False,False,False,True,False,False] and
               np.isnan(axes[0,1].lines[0].get_ydata()).tolist()==[False,False,False,True,True,True])
            ck('histogram counts preserve sample sizes',
               [int(p.get_data().values.sum()) for p in axes[1,0].patches]==[3,5])
            ck('scatter uses BETA x ALPHA y with observed zero',
               np.allclose(axes[1,1].collections[0].get_offsets(),
                           result['pairs'][['BETA','ALPHA']].to_numpy(),atol=1e-12,rtol=0))
        finally:m.plt.close(fig)
        from unittest.mock import patch
        original=m.matplotlib.figure.Figure.savefig
        failed_dir=lab/'failed-export';open_before=set(m.plt.get_fignums())
        def fail_svg(fig,path,*args,**kwargs):
            if Path(path).suffix=='.svg':raise OSError('QA simulated SVG export failure')
            return original(fig,path,*args,**kwargs)
        with patch.object(m.matplotlib.figure.Figure,'savefig',fail_svg):
            try:m.run(lab/'prices.csv',failed_dir,grid)
            except OSError as error:
                ck('expected partial export has PNG but no completion record and closes figure',
                   str(error)=='QA simulated SVG export failure' and
                   (failed_dir/'dashboard.png').exists() and not (failed_dir/'evidence.json').exists()
                   and set(m.plt.get_fignums())==open_before)
            else:ck('expected partial export has PNG but no completion record and closes figure',False)
        before={p.name:sha(p.read_bytes()) for p in out.iterdir()}
        try:m.run(lab/'prices.csv',out,grid)
        except FileExistsError:ck('existing report directory remains byte-identical',before=={p.name:sha(p.read_bytes()) for p in out.iterdir()})
        else:ck('existing report directory remains byte-identical',False)
    output=dict(source_sha256=sha(raw),program_sha256=sha(program),tests_sha256=sha(tests),verifier_sha256=sha(verify),
                fixture_sha256=sha(fixture),python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
                matplotlib=m.matplotlib.__version__,platform=platform.platform(),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
