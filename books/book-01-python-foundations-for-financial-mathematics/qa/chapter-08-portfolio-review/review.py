"""Section 8.5: exact lab and independent return-path checks."""
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import types
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'chapter-08/8.08-portfolio-visualizations.md'
EXPECTED = """Net marked value: USD 1000.00
Absolute marked value including cash: USD 1400.00
Signed weight sum: 1.000000
Absolute share sum: 1.000000
Risky gross / net value (cash excluded): 120.00%
Saved output/portfolio_visualizations.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-88-') as tmp:
        lab = Path(tmp) / 'visualization_lab_88'
        lab.mkdir()
        for name, body in [('portfolio_visualizations.py', program), ('test_portfolio_visualizations.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['portfolio_visualizations.py']),
            ('compilation', ['-m', 'compileall', '-q', '.']),
        ]:
            p = subprocess.run([sys.executable, '-B', '-W', 'error::FutureWarning', *args],
                               env=env, cwd=lab, capture_output=True, text=True, timeout=60)
            count = re.search(r'Ran (\d+) tests?', p.stderr)
            methods = int(count[1]) if count else None
            if label == 'test discovery':
                ok = methods == 8 and bool(re.search(r'^OK\s*$', p.stderr, re.M))
            elif label == 'demonstration':
                ok = p.stdout == EXPECTED and not p.stderr
            else:
                ok = not (p.stdout or p.stderr)
            commands.append(dict(label=label, args=args, returncode=p.returncode, stdout=p.stdout,
                                 stderr=p.stderr, methods=methods, passed=ok and p.returncode == 0))
        png = lab / 'output/portfolio_visualizations.png'
        if png.exists():
            (HERE / 'portfolio_visualizations.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m=types.ModuleType('exact_portfolio')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    h,instant=m.fixture()
    data,report=m.summarize(h,instant)
    amounts={'ALPHA':600,'BETA':400,'GAMMA':-200,'CASH':200}
    net=sum(amounts.values());absolute=sum(abs(x) for x in amounts.values())
    check('independent net and absolute sums',(report['net_value'],report['absolute_value_including_cash'])==(net,absolute))
    check('all signed weights and absolute shares match fractions',
          all(abs(data.loc[k,'weight']-float(Fraction(v,net)))<1e-12 and
              abs(data.loc[k,'absolute_share']-float(Fraction(abs(v),absolute)))<1e-12
              for k,v in amounts.items()))
    check('risky gross numerator excludes cash',
          abs(report['risky_gross_over_net']-float(Fraction(1200,1000)))<1e-12
          and report['cash_value']==200)
    bad=h.copy();bad.loc['GAMMA','price']=np.nan
    try:m.summarize(bad,instant)
    except ValueError as error:check('missing short valuation rejects entire snapshot','complete finite' in str(error))
    else:check('missing short valuation rejects entire snapshot',False)
    longonly=h.copy();longonly.loc['GAMMA','quantity']=0
    ld,lr=m.summarize(longonly,instant)
    check('long-only denominators coincide and zero holding remains',
          lr['net_value']==lr['absolute_value_including_cash']==1200 and
          np.array_equal(ld.weight,ld.absolute_share) and ld.loc['GAMMA','value']==0)
    scaled=h.copy();scaled['quantity']*=2
    sd,sr=m.summarize(scaled,instant)
    check('doubling quantities doubles monetary values but preserves ratios',
          sr['net_value']==2*net and sr['absolute_value_including_cash']==2*absolute
          and np.array_equal(sd.weight,data.weight) and np.array_equal(sd.absolute_share,data.absolute_share))
    check('deterministic tie sorts CASH before GAMMA',
          data.index.tolist()==['ALPHA','BETA','CASH','GAMMA'])
    fig,(left,right)=m.build_figure(h,instant)
    try:
        check('left artist retains short sign and right magnitude',
              np.allclose([b.get_width() for b in left.patches],[.6,.4,.2,-.2],atol=1e-12,rtol=0)
              and np.allclose([b.get_width() for b in right.patches],
                              [float(Fraction(x,1400)) for x in [600,400,200,200]],atol=1e-12,rtol=0))
        check('chart tick labels follow deterministic sorted rows',
              [t.get_text() for t in left.get_yticklabels()]==data.index.tolist())
    finally:m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
             matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'portfolio_visualizations.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
