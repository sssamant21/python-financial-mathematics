"""Inventory manuscript Python fences; compile without executing their contents."""
import ast, collections, hashlib, json, pathlib, subprocess, sys
from markdown_it import MarkdownIt
root=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
parser=MarkdownIt('commonmark'); records=[]; imports=collections.defaultdict(list); manifest=[]
for p in sorted(root.glob('chapter-*/**/*.md')):
 raw=p.read_bytes(); rel=p.relative_to(root).as_posix(); manifest.append({'path':rel,'sha256':hashlib.sha256(raw).hexdigest()})
 for t in parser.parse(raw.decode()):
  if t.type!='fence' or t.info.strip().split(' ')[0].lower() not in ('python','py','python3'): continue
  code=t.content; ident=f'{rel}:{t.map[0]+1}'; rec={'id':ident,'sha256':hashlib.sha256(code.encode()).hexdigest(),'code':code}
  try:
   tree=ast.parse(code,filename=ident); compile(tree,ident,'exec'); rec['compile']='PASS'
   rec['kind']='module_or_script_candidate' if any(isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) for x in tree.body) else 'illustrative_or_context_dependent'
   rec['has_main_guard']=any(isinstance(x,ast.If) and '__name__' in ast.unparse(x.test) for x in tree.body)
   rec['contains_ellipsis']=any(isinstance(x,ast.Constant) and x.value is Ellipsis for x in ast.walk(tree))
   roots=set()
   for x in ast.walk(tree):
    if isinstance(x,ast.Import): roots.update(a.name.split('.')[0] for a in x.names)
    if isinstance(x,ast.ImportFrom) and x.module: roots.add(x.module.split('.')[0])
   rec['import_roots']=sorted(roots)
   for name in roots: imports[name].append(ident)
  except SyntaxError as e: rec.update(compile='FAIL',error=str(e),kind='unparsed_fragment_or_error')
  records.append(rec)
(out/'blocks-for-compilation.json').write_text(json.dumps(records,indent=2)+'\n')
(out/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'import-inventory.json').write_text(json.dumps(dict(sorted(imports.items())),indent=2)+'\n')
summary={'documents':len(manifest),'python_fences':len(records),'compile_counts':dict(collections.Counter(r['compile'] for r in records)),'classification':dict(collections.Counter(r['kind'] for r in records)),'import_roots':len(imports),'failures':[r['id'] for r in records if r['compile']=='FAIL']}
(out/'inventory-summary.json').write_text(json.dumps(summary,indent=2)+'\n'); print(json.dumps(summary))
