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
SOURCE = HERE.parents[1] / 'chapter-08/8.10-interest-and-investment-growth-curves.md'
EXPECTED = """Simple 5% per year: year 20 balance USD 2000.00
Annual 5% nominal: year 20 balance USD 2653.30
Monthly 5% nominal: year 20 balance USD 2712.64
Continuous 5% force: year 20 balance USD 2718.28
Effective annual rate from monthly 5% nominal: 5.116190%
Saved output/growth_curves.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-810-') as tmp:
        lab = Path(tmp) / 'visualization_lab_810'
        lab.mkdir()
        for name, body in [('growth_curves.py', program), ('test_growth_curves.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['growth_curves.py']),
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
        png = lab / 'output/growth_curves.png'
        if png.exists():
            (HERE / 'growth_curves.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m=types.ModuleType('exact_growth')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    from decimal import Decimal,localcontext
    with localcontext() as ctx:
        ctx.prec=60
        rate=Decimal('0.05');one=Decimal(1);principal=Decimal(1000)
        oracles=[principal*(1+rate*20),principal*(1+rate)**20,
                 principal*(1+rate/12)**240,principal*(rate*20).exp()]
        effective=(1+rate/12)**12-1
        equivalent=12*((one+rate)**(one/12)-one)
    curves=m.fixture()
    check('independent high-precision four endpoints',
          np.allclose([c[2][-1] for c in curves],list(map(float,oracles)),atol=1e-9,rtol=0),
          decimal_references=list(map(str,oracles)))
    check('simple interest at10 and annual recurrence',
          abs(m.growth(1000,.05,np.array([0.,10.]),'simple')[1][-1]-1500)<1e-12 and
          np.allclose(curves[1][2][1:],curves[1][2][:-1]*1.05,atol=1e-9,rtol=0))
    check('nominal monthly effective annual exceeds five percent',effective>rate,reference=str(effective))
    annual_years=np.arange(21,dtype=float)
    monthly=m.growth(1000,float(equivalent),annual_years,'periodic',12)[1]
    check('equivalent monthly nominal matches every common year-end',
          np.allclose(monthly,[float(1000*Fraction(21,20)**i) for i in range(21)],atol=1e-9,rtol=0),
          equivalent_nominal=str(equivalent))
    try:m.growth(1000,.05,np.array([0.,.5]),'periodic')
    except ValueError as error:check('annual rejects half-year credit','whole credit periods' in str(error))
    else:check('annual rejects half-year credit',False)
    half=m.growth(1000,.05,np.array([0.,.5]),'periodic',12)[1][-1]
    check('monthly accepts six completed periods',
          abs(half-float(1000*(1+Fraction(1,240))**6))<1e-9)
    try:m.growth(1000,-.5,np.array([0.,2.]),'simple')
    except ValueError as error:check('simple negative rate rejects zero balance','strictly positive' in str(error))
    else:check('simple negative rate rejects zero balance',False)
    try:
        fractional=m.growth(Fraction(1000),Fraction(1,20),annual_years,'periodic')[1]
    except Exception as error:check('declared Real Fraction scalars accepted',False,error=repr(error))
    else:check('declared Real Fraction scalars accepted',
               np.allclose(fractional,curves[1][2],atol=1e-9,rtol=0))
    fig,axes=m.build_figure()
    try:
        check('log scale retains exact source monetary arrays',
              axes[1].get_yscale()=='log' and all(np.array_equal(a.get_ydata(),b.get_ydata())
                        for a,b in zip(axes[0].lines,axes[1].lines)))
        check('periodic artists are post-step and others linearly connected',
              [line.get_drawstyle() for line in axes[0].lines]==['default','steps-post','steps-post','default'])
    finally:m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,
             matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'growth_curves.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
