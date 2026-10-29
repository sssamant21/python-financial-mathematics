"""Close later source-selection gaps; do not infer statement/branch coverage."""
import collections,hashlib,json,pathlib,sys
from markdown_it import MarkdownIt
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True);parser=MarkdownIt()
base=json.loads((root/'qa/early-examples-2026-10-28/current-coverage-ledger.json').read_text());runs=json.loads(pathlib.Path(sys.argv[3]).read_text());hits={}
for r in runs['results']:
 if r['status']!='PASS':raise ValueError('Unpassed later workflow')
 for s in r['sources']:
  if s['role']=='target':hits.setdefault((s['path'],s['python_block_index']),[]).append((r['workflow'],s['code_sha256']))
queue={(r['path'],r['python_block_index']) for r in base if r['state']=='NO_EXACT_EXECUTION_MAPPING'}
assert len(queue)==169 and queue==set(hits)
rows=[];new=[]
for old in base:
 row=dict(old);key=(row['path'],row['python_block_index']);f=root/row['path'];b=[t for t in parser.parse(f.read_text()) if t.type=='fence' and t.info.strip() in ('python','py','python3')];code=b[row['python_block_index']].content;h=hashlib.sha256(code.encode()).hexdigest();assert h==row['code_sha256'],key
 if key in hits:
  assert all(value==h for _,value in hits[key]);row.update(state='PASS_SCOPED_LATER_RUNTIME',later_workflows=[n for n,_ in hits[key]],disposition='Included unchanged in the explicitly configured passing workflow. Source selection is not full branch/input/financial validation.',evidence='qa/later-examples-2026-10-28/README.md');new.append(row)
 rows.append(row)
assert len(rows)==1160 and not any(r['state']=='NO_EXACT_EXECUTION_MAPPING' for r in rows)
summary={'source_revision':sys.argv[4],'runtime_workflows':len(runs['results']),'newly_mapped_fences':len(new),'remaining_no_exact_execution_mapping':0,'total_fences':len(rows),'states':dict(collections.Counter(r['state'] for r in rows)),'per_chapter':{f'{ch:02}':dict(collections.Counter(r['state'] for r in rows if r['path'].startswith(f'chapter-{ch:02}/'))) for ch in range(1,22)}}
for name,data in [('current-coverage-ledger.json',rows),('later-dispositions.json',new),('coverage-summary.json',summary)]: (out/name).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(summary,indent=2))
