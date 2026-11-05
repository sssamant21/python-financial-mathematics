"""Section 9.16 exact-source review. Prepared, not executed at publication.
Run from any directory with Python 3.12+; --source can target a baseline copy.
Every invocation creates a new runs/<UTC>-<uuid>/ directory; retain all failures.
"""
import argparse
import datetime
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import types
import uuid

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parents[1] / "chapter-09/9.16-chapter-project-time-value-of-money-engine.md"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    listings = re.findall(rb"^" + b"\x60"*3 + rb"python\n(.*?)^" + b"\x60"*3, raw, re.M|re.S)
    if len(listings) != 1:
        raise ValueError("expected exactly one complete Python listing")
    code = listings[0]
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = HERE / "runs" / (stamp + "-" + uuid.uuid4().hex[:12])
    outdir.mkdir(parents=True, exist_ok=False)
    commands, checks = [], []
    def check(label, fn):
        try:
            detail = fn()
            checks.append(dict(label=label, passed=True, detail=detail))
        except Exception as exc:
            checks.append(dict(label=label, passed=False, exception=repr(exc)))
    def close(actual, expected, atol=1e-10, rtol=1e-12):
        assert math.isclose(actual, float(expected), abs_tol=atol, rel_tol=rtol), (actual, str(expected))
        return dict(actual=actual, expected=str(expected), absolute_tolerance=atol, relative_tolerance=rtol)
    def reject(fn):
        try:
            actual = fn()
        except (ValueError, TypeError) as exc:
            return dict(exception=repr(exc))
        raise AssertionError("expected explicit rejection; actual=" + repr(actual))
    stdout = ""
    with tempfile.TemporaryDirectory(prefix="book1-916-") as tmp:
        Path(tmp, "tvm_engine.py").write_bytes(code)
        for label, argv in [
            ("exact demonstration and twelve embedded tests", ["tvm_engine.py"]),
            ("exact compilation", ["-m", "compileall", "-q", "tvm_engine.py"])
        ]:
            p = subprocess.run([sys.executable, "-B", *argv], cwd=tmp, capture_output=True, text=True, timeout=60)
            is_script = argv == ["tvm_engine.py"]
            suite_ok = (bool(re.search(r"Ran 12 tests", p.stderr))
                        and bool(re.search(r"^OK\s*$", p.stderr, re.M)))
            expected_output = suite_ok if is_script else not(p.stdout or p.stderr)
            commands.append(dict(label=label, argv=argv, returncode=p.returncode,
                                 stdout=p.stdout, stderr=p.stderr,
                                 passed=(p.returncode == 0 and expected_output)))
            if argv == ["tvm_engine.py"]:
                stdout = p.stdout
    module = types.ModuleType("exact_engine_916")
    sys.modules[module.__name__] = module
    try:
        exec(compile(code, str(args.source), "exec"), module.__dict__)
        m = module
        c = m.Convention
        with localcontext() as ctx:
            ctx.prec = 100
            fv = D(1000)*(D(201)/200)**24
            ear = (D(201)/200)**12-1
            dnpv = -D(1000)+D(400)*(D(150)/151)**12+D(500)*(D(150)/151)**24+D(300)*(D(150)/151)**36
        check("P1 monthly accumulation", lambda: close(m.future_value(1000,c(.06,12),2),fv))
        check("P2 effective annual", lambda: close(c(.06,12).effective_annual(),ear))
        check("P3 break-even NPV", lambda: close(m.report([(0,-1000),(1,1100)],c(.1))["npv"],0))
        check("P4 reverse annual rate", lambda: close(m.solve_rate(1000,1210,2),F(1,10)))
        check("P5 reverse years", lambda: close(m.solve_time(1000,1210,c(.1)),2))
        check("P6 invalid frequency", lambda: reject(lambda:c(.05,0)))
        def netting():
            r=m.report([(0,-100),(0,40),(0,60)],c(.07))
            assert r["event_count"] == 3
            assert [row["amount"] for row in r["cash_flows"]] == [-100,40,60]
            assert [row["event"] for row in r["cash_flows"]] == [1,2,3]
            return close(r["npv"],0)
        check("P7 separate rows and net",netting)
        csv_text="year,amount\n0,-1000\n1,400\n2,500\n3,300\n"
        (outdir/"example_cash_flows.csv").write_text(csv_text)
        def pipeline():
            parsed=m.parse_cashflow_csv(csv_text)
            assert parsed == [(0,-1000),(1,400),(2,500),(3,300)]
            result=m.report(parsed,c(.08,12))
            assert result["rate_convention"] == "nominal_annual"
            assert result["compounds_per_year"] == 12 and result["event_count"] == 4
            for row, (t,a) in zip(result["cash_flows"],parsed,strict=True):
                with localcontext() as ctx:
                    ctx.prec=100
                    expected=D(a)*(D(150)/151)**(12*int(t))
                    discount=(D(150)/151)**(12*int(t))
                close(row["present_value"],expected)
                close(row["discount_factor"],discount)
                assert row["year"] == t and row["amount"] == a
            close(result["npv"],dnpv)
            assert math.isclose(math.fsum(row["present_value"] for row in result["cash_flows"]),result["npv"],abs_tol=1e-10)
            encoded=json.dumps(result,allow_nan=False,indent=2)
            assert json.loads(encoded)["event_count"] == 4
            (outdir/"sample-report.json").write_text(encoded+"\n")
            return dict(npv=result["npv"],decimal_reference=str(dnpv))
        check("source CSV-report pipeline",pipeline)
        check("exact printed demo JSON",lambda:close(json.loads(stdout)["npv"],dnpv))
        check("empty input report",lambda:close(m.report(iter(()),c(.05))["npv"],0))
        check("no hidden cost",lambda:close(m.report([(1,110)],c(.1))["npv"],100))
        check("negative rate",lambda:close(m.future_value(100,c(-.1),2),81))
        check("continuous roundtrip",lambda:close(m.continuous_present_value(m.continuous_future_value(2500,.04,3),.04,3),2500))
        check("signed discrete roundtrip",lambda:close(m.present_value(m.future_value(-100,c(.05,12),2),c(.05,12),2),-100))
        def frozen_config():
            from dataclasses import FrozenInstanceError
            config=c(.05,12)
            try:
                config.rate=.06
            except FrozenInstanceError:
                return "mutation rejected"
            raise AssertionError("configuration was mutable")
        check("immutable configuration",frozen_config)
        def literal_zeros():
            parsed=m.parse_cashflow_csv("year,amount\n0,0\n-0,-0.0\n")
            assert parsed == [(0,0),(0,0)]
            return dict(events=parsed)
        check("literal CSV zeros stay valid",literal_zeros)
        with localcontext() as ctx:
            ctx.prec=100
            scaled_ref=D('1e-300')*D(1000).exp()
        check("small amount avoids intermediate factor overflow",
              lambda:close(m.continuous_future_value(1e-300,1000,1),scaled_ref,atol=0))
        for label,fn in [
            ("negative date",lambda:m.future_value(100,c(.05),-1)),
            ("zero rate indeterminate",lambda:m.solve_time(100,100,c(0))),
            ("zero rate impossible",lambda:m.solve_time(100,110,c(0))),
            ("missing CSV field",lambda:m.parse_cashflow_csv("year,amount\n0\n")),
            ("extra CSV field",lambda:m.parse_cashflow_csv("year,amount\n0,-100,unexpected\n")),
            ("CSV nonfinite",lambda:m.parse_cashflow_csv("year,amount\n0,nan\n")),
            ("F46 amount",lambda:m.future_value(F(1,10**400),c(.05),1)),
            ("F46 rate",lambda:c(F(1,10**400))),
            ("F46 horizon",lambda:m.future_value(100,c(.05),F(1,10**400))),
            ("CSV nonzero amount underflow",lambda:m.parse_cashflow_csv("year,amount\n0,1e-400\n")),
            ("CSV negative time underflow",lambda:m.parse_cashflow_csv("year,amount\n-1e-400,100\n")),
            ("F48 total-period overflow",lambda:m.solve_rate(1,2,1e308,12)),
            ("F48 inferred-rate underflow",lambda:m.solve_rate(1,math.nextafter(1.,2.),1e308)),
            ("F49 nonfinite nominal log factor",lambda:m.solve_time(100,50,c(-9e307,10**308))),
            ("F49 elapsed-time underflow",lambda:m.solve_time(1,math.nextafter(1.,0.),c(-8e307,10**308)))
        ]:
            check(label,lambda fn=fn:reject(fn))
        p=1e300
        up,down=math.nextafter(p,math.inf),math.nextafter(p,0.)
        for label,f,rate in [("increase",up,.05),("decline",down,-.05)]:
            with localcontext() as ctx:
                ctx.prec=100
                ratio=D.from_float(f)/D.from_float(p)
                tref=ratio.ln()/(1+D(str(rate))).ln()
                rref=ratio-1
            check("F49 nearby time "+label,lambda f=f,rate=rate,tref=tref:close(m.solve_time(p,f,c(rate)),tref,atol=0))
            check("F49 nearby rate "+label,lambda f=f,rref=rref:close(m.solve_rate(p,f,1),rref,atol=0))
        check("F49 opposed nearby target",lambda:reject(lambda:m.solve_time(p,up,c(-.05))))
    except Exception as exc:
        checks.append(dict(label="source import or harness setup",passed=False,exception=repr(exc)))
    finally:
        sys.modules.pop(module.__name__,None)
    result=dict(python=platform.python_version(),platform=platform.platform(),
                source=str(args.source),source_sha256=hashlib.sha256(raw).hexdigest(),
                listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
                section_workflow_records=1,local_prompt_records=8,
                conceptual_only_prompts=[8],historical_unique_methods_added=0,
                existing_methods_expected=12,independent_acceptance=False)
    (outdir/"results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(str(outdir))
    return int(not all(x["passed"] for x in commands+checks))
if __name__=="__main__":
    raise SystemExit(main())
