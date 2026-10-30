import hashlib

from decimal import Decimal
from importlib.metadata import version
from pathlib import Path
import json, sys
import book1_report_demo
import book1_unit_demo

assert Path(book1_report_demo.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
assert Path(book1_unit_demo.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
input_raw=Path(sys.argv[1]).read_bytes()
input_text=input_raw.decode('utf-8')
label, quantity = book1_report_demo.labeled_quantity(Decimal(input_text))
assert label == "instrument_units"
assert str(quantity) == "12.50"
assert book1_report_demo.labeled_quantity(Decimal("0")) == ("instrument_units", Decimal("0"))
for bad in (None, True, 1, 1.5, "1"):
    try:
        book1_report_demo.labeled_quantity(bad)
    except TypeError:
        pass
    else:
        raise AssertionError("invalid type accepted")
for token in ("NaN", "sNaN", "Infinity", "-Infinity", "-1"):
    try:
        book1_report_demo.labeled_quantity(Decimal(token))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid domain accepted")
print(json.dumps({
    "versions": {"book1-report-demo": version("book1-report-demo"),
                 "book1-unit-demo": version("book1-unit-demo")},
    "input": input_text, "input_sha256":hashlib.sha256(input_raw).hexdigest(), "application_source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "output": [label, str(quantity)],
}, sort_keys=True))
