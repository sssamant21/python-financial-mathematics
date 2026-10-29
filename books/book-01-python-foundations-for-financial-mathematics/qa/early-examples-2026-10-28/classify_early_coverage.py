"""Account for the 430 initial Chapter 1–3 mapping gaps without implying coverage."""
import ast,collections,hashlib,json,pathlib,sys
from markdown_it import MarkdownIt
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
base=json.loads((root/'qa/coverage-and-labs-2026-10-28/coverage-ledger.json').read_text());runs=json.loads(pathlib.Path(sys.argv[3]).read_text());typing=json.loads(pathlib.Path(sys.argv[4]).read_text());parser=MarkdownIt();hits={}
for r in runs['results']:
 if r['status']!='PASS':raise ValueError('Unpassed workflow')
 for s in r['sources']:
  if s['role']=='target':hits.setdefault((s['path'],s['python_block_index']),[]).append((r['workflow'],s['code_sha256']))
assert all(r['status']=='PASS' for r in typing['results'])
review=[];updated=[]
for old in base:
 row=dict(old);key=(row['path'],row['python_block_index'])
 if row['state']=='NO_EXACT_EXECUTION_MAPPING' and row['path'].startswith(('chapter-01/','chapter-02/','chapter-03/')):
  f=root/row['path'];b=[t for t in parser.parse(f.read_text()) if t.type=='fence' and t.info.strip() in ('python','py','python3')];code=b[row['python_block_index']].content;digest=hashlib.sha256(code.encode()).hexdigest();assert digest==row['code_sha256']
  if key in hits:
   assert all(h==digest for _,h in hits[key]);state='PASS_SCOPED_RUNTIME';note='Included unchanged in explicitly configured runtime assembly; source inclusion is not full line/branch or numerical-domain coverage.';workflows=[n for n,_ in hits[key]]
  elif row['path']==typing['source'] and row['python_block_index']==10:
   assert digest==typing['code_hashes']['10'];state='PASS_EXPECTED_STATIC_DIAGNOSTICS';note='Mypy reports the three expected argument-type errors; this deliberately invalid file was not run as an ordinary program.';workflows=['invalid-calls']
  elif 'eval(input(' in code:
   state='NOT_EXECUTED_INPUT_EVAL_ANTIPATTERN';note='The manuscript explicitly warns against this input-parsing pattern; static disposition only. No untrusted expression was evaluated.';workflows=[]
  else:
   tree=ast.parse(code)
   assert any(isinstance(n,ast.Constant) and n.value is Ellipsis for n in ast.walk(tree)) or any(isinstance(n,ast.Name) and n.id=='statement' for n in ast.walk(tree)),key
   state='PLACEHOLDER_NOT_RUN';note='Generic statement/Ellipsis body; not a complete executable financial algorithm. Existing V04 compilation does not establish loop termination or runtime behavior.';workflows=[]
  row.update(state=state,early_workflows=workflows,disposition=note,evidence='qa/early-examples-2026-10-28/README.md');review.append(row)
 updated.append(row)
assert len(review)==430 and len(hits)==405 and len(updated)==1160
summary={'source_revision':sys.argv[5],'reviewed_initial_gaps':len(review),'runtime_workflows':len(runs['results']),'gap_dispositions':dict(collections.Counter(r['state'] for r in review)),'remaining_no_exact_execution_mapping':sum(r['state']=='NO_EXACT_EXECUTION_MAPPING' for r in updated),'total_fences':len(updated),'per_chapter':{f'{ch:02}':dict(collections.Counter(r['state'] for r in updated if r['path'].startswith(f'chapter-{ch:02}/'))) for ch in range(1,22)}}
for name,data in [('early-dispositions.json',review),('current-coverage-ledger.json',updated),('coverage-summary.json',summary)]: (out/name).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(summary,indent=2))
