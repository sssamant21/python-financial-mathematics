"""Check declared implemented contracts against actual callables and returned shapes."""
import inspect
import json
from pathlib import Path
import sys
if len(sys.argv) == 2:
    sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import section_21_02 as catalog
import section_21_03 as cash
import section_21_04 as sensitivity
import section_21_05 as linear
import section_21_06 as allocation
import section_21_07 as account
import section_21_09 as reporting


def matches(entry, function, result):
    signature = str(inspect.signature(function))
    if entry["signature"] != signature:
        return False
    kind = entry["return_kind"]
    if kind == "scalar":
        return type(result) is float and entry["fields"] == []
    if kind == "pair":
        return type(result) is tuple and len(result) == 2 and entry["fields"] == []
    return kind == "mapping" and type(result) is dict and sorted(result) == sorted(entry["fields"])


def check():
    rows = []
    def record(name, expected, operation):
        try:
            actual = operation()
        except Exception as exc:
            actual = type(exc).__name__
        rows.append(dict(case=name,expected=expected,actual=actual,passed=expected==actual))
    cases = [
        ("cash_flow", cash.present_value, ([(3., 0.)], 0., "continuous"), {}),
        ("sensitivity", sensitivity.derivatives, (3.,0.,2.), {}),
        ("sensitivity", sensitivity.central_difference, (3.,0.,2.,.01), {}),
        ("linear_algebra", linear.solve_2x2, ([[1.,0.],[0.,1.]],[2.,3.]), {"threshold":0.}),
        ("optimization", allocation.solve, (.6,.3), {"tolerance":0.}),
        ("continuous_time", account.scenario_report, (3.,0.,2.,1.), {}),
        ("reporting", reporting.build_report, (), {}),
    ]
    implemented = getattr(catalog, "implemented_catalog", None)
    inventory = implemented() if implemented else {}
    record("draft remains six independent design entries", 6, lambda: len(catalog.interface_catalog()))
    record("implemented inventory has all draft areas", sorted(catalog.interface_catalog()),
           lambda: sorted(inventory))
    for area, fn, args, kwargs in cases:
        result = fn(*args, **kwargs)
        key = fn.__name__
        def mapped(area=area,key=key,fn=fn,result=result):
            entry = next(e for e in inventory[area]["callables"] if e["name"]==key)
            return (entry["module"] == fn.__module__ and
                    bool(inventory[area]["limits"]) and matches(entry,fn,result))
        record("actual signature and return shape: "+key, True, mapped)
        # Execute complete keyword call forms, not just inspect.bind.
        bound = inspect.signature(fn).bind(*args, **kwargs)
        record("keyword form accepted: "+key, True,
               lambda fn=fn,bound=bound,result=result: fn(**bound.arguments) == result)

    def rejected(fn,*args,**kwargs):
        try:
            fn(*args,**kwargs)
        except Exception as exc:
            return type(exc).__name__
        return "returned"
    record("threshold is keyword-only", "TypeError",
           lambda: rejected(linear.solve_2x2,[[1.,0.],[0.,1.]],[2.,3.],0.))
    record("report accepts no scenario arguments", "TypeError",
           lambda: rejected(reporting.build_report,{}))
    record("cash convention is required", "TypeError",
           lambda: rejected(cash.present_value,[(1.,0.)],0.))
    record("unsupported convention rejects", "ValueError",
           lambda: rejected(cash.present_value,[(1.,0.)],0.,"unknown"))
    record("generic objective is not an accepted solve parameter", "TypeError",
           lambda: rejected(allocation.solve,objective=lambda x:x,constraints=[]))
    record("account rejects events keyword", "TypeError",
           lambda: rejected(account.scenario_report,3.,0.,2.,1.,events=[]))
    if implemented:
        before = implemented()
        changed = implemented()
        changed["reporting"]["callables"][0]["fields"].clear()
        changed["cash_flow"]["limits"].append("mutation")
        record("implemented map is copied deeply", before, implemented)
        actual_report = reporting.build_report()
        entry = before["reporting"]["callables"][0]
        record("checker detects wrong signature", False,
               lambda: matches({**entry,"signature":"(scenario)"},reporting.build_report,actual_report))
        record("checker detects missing report field", False,
               lambda: matches(entry,reporting.build_report,{k:v for k,v in actual_report.items() if k!="approval"}))
    else:
        for name in ("implemented map is copied deeply","checker detects wrong signature",
                     "checker detects missing report field"):
            record(name,"implemented mapping available",lambda:"missing")
    report = reporting.build_report()
    record("pending status preserved", ["not run","pending","pending"],
           lambda:[report[k] for k in ("validation_execution","independent_review","approval")])
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
