"""Section 8.1: exact lab and independent rational checks."""
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
SOURCE = HERE.parents[1] / 'chapter-08/8.02-matplotlib-fundamentals.md'
EXPECTED = """Final balance: USD 1215.51
Cumulative gain: USD 215.51
Axes array shape: (2, 1)
Saved output/matplotlib_fundamentals.png
Saved output/matplotlib_fundamentals.svg
"""

def main():
    source = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', source, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    from xml.etree import ElementTree
    with tempfile.TemporaryDirectory(prefix='chapter08-82-') as tmp:
        lab = Path(tmp) / 'visualization_lab_82'
        lab.mkdir()
        for name, body in [('matplotlib_fundamentals.py', program), ('test_matplotlib_fundamentals.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['matplotlib_fundamentals.py']),
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
        png = lab / 'output/matplotlib_fundamentals.png'
        if png.exists():
            (HERE / 'matplotlib_fundamentals.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
        svg = lab / 'output/matplotlib_fundamentals.svg'
        check('documented SVG parses',svg.exists() and ElementTree.parse(svg).getroot().tag.endswith('}svg'))
    module = types.ModuleType('exact_fundamentals')
    exec(compile(program, str(SOURCE), 'exec'), module.__dict__)
    years = np.arange(5)
    _, balance, gain = module.balance_schedule(1000, .05, years)
    expected = [1000 * Fraction(21,20)**i for i in range(5)]
    check('independent rational balances and gains',
          np.allclose(balance, list(map(float,expected)),atol=1e-11,rtol=0)
          and np.allclose(gain,[float(x-1000) for x in expected],atol=1e-11,rtol=0),
          expected=list(map(str,expected)))
    check('year-two cumulative gain differs from one-year increase',
          abs(gain[2]-102.5)<1e-12 and abs(balance[2]-balance[1]-52.5)<1e-12)
    try:
        _, b, _ = module.balance_schedule(Fraction(1000), Fraction(1,20), years)
    except Exception as e:
        check('supported Real fractions produce the known schedule',False,error=repr(e))
    else:
        check('supported Real fractions produce the known schedule',
              np.allclose(b,list(map(float,expected)),atol=1e-11,rtol=0))
    try:
        module.balance_schedule(1000, Fraction(-1)+Fraction(1,2**60), years)
    except Exception as e:
        check('rate rounding to -1 rejected by range validation',isinstance(e,ValueError),actual=repr(e))
    else:
        check('rate rounding to -1 rejected by range validation',False,actual='no error')
    plt = module.plt
    with plt.rc_context({'font.size':17}):
        fig, axes = module.build_figure(1000,.05,years)
        try:
            upper = axes[0,0]
            check('Figure, Axes and y-axis ownership',
                  upper.figure is fig and upper.yaxis.axes is upper and upper.yaxis.label is upper.yaxis.get_label())
            check('style is restored outside source build',plt.rcParams['font.size']==17
                  and upper.get_legend().get_texts()[0].get_fontsize()==10)
        finally:
            plt.close(fig)
    from unittest.mock import patch
    from pathlib import Path as P
    before=set(plt.get_fignums())
    original=module.matplotlib.figure.Figure.savefig
    def fail_svg(fig,path,*args,**kwargs):
        if P(path).suffix=='.svg':
            raise OSError('QA simulated SVG write error')
        return original(fig,path,*args,**kwargs)
    with tempfile.TemporaryDirectory() as tmp:
        previous=os.getcwd()
        try:
            os.chdir(tmp)
            with patch.object(module.matplotlib.figure.Figure,'savefig',fail_svg):
                try: module.main()
                except OSError as e:
                    check('source closes figure and retains PNG after simulated SVG error',
                          str(e)=='QA simulated SVG write error' and set(plt.get_fignums())==before
                          and P('output/matplotlib_fundamentals.png').exists()
                          and not P('output/matplotlib_fundamentals.svg').exists())
                else: check('source closes figure and retains PNG after simulated SVG error',False)
        finally:
            os.chdir(previous)
    import io, struct
    fig, axes = plt.subplots(1,1,squeeze=False,figsize=(10,4))
    try:
        check('supplemental subplot keeps 1 by 1 container',axes.shape==(1,1))
        lines=axes[0,0].plot([0,1],[0,1])
        check('supplemental plot returns a list of Line2D objects',isinstance(lines,list)
              and len(lines)==1 and isinstance(lines[0],module.matplotlib.lines.Line2D))
        png=io.BytesIO()
        fig.savefig(png,format='png',dpi=200)
        check('supplemental uncropped raster is 2000 by 800',struct.unpack('>II',png.getvalue()[16:24])==(2000,800))
    finally:
        plt.close(fig)
    out=dict(python=platform.python_version(), numpy=np.__version__, matplotlib=module.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(source),program_sha256=sha(program),tests_sha256=sha(tests),
             png_sha256=sha((HERE/'matplotlib_fundamentals.png').read_bytes()),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
