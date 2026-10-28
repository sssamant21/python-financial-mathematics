"""Exercise parser/anchor/link edge cases in temporary fixture documents."""
import collections,json,pathlib,shutil,subprocess,sys
repo=pathlib.Path(sys.argv[1]).resolve();audit=pathlib.Path(sys.argv[2]).resolve();out=pathlib.Path(sys.argv[3]).resolve();slugger=sys.argv[4]
fixtures=repo/'books/book-01-python-foundations-for-financial-mathematics/qa/_audit-fixtures'
if fixtures.exists():raise SystemExit('fixture path already exists')
fixtures.mkdir();checks=[]
try:
 (fixtures/'README.md').write_text('''# Repeat
## Repeat
[duplicate](#repeat-1)
[reference][ok]
[unicode](space%20name.md#caf%C3%A9)
[parentheses](part(1).md#ok)
<a id="manual"></a>
[manual](#manual)
[bad-path](does-not-exist.md)
[bad-anchor](target.md#missing)
[visible][unknown]
other[0]["quantity"] is prose indexing.
`[not-a-link](inline-fake.md)`
```python
print("[not-a-link](code-fake.md)")
```
```math
[x](math-fake)
```
| Quantity | Value |
|---|---|
| P(A\\|B) | valid |
| P(A|B) | intentionally malformed |

[ok]: target.md#code-identifier
''')
 (fixtures/'target.md').write_text('# Code `identifier`\n')
 (fixtures/'space name.md').write_text('# Café\n')
 (fixtures/'part(1).md').write_text('# OK\n')
 (fixtures/'unclosed.md').write_text('```python\nprint(1)\n')
 (fixtures/'escaped.md').write_text('\\`\\`\\`python\nnot a real fence\n\\`\\`\\`\n')
 proc=subprocess.run([sys.executable,str(audit),str(repo),str(out),slugger],text=True,capture_output=True,timeout=120)
 (out/'selftest-command.log').write_text(proc.stdout+proc.stderr)
 findings=json.loads((out/'findings.json').read_text());own=[x for x in findings if '/_audit-fixtures/' in x['file']];kinds=collections.Counter(x['kind'] for x in own)
 expected={'missing_internal_target':1,'missing_internal_anchor':1,'table_column_mismatch':1,'unresolved_explicit_reference_review':1,'unclosed_fence':1,'escaped_fence_review':2}
 def check(name,condition):
  if not condition:raise AssertionError(name)
  checks.append({'check':name,'status':'PASS'})
 check('expected fixture finding counts',dict(kinds)==expected)
 check('intentional failures produce nonzero audit exit',proc.returncode==1)
 links=json.loads((out/'internal-links.json').read_text());ownlinks=[x for x in links if '/_audit-fixtures/' in x['file']]
 for label in ('duplicate','reference','unicode','parentheses','manual'):check(label+' target/anchor passes',any(x.get('label')==label and x['status']=='PASS' for x in ownlinks))
 check('fenced-code link ignored',not any('code-fake' in x['destination'] for x in ownlinks))
 check('inline-code link ignored',not any('inline-fake' in x['destination'] for x in ownlinks))
 check('native math-fence link ignored',not any('math-fake' in x['destination'] for x in ownlinks))
 check('dictionary indexing does not become unresolved-reference finding',not any('other[0]' in x.get('text','') for x in own))
 check('only unescaped table pipe is flagged',kinds['table_column_mismatch']==1)
 result={'status':'PASS','checks':checks,'fixture_findings':own}
 (out/'selftest-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks)},indent=2))
finally:shutil.rmtree(fixtures)
