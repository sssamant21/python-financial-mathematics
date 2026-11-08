# V-123 — Signed cash-flow aggregate derivatives

Candidate based on`ade7da5b8c157c23f8b3be32c06af57add8602f4`; exact changed/source/dependency blobs are in the [raw evidence](chapter-08-cash-flow-derivatives-followup.json). Publication verification pins the executable commit. Earlier [five-probe baseline](chapter-08-cash-flow-derivatives-baseline.md) remains unchanged. [Expanded baseline](chapter-08-cash-flow-derivatives-expanded-baseline.json) retains21 mismatches; byte-identical repeat is embedded in the follow-up. These are predicate mismatches, not distinct defects or COV closure counts.

All63 selected predicates pass: independent complete signed aggregate value/first/second references at Decimal1600/2200 digits, permutations/order controls, exact same-exponent cancellation, extreme-growth tiny payments, lost subnormal derivatives, negative underflow signs, empty/zero-horizon cases, true final overflow, one-shot iteration, rate-first/empty validation, signed-payment domains and independence from the nonnegative single-payment helper. Seven scoped Python files compiled and all five scoped scripts passed, with exact candidate blob hashes verified before/after. The four preceding Section8.6 reference/curvature/PV/shock suites are included. Actual platform/commands/timings/stdout hashes retained.

[Superseded observer manifest and collection correction](chapter-08-cash-flow-derivatives-observer-notes.md) are retained separately. Final evidence uses verified real Git-object hashes.

## Model and independent expectations

For signed flows(Ci,ti), nonnegative ti and represented finite continuous rate r:

- value=sum(Ci exp(−r ti));
- first=sum(−ti Ci exp(−r ti));
- second=sum(ti² Ci exp(−r ti)).

The independent oracle directly expands each complete Decimal term from exact binary64 inputs and adds signed terms at1600/2200 digits. Final float/sign observations agree. Implementation instead groups rational coefficients by exact represented exponent, sums signed relative-exponent terms and applies a log-amplitude before one final float conversion. Source and oracle share Decimal as an arithmetic backend, not independent library certification. rtol4e-15,atol0; zeros, subnormals and exceptions exact.

Original source returns NaN derivatives for equal/opposite large same-horizon flows, overflows one permutation of a finite signed zero-horizon sum, raises premature exponential overflow for tiny signed payments at large growth horizons, and loses nonzero subnormal derivatives beside a zero-rounded value. Correction preserves these finite aggregate results and rejects true nonfinite aggregate triples with ValueError. Numeric sign policies are explicit: exact cancellation and empty sums are+0; nonzero negative underflow is−0. Finite underflow is permitted in this Book2 API, not conflated with Book1 reportability policies.

The1600-digit grouped calculation is a scoped teaching implementation, not an arbitrary-length/adversarial cancellation or correctly-rounded proof. Resource/bit-length/collection-size limits remain unreviewed. Input validation happens while consuming flows once; final aggregate calculation follows validation. Signed payments are preserved. No nonnegative single-payment helper is called. Other local polynomial/sampled-second-difference functions remain separate obligations, not covered by these passes.

## Reproduce

From chapter-08/code run`python check_section_06_cash_flows.py`. It emits per-predicate JSON and exits1 against the recorded baseline,0 against the corrected source. For exact scoped reproduction from repository root, use the raw manifest and git:

```python
from pathlib import Path
import hashlib,json,os,py_compile,subprocess,sys,tempfile
book=Path('books/book-02-mathematical-foundations-for-finance-with-python')
e=json.loads((book/'validation/chapter-08-cash-flow-derivatives-followup.json').read_text())
assert __debug__
env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
def get(rev,path,sha):
    raw=subprocess.check_output(['git','show',rev+':'+path]) if rev else subprocess.check_output(['git','cat-file','blob',sha])
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()==sha
    return raw
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)
    for x in e['scoped']['scope_manifest']:
        (p/Path(x['path']).name).write_bytes(get(e.get('executable_source_revision'),x['path'],x['sha']))
    for f in sorted(p.glob('*.py')):
        py_compile.compile(str(f),doraise=True)
        if f.name.startswith('check_'):
            subprocess.run([sys.executable,f.name],cwd=p,env=env,check=True,timeout=60)
    name='books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_06.py'
    (p/'section_8_06.py').write_bytes(get(e['baseline_revision'],name,e['baseline_source_blob']))
    for cache in p.glob('__pycache__/section_8_06.*'):cache.unlink()
    for _ in range(2):
        r=subprocess.run([sys.executable,'check_section_06_cash_flows.py'],cwd=p,env=env,capture_output=True,text=True,timeout=60)
        assert r.returncode==1 and json.loads(r.stdout)==e['baseline']
```

Next substantive item: Section8.6 polynomial/derivative-coefficient complete-expression range and output contracts, with independent exact polynomial expectations; then sampled-second differences. No new full-book pass is implied by this scoped run. Accumulated V-122/V-123 code/check additions warrant the following pinned full refresh. Thirty-five selected categories remain partially addressed, none closed; COV-49/51 and independent reviewer/platform/release/canonical obligations remain open.
