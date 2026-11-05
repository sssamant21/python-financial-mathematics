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

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'chapter-08/8.11-sensitivity-and-scenario-charts.md'
EXPECTED = """Reference terminal balance: USD 1628.89
3% rate, 8 years: balance USD 1266.77; difference USD -362.12
Reference: 5%, 10 years: balance USD 1628.89; difference USD +0.00
7% rate, 12 years: balance USD 2252.19; difference USD +623.30
Saved output/scenario_charts.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-811-') as tmp:
        lab = Path(tmp) / 'visualization_lab_811'
        lab.mkdir()
        for name, body in [('scenario_charts.py', program), ('test_scenario_charts.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['scenario_charts.py']),
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
        png = lab / 'output/scenario_charts.png'
        if png.exists():
            (HERE / 'scenario_charts.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m=types.ModuleType('exact_scenarios')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    baseline=1000*Fraction(21,20)**10
    rows,actual=m.scenario_table()
    check('reference input contract and independent exact balance',
          rows[1][1:3]==(.05,10) and abs(actual-float(baseline))<1e-9,
          rational_balance=str(baseline))
    exact=[1000*Fraction(103,100)**8,baseline,1000*Fraction(107,100)**12]
    check('all named outputs and deltas match rational oracle',
          all(abs(row[3]-float(b))<1e-9 and abs(row[4]-float(b-baseline))<1e-9
              for row,b in zip(rows,exact)))
    check('supplemental basis point conversion',Fraction(5,100)+Fraction(100,10000)==Fraction(6,100))
    derivative=1000*10*Fraction(21,20)**9
    shocked=1000*Fraction(106,100)**10
    check('local derivative units differ from full finite shock',
          float(derivative)>15000 and 150<float(derivative*Fraction(1,100))<160
          and abs(float(shocked-baseline-derivative*Fraction(1,100)))>1,
          derivative=str(derivative),first_order=str(derivative*Fraction(1,100)),
          finite_shock=str(shocked-baseline))
    r=np.array([.01,.03,.05,.07,.09]);n=np.array([5,10,15,20])
    _,_,values=m.balance_grid(1000,r,n)
    oracle=np.array([[float(1000*Fraction(100+int(rate),100)**int(year)) for year in n]
                     for rate in [1,3,5,7,9]])
    check('entire rate-row horizon-column grid matches independent fractions',
          values.shape==(5,4) and np.allclose(values,oracle,rtol=0,atol=1e-8))
    check('matrix index2,1 is reference',abs(values[2,1]-float(baseline))<1e-9)
    try: fraction=m.balance_grid(Fraction(1000),r,n)[2]
    except Exception as error:check('declared Real Fraction principal accepted',False,error=repr(error))
    else:check('declared Real Fraction principal accepted',np.array_equal(fraction,values))
    fig,axes=m.build_figure()
    try:
        check('source scenario bar heights show full joint deltas',
              np.allclose([p.get_width() for p in axes[1].patches],
                          [float(x-baseline) for x in exact],atol=1e-9,rtol=0))
        mesh=axes[2].collections[0]
        check('mesh values preserve numerical grid orientation',
              np.allclose(mesh.get_array(),oracle,rtol=0,atol=1e-8))
        check('colorbar identifies USD and no probability is assigned',
              fig.axes[-1].get_ylabel()=='Terminal balance (USD)' and
              len(axes[2].texts)==20)
    finally:m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,
             matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'scenario_charts.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
