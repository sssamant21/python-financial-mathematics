"""Section 8.6: exact lab and independent histogram oracle."""
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
SOURCE = HERE.parents[1] / 'chapter-08/8.06-histograms-and-return-distributions.md'
EXPECTED = """Slots: 13; observed: 11; missing: 2
Unequal-bin counts: [2, 2, 3, 4]
Sample shares sum: 1.000000
Density area: 1.000000
Observed negative fraction: 36.36%
Saved output/return_histograms.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-86-') as tmp:
        lab = Path(tmp) / 'visualization_lab_86'
        lab.mkdir()
        for name, body in [('return_histograms.py', program), ('test_return_histograms.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['return_histograms.py']),
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
        png = lab / 'output/return_histograms.png'
        if png.exists():
            (HERE / 'return_histograms.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m=types.ModuleType('exact_histograms')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    sample=m.fixture()
    edges=np.array([-.10,-.02,0,.02,.10])
    out0=m.summarize(sample,edges)
    integer_returns=[-8,-4,-2,-1,0,0,1,2,3,4,10]
    bounds=[-10,-2,0,2,10]
    counts=[sum(a<=x and (x<b or (i==3 and x==b)) for x in integer_returns)
            for i,(a,b) in enumerate(zip(bounds,bounds[1:]))]
    widths=[Fraction(b-a,100) for a,b in zip(bounds,bounds[1:])]
    density=[Fraction(n,11)/w for n,w in zip(counts,widths)]
    check('scalar half-open bin oracle with closed final edge',out0['counts'].tolist()==counts,expected=counts)
    check('all unequal densities match rational reference',
          np.allclose(out0['density'],list(map(float,density)),atol=1e-12,rtol=0),expected=list(map(str,density)))
    check('exact boundary -2% starts second bin and +10% is included',
          m.summarize(np.array([-.02,.10]),edges)['counts'].tolist()==[0,1,0,1])
    check('observed negative fraction uses eleven eligible values',
          (int(sum(out0['observed']<0)),len(out0['observed']),out0['missing'])==(4,11,2))
    check('supplemental rational area and density units',
          Fraction(5,20)/Fraction(5,100)==5 and Fraction(5,20)/5==Fraction(1,20))
    rev=m.summarize(sample[::-1],edges)
    check('reversal preserves counts and densities',all(np.array_equal(rev[k],out0[k]) for k in ('counts','density')))
    filled=m.summarize(np.nan_to_num(sample),edges)
    check('supplemental zero filling changes denominator and zero bin',
          filled['counts'].tolist()==[2,2,5,4] and filled['missing']==0 and len(filled['observed'])==13)
    bad=sample.copy();bad[0]=-.15
    try:m.build_figure(bad)
    except ValueError as error:check('figure rejects tail outside declared support','cover every' in str(error))
    else:check('figure rejects tail outside declared support',False)
    fig,(left,right)=m.build_figure(sample)
    try:
        check('source stairs are counts on left and density on right',
              left.patches[0].get_data().values.tolist()==[1,3,6,1] and
              np.allclose(right.patches[0].get_data().values,list(map(float,density)),atol=1e-12,rtol=0))
    finally:m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,
             matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'return_histograms.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
