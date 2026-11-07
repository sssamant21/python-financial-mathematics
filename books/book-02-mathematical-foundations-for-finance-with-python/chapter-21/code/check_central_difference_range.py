"""Independent complete-stencil references for the Section 21.4 entry point."""
from decimal import Context, Decimal as D, localcontext
import json
import math
from pathlib import Path
import sys
from unittest.mock import patch
if len(sys.argv) == 2:
    sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import section_21_04 as lab


def oracle(a, r, t, h):
    # Use the actual represented perturbations and the stated 2*h denominator.
    up, down = r+h, r-h
    if a == 0 or t == 0:
        return 0.
    with localcontext(Context(prec=2100)):
        high = D(a)*(-D(up)*D(t)).exp()
        low = D(a)*(-D(down)*D(t)).exp()
        answer = float((high-low)/(2*D(h)))
    return answer if math.isfinite(answer) else "OverflowError"


def check():
    rows = []
    def record(name, args, expected):
        try:
            actual = lab.central_difference(*args)
        except Exception as exc:
            actual = type(exc).__name__
        if isinstance(expected, float):
            passed = isinstance(actual, float) and (
                actual == expected if expected == 0 or abs(expected) < sys.float_info.min
                else math.isclose(actual, expected, rel_tol=5e-14, abs_tol=0.))
        else:
            passed = actual == expected
        rows.append(dict(case=name, inputs=args, expected=expected, actual=actual, passed=passed))
    M, tiny = sys.float_info.max, math.ulp(0.)
    fixtures = [
        ("finite despite PV overflow", (M, 0., .5, .5)),
        ("signed finite despite PV overflow", (-M, 0., .5, .5)),
        ("complete large denominator", (1., 0., 1e-308, 1e308)),
        ("complete large denominator scaled", (100., 0., 1e-308, 1e308)),
        ("zero horizon with large denominator", (M, 0., 0., 1e308)),
        ("zero amount with large denominator", (0., 0., 1., 1e308)),
        ("lost subtraction at tiny horizon", (100., 0., tiny, .5)),
        ("lost subtraction at tiny step", (100., 0., 2., tiny)),
        ("tiny step with signed amount", (-100., 0., 2., tiny)),
        ("both PVs underflow but stencil finite", (1., 1., 750., 1e-15)),
        ("huge exponent zero identity", (0., 0., M, M)),
        ("underflow to zero", (1., 10., 1000., .01)),
        ("ordinary diagnostic", (100., 0., 2., 1e-5)),
        ("rounded asymmetric perturbations", (100., 1., 2., math.ulp(1.))),
        ("true final overflow", (M, 0., 2., .5)),
    ]
    for name,args in fixtures:
        expected = 0. if args[0]==0 or args[2]==0 else oracle(*args)
        record(name,args,expected)
    for name,args,exc in [
        ("collapsed positive step",(100.,1.,2.,1e-30),"ValueError"),
        ("nonfinite perturbation",(1.,M,1.,M),"ValueError"),
        ("coarse positive exponent",(1.,-1e308,1.,1e292),"OverflowError"),
        ("zero identity still checks perturbations",(0.,1e308,1.,1e308),"ValueError"),
        ("zero step",(1.,0.,1.,0.),"ValueError"),
        ("negative horizon",(1.,0.,-1.,1.),"ValueError"),
        ("bool amount",(True,0.,1.,1.),"TypeError"),
    ]:
        record(name,args,exc)
    record("coarse negative exponent", (1.,1e308,1.,1e292), 0.)
    # Observe the actual report consumer when run alongside the complete chapter.
    try:
        import section_21_09 as integrated
    except ModuleNotFoundError:
        pass
    else:
        calls=[]
        def observed(*args):
            calls.append(args)
            return lab.central_difference(*args)
        with patch.object(integrated, "central_difference", observed):
            report=integrated.build_report()
        diagnostic=report["sensitivity"]["finite_difference"]
        want=oracle(100.,0.,2.,1e-5)
        expected=[[(100,0,2,1e-5)],True,True,True,True]
        actual=[calls,math.isclose(diagnostic["estimate"],want,rel_tol=5e-14),
                diagnostic["signed_error"]==diagnostic["estimate"]+200,
                diagnostic["absolute_error"]==abs(diagnostic["signed_error"]),
                report["validation_execution"]=="not run" and report["approval"]=="pending"]
        rows.append(dict(case="actual integrated diagnostic",expected=expected,
                         actual=actual,passed=expected==actual))
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
