"""Extract exact Section 1.12 program and insert three additional menu operations."""
from pathlib import Path
import ast
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
BOOK = HERE.parents[1]
SOURCE = BOOK / 'chapter-01/1.12-chapter-project-basic-financial-calculator.md'


def build():
    text = SOURCE.read_text()
    blocks = re.findall(r'^```python\n(.*?)^```', text, re.M | re.S)
    selected = [(i, b) for i,b in enumerate(blocks, 1) if 'BASIC FINANCIAL CALCULATOR' in b]
    assert len(selected) == 1
    index, original = selected[0]
    menu = 'choice = input("Select calculation: ").strip()'
    fallback = '    else:\n        print("Invalid calculator selection.")'
    assert original.count(menu) == original.count(fallback) == 1
    branches = '''    elif choice == "7":
        result = present_value(input("Future receipt (USD): "), input("Effective rate per period (%): "), input("Whole periods: "))
        print(f"Present Value: USD {money(result):,.2f}")
    elif choice == "8":
        result = discount_amount(input("Original price (USD): "), input("Final price (USD): "))
        print(f"Discount Amount: USD {money(result):,.2f}")
    elif choice == "9":
        rate, points = basis_points(input("Basis points (signed): "))
        print(f"Decimal rate: {rate:f}")
        print(f"Percentage points: {points:f}")
'''
    extended = 'from reference import present_value, discount_amount, basis_points, money\n' + original.replace(menu, 'print("7. Present Value")\nprint("8. Discount Amount")\nprint("9. Basis-Point Conversion")\n'+menu).replace(fallback,branches+fallback)
    # AST proof: original six calculation branches remain structurally identical.
    old_try=next(n for n in ast.parse(original).body if isinstance(n,ast.Try))
    new_try=next(n for n in ast.parse(extended).body if isinstance(n,ast.Try))
    old,new=old_try.body[0],new_try.body[0]
    for i in range(6):
        assert ast.dump(old.test)==ast.dump(new.test)
        assert [ast.dump(n) for n in old.body]==[ast.dump(n) for n in new.body]
        if i<5: old,new=old.orelse[0],new.orelse[0]
    (HERE/'extended_calculator.py').write_text(extended)
    (HERE/'assembly.json').write_text(json.dumps(dict(source=str(SOURCE.relative_to(BOOK)),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),python_fence_index=index,original_code_sha256=hashlib.sha256(original.encode()).hexdigest(),original_six_branches_ast_unchanged=True,extended_code_sha256=hashlib.sha256(extended.encode()).hexdigest()),indent=2)+'\n')

if __name__=='__main__': build()
