"""Conservative per-fence selection ledger, not line/branch coverage."""
import ast,collections,hashlib,json,pathlib,re,subprocess,sys
from markdown_it import MarkdownIt
repo=pathlib.Path(sys.argv[1]).resolve();root=repo/'books/book-01-python-foundations-for-financial-mathematics';out=pathlib.Path(sys.argv[2]);out.mkdir(exist_ok=True);parser=MarkdownIt()
def blocks(text):return [t for t in parser.parse(text) if t.type=='fence' and t.info.strip() in ('python','py','python3')]
def literal(path,name):
 tree=ast.parse(path.read_text())
 return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
qa=root/'qa'; snapshots={}
for ch in range(1,22):
 d=f'chapter-{ch:02}-runtime' if ch<19 else 'chapters-19-20-runtime' if ch<21 else 'initial-2026-10-27'
 p=qa/d/'README.md'; commit=subprocess.check_output(['git','log','--format=%H','--diff-filter=A','--',str(p.relative_to(repo))],cwd=repo,text=True).splitlines()[0];snapshots[ch]={'evidence':str(p.relative_to(root)),'publication_commit':commit}
# Explicit index selections preserved in structured early-chapter evidence.
selected={}
for ch in [1,2,3]:
 data=json.loads((qa/f'chapter-{ch:02}-runtime/results.json').read_text())
 for row in data.get('example_groups',data.get('results',[])):
  selected[(ch,row['file'])]=set(row.get('selected_python_block_indices',[]))
 if ch==1:
  for row in data['interactive_programs']: selected.setdefault((ch,row['file']),set()).add(row['python_block_index'])
 if ch==2:
  # All controlled analyzer cases are based on its first listing.
  f=next((root/'chapter-02').glob('2.12-*.md'));selected[(2,f.name)]={0}
config5=literal(qa/'chapter-05-runtime/run_reference_checks.py','config')
current_results=json.loads(pathlib.Path(sys.argv[3]).read_text());new={}
for r in current_results['results']:
 if r['status']!='PASS':raise ValueError('Unpassed new workflow')
 for s in r['sources']:new.setdefault((s['source'],s['python_block_index']),[]).append((r['workflow'],s['code_sha256']))
rows=[];labs=[];manifest=[]
for f in sorted(root.glob('chapter-*/**/*.md')):
 rel=str(f.relative_to(root));ch=int(rel.split('/')[0].split('-')[1]);raw=f.read_bytes();text=raw.decode();b=blocks(text);manifest.append({'path':rel,'sha256':hashlib.sha256(raw).hexdigest()})
 try:oldtext=subprocess.check_output(['git','show',snapshots[ch]['publication_commit']+':'+str(f.relative_to(repo))],cwd=repo,text=True,stderr=subprocess.DEVNULL);oldblocks=blocks(oldtext)
 except subprocess.CalledProcessError:oldblocks=[]
 n=int(f.name.split('.')[1][:2]) if re.match(r'\d+\.\d+',f.name) else 0
 choices=set()
 if ch<=3: choices=selected.get((ch,str(f.relative_to(root/f'chapter-{ch:02}'))),set())
 elif ch==4:
  choices={i for i,t in enumerate(b) if 'unittest' in t.content and '__main__' in t.content}
  if n==13: choices.add(1)
 elif ch==5:
  if n in config5:choices=set(config5[n]['files'].values())
  elif n==13 and 'solutions/' in rel:choices={0}
 elif 6<=ch<=8:
  suites=[i for i,t in enumerate(b) if 'unittest' in t.content and '__main__' in t.content]
  if suites:
   i=suites[0];choices.add(i)
   if i: choices.add(i-1)
 elif 9<=ch<=20:
  choices={i for i,t in enumerate(b) if 'unittest' in t.content and '__main__' in t.content}
  if ch==17 and n==14:choices={0,1}
  if ch in (17,18,19) and n==15:choices={0}
  if ch==20 and n==15:choices={0,1,3}
 elif ch==21:
  if n in (1,2,4,16):choices={0,1}
  elif 5<=n<=14:
   choices={0}|{i for i,t in enumerate(b) if 'unittest' in t.content and 'class ' in t.content}
   if n==14:choices.add(1) # Earlier __init__ listings overwritten by assembly, not credited.
  elif n in (15,17,18):choices={i for i,t in enumerate(b) if 'unittest' in t.content and 'class ' in t.content}
  if n==17:choices.add(0)
 for i,t in enumerate(b):
  digest=hashlib.sha256(t.content.encode()).hexdigest();prior=i in choices; unchanged=prior and i<len(oldblocks) and t.content==oldblocks[i].content
  new_records=new.get((rel,i),[])
  if any(h!=digest for _,h in new_records):raise ValueError('New run payload mismatch: '+rel)
  newruns=[name for name,_ in new_records]
  context=rel.endswith('2.10-break-continue-and-loop-control.md') and t.map[0]+1 in (16,81)
  state='PASS_NEW_SCOPED_WORKFLOW' if newruns else 'HISTORICAL_SELECTION_UNCHANGED' if unchanged else 'PRIOR_SELECTION_REQUIRES_RECONCILIATION' if prior else 'CONTEXT_FRAGMENT' if context else 'NO_EXACT_EXECUTION_MAPPING'
  rows.append({'path':rel,'python_block_index':i,'line':t.map[0]+1,'code_sha256':digest,'state':state,'prior_selection':prior,'same_payload_at_evidence_publication':unchanged if prior else None,'historical_evidence':snapshots[ch] if prior else None,'new_workflows':newruns})
 lines=text.splitlines()
 for i,line in enumerate(lines,1):
  if re.match(r'^#{1,6}\s',line) and re.search(r'\b(lab|hands.on|worked exercises|exercises and applied problems)\b',line,re.I):labs.append({'path':rel,'line':i,'heading':line.lstrip('# ').strip(),'status':'STEP_AND_ANSWER_REVIEW_PENDING','note':'Fence execution is not proof that every prose step or worked answer has been independently validated.'})
summary={'source_revision':'a4aebd6d937a97dd5ed3f6b6cbb947fb5f58e76f','documents':len(manifest),'python_fences':len(rows),'states':dict(collections.Counter(r['state'] for r in rows)),'lab_or_exercise_heading_candidates':len(labs),'per_chapter':{f'{ch:02}':dict(collections.Counter(r['state'] for r in rows if r['path'].startswith(f'chapter-{ch:02}/'))) for ch in range(1,22)}}
if len({(r['path'],r['python_block_index']) for r in rows})!=len(rows):raise ValueError('Duplicate fence identity')
if len([r for r in rows if r['new_workflows']])!=len(new):raise ValueError('Unmapped new workflow source')
for name,data in [('coverage-ledger.json',rows),('lab-review-queue.json',labs),('coverage-summary.json',summary),('source-manifest.json',manifest)]: (out/name).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(summary,indent=2))
