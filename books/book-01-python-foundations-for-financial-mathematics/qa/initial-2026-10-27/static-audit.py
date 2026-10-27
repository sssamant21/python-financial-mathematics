import ast, pathlib, re, json, urllib.parse, collections
root=pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics')
paths=list(root.rglob('*.md'))
issues=[]; blocks=0; parsed=0; broken=[]; external=0; fences=0
for p in paths:
 s=p.read_text(encoding='utf-8')
 # Capture fenced Python examples. Syntax errors can be illustrative fragments.
 pat=re.compile(r'(?ms)^([`~]{3,})\s*python[^\n]*\n(.*?)^\1\s*$')
 for m in pat.finditer(s):
  blocks+=1
  try: ast.parse(m.group(2));parsed+=1
  except SyntaxError as e:issues.append({'path':str(p.relative_to(root)),'line':s.count('\n',0,m.start())+1,'error':e.msg,'code_line':e.lineno})
 for m in re.finditer(r'(?<!!)\[[^\]]*\]\(([^\s)]+)',s):
  dest=m.group(1).split('#')[0].split('?')[0]
  if not dest or '://' in dest or dest.startswith(('mailto:','#')): external+=1;continue
  target=(p.parent / urllib.parse.unquote(dest)).resolve()
  if not target.exists() and str(target).startswith(str(root.resolve())):broken.append({'path':str(p.relative_to(root)),'target':dest})
 # Count only fences at line start, a heuristic; matching nested fences require review.
 fences+=len(re.findall(r'(?m)^\s*(?:`{3,}|~{3,})',s))
result={'files':len(paths),'python_blocks':blocks,'python_parse_ok':parsed,'python_syntax_review':issues,'missing_local_targets':broken,'external_or_anchor_links':external,'fence_lines':fences}
pathlib.Path('/tmp/book1_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'files':len(paths),'python_blocks':blocks,'parse_ok':parsed,'syntax_review':len(issues),'missing_local_targets':len(broken),'examples':issues[:12],'missing_examples':broken[:15]},indent=2))
