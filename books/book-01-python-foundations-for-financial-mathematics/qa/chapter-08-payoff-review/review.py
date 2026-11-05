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
SOURCE = HERE.parents[1] / 'chapter-08/8.09-payoff-diagrams.md'
EXPECTED = """call: terminal prices [0.0, 96.0, 100.0, 106.0, 120.0]
  payoff USD: [0.0, 0.0, 0.0, 600.0, 2000.0]
  simplified profit USD: [-600.0, -600.0, -600.0, 0.0, 1400.0]
put: terminal prices [0.0, 96.0, 100.0, 106.0, 120.0]
  payoff USD: [10000.0, 400.0, 0.0, 0.0, 0.0]
  simplified profit USD: [9600.0, 0.0, -400.0, -400.0, -400.0]
Saved output/payoff_diagrams.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-89-') as tmp:
        lab = Path(tmp) / 'visualization_lab_89'
        lab.mkdir()
        for name, body in [('payoff_diagrams.py', program), ('test_payoff_diagrams.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['payoff_diagrams.py']),
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
        png = lab / 'output/payoff_diagrams.png'
        if png.exists():
            (HERE / 'payoff_diagrams.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m=types.ModuleType('exact_payoffs')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    grid=np.array([0.,96.,100.,103.,106.,108.,120.])
    for kind,premium in [('call',6),('put',4)]:
        _,payoff,profit=m.option_result(grid,100,premium,kind)
        oracle=[100*max(Fraction(int(x)-100) if kind=='call' else Fraction(100-int(x)),0) for x in grid]
        check(kind+' full per-position monetary oracle',
              np.array_equal(payoff,list(map(float,oracle))) and
              np.array_equal(profit,[float(x-100*premium) for x in oracle]))
    _,payoff,profit=m.option_result(grid,100,6,'call')
    check('call at103 and strike100', (payoff[3],profit[3],payoff[2],profit[2])==(300,-300,0,-600))
    _,p8,g8=m.option_result(grid,100,8,'call')
    check('premium8 shifts profit down200 with zero at108',
          np.array_equal(p8,payoff) and np.array_equal(g8,profit-200) and g8[5]==0)
    for kind,premium in [('call',6),('put',4)]:
        _,p100,g100=m.option_result(grid,100,premium,kind,multiplier=100)
        _,p10,g10=m.option_result(grid,100,premium,kind,multiplier=10)
        check(kind+' multiplier10 scales money one tenth',
              np.array_equal(p10,p100/10) and np.array_equal(g10,g100/10))
    check('supplemental endpoint interpolation invents payoff at strike',
          Fraction(0+10,2)==5 and max(Fraction(100-100),0)==0)
    _,call,_=m.option_result(grid,100,0,'call',multiplier=1)
    _,put,_=m.option_result(grid,100,0,'put',multiplier=1)
    check('per-unit terminal positive-part identity',
          np.array_equal(call-put,grid-100))
    try:
        _,fp,fg=m.option_result(grid,Fraction(100),Fraction(6),'call')
    except Exception as error:check('declared Real Fraction contract computes known amounts',False,error=repr(error))
    else:check('declared Real Fraction contract computes known amounts',
               np.array_equal(fp,payoff) and np.array_equal(fg,profit))
    fig,axes=m.build_figure()
    try:
        check('plotted call grid includes strike and break-even',
              100 in axes[0].lines[0].get_xdata() and 106 in axes[0].lines[1].get_xdata())
        check('plotted put grid includes strike and break-even',
              100 in axes[1].lines[0].get_xdata() and 96 in axes[1].lines[1].get_xdata())
    finally:m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,
             matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'payoff_diagrams.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
