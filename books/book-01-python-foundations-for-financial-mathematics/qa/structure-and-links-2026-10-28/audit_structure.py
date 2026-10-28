"""Audit locked Book 1 structure and explicit Markdown internal links.

Requires markdown-it-py 4.0.0, mdurl 0.1.2, Node and github-slugger 2.0.0.
Usage: python audit_structure.py REPO_ROOT OUTPUT_DIR GITHUB_SLUGGER_INDEX_JS
This is a parser-based scoped audit, not a full GitHub renderer certification.
"""
from __future__ import annotations
import collections,hashlib,json,pathlib,posixpath,re,subprocess,sys
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
from importlib.metadata import version
from markdown_it import MarkdownIt
ROOT=pathlib.Path(sys.argv[1]).resolve();OUT=pathlib.Path(sys.argv[2]).resolve();SLUGGER=pathlib.Path(sys.argv[3]).resolve();OUT.mkdir(parents=True,exist_ok=True)
if json.loads((SLUGGER.parent/'package.json').read_text())['version']!='2.0.0':raise SystemExit('github-slugger 2.0.0 required')
if version('markdown-it-py')!='4.0.0' or version('mdurl')!='0.1.2':raise SystemExit('pinned Markdown parser versions required')
BOOK='books/book-01-python-foundations-for-financial-mathematics';md=MarkdownIt('commonmark',{'html':True}).enable(['table','strikethrough']);findings=[];docs={};links=[];external=[];link_results=[]
def issue(kind,path,line,**details):findings.append({'kind':kind,'file':path,'line':line,**details})
def visible(tokens):
 result=''
 for t in tokens or []:
  if t.type in ('text','code_inline'):result+=t.content
  elif t.type in ('softbreak','hardbreak'):result+=' '
  elif t.type=='image':result+=visible(t.children) or t.content
 return result

def plain(text):return re.sub(r'\s+',' ',visible(md.parseInline(text)[0].children)).strip()
class HTMLBits(HTMLParser):
 def __init__(self):super().__init__();self.anchors=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for name in ('id','name'):
   if a.get(name):self.anchors.append(a[name])
  if tag=='a' and a.get('href') is not None:self.links.append(a['href'])
  if tag in ('img','source') and a.get('src') is not None:self.links.append(a['src'])

def count_cells(line):
 s=line.strip();parts=[];start=0
 for i,ch in enumerate(s):
  if ch=='|':
   j=i-1
   while j>=0 and s[j]=='\\':j-=1
   if (i-1-j)%2==0:parts.append(s[start:i]);start=i+1
 parts.append(s[start:])
 if s.startswith('|'):parts=parts[1:]
 if s.endswith('|') and not s.endswith('\\|'):parts=parts[:-1]
 return len(parts)

def parse_document(path):
 if path in docs:return docs[path]
 text=(ROOT/path).read_text(encoding='utf-8');env={};tokens=md.parse(text,env);lines=text.splitlines();headings=[];explicit=[];rows=[];table_rows=[];current_table=None;row=None;blocked=set();fences=0;tables=0
 for i,t in enumerate(tokens):
  if t.type in ('fence','code_block') and t.map:
   blocked.update(range(t.map[0],t.map[1]))
  if t.type=='fence':
   fences+=1;end=lines[t.map[1]-1] if t.map and t.map[1] else '';marker=t.markup[0]
   if not re.match(r'^\s*(?:>\s*)*'+re.escape(marker)+'{'+str(len(t.markup))+r',}\s*$',end):issue('unclosed_fence',path,t.map[0]+1,marker=t.markup)
  if t.type=='heading_open' and i+1<len(tokens):headings.append({'level':int(t.tag[1:]),'text':visible(tokens[i+1].children),'line':t.map[0]+1})
  if t.type in ('html_inline','html_block'):
   h=HTMLBits();h.feed(t.content);explicit+=h.anchors
   for dest in h.links:links.append({'file':path,'line':t.map[0]+1 if t.map else 1,'destination':dest,'syntax':'html'})
  if t.type=='inline':
   children=t.children or [];ln=t.map[0]+1 if t.map else 1
   for child_index,child in enumerate(children):
    if child.type=='link_open':
     closing=next((j for j in range(child_index+1,len(children)) if children[j].type=='link_close'),len(children))
     links.append({'file':path,'line':ln,'destination':child.attrGet('href') or '', 'syntax':'markdown','label':visible(children[child_index+1:closing])})
    elif child.type=='image':links.append({'file':path,'line':ln,'destination':child.attrGet('src') or '', 'syntax':'image'})
    elif child.type=='html_inline':
     h=HTMLBits();h.feed(child.content);explicit+=h.anchors
     for dest in h.links:links.append({'file':path,'line':ln,'destination':dest,'syntax':'html'})
    elif child.type=='text' and re.search(r'(?<![\w\]])\[[^\]\n]+\]\[[^\]\n]*\]',child.content):issue('unresolved_explicit_reference_review',path,ln,text=child.content[:250])
  if t.type=='table_open':current_table=[]
  if t.type=='tr_open':row=[]
  elif t.type=='inline' and row is not None:row.append(visible(t.children))
  elif t.type=='tr_close':
   rows.append(row)
   if current_table is not None:current_table.append(row)
   row=None
  if t.type=='table_close':
   table_rows.append(current_table);current_table=None
  if t.type=='table_open' and t.map:
   tables+=1;start,end=t.map;expected=count_cells(lines[start])
   for n in range(start+2,end):
    if lines[n].strip() and count_cells(lines[n])!=expected:issue('table_column_mismatch',path,n+1,expected=expected,actual=count_cells(lines[n]),text=lines[n][:250])
 for n,line in enumerate(lines):
  if n not in blocked and line.lstrip().startswith('\\`\\`\\`'):issue('escaped_fence_review',path,n+1,text=line[:200])
 for label,duplicates in env.get('duplicate_refs',{}).items() if isinstance(env.get('duplicate_refs'),dict) else []:issue('duplicate_reference_review',path,1,label=label)
 docs[path]={'text':text,'headings':headings,'explicit_anchors':explicit,'rows':rows,'table_rows':table_rows,'fences':fences,'tables':tables,'sha256':hashlib.sha256(text.encode()).hexdigest()}
 return docs[path]

# All Book 1 Markdown, including prior QA evidence, plus the repository landing index.
scan=sorted(str(p.relative_to(ROOT)) for p in (ROOT/BOOK).rglob('*.md'))+['README.md']
for p in scan:parse_document(p)
locked=parse_document(BOOK+'/MASTER-TOC.md')['text'];expected={};chapters={}
for line in locked.splitlines():
 m=re.match(r'^# Chapter (\d+) — (.+)$',line)
 if m:chapters[int(m[1])]=plain(m[2])
 m=re.match(r'^(\d+)\.(\d+)\s+—\s+(.+?)\s*$',line)
 if m:
  key=(int(m[1]),int(m[2]));title=plain(m[3])
  if key in expected:issue('duplicate_locked_id',BOOK+'/MASTER-TOC.md',1,section=f'{key[0]}.{key[1]}')
  expected[key]=title
if len(expected)!=322 or len(chapters)!=21:issue('locked_inventory_size',BOOK+'/MASTER-TOC.md',1,sections=len(expected),chapters=len(chapters))
canonical=collections.defaultdict(list);companions=[]
for path in scan:
 m=re.match(re.escape(BOOK)+r'/chapter-(\d{2})/(\d+)\.(\d+)-([^/]+)\.md$',path)
 if m and 'solutions-and-reference-implementations' not in m[4]:
  key=(int(m[2]),int(m[3]));canonical[key].append(path)
  if int(m[1])!=key[0]:issue('chapter_directory_mismatch',path,1,section=f'{key[0]}.{key[1]}')
 if path.endswith('-solutions-and-reference-implementations.md'):companions.append(path)
for key,title in expected.items():
 files=canonical.get(key,[])
 if len(files)!=1:issue('section_file_count',BOOK,1,section=f'{key[0]}.{key[1]}',expected=1,actual=files);continue
 path=files[0];heads=docs[path]['headings'];h=next((x for x in heads if x['level']==1),None)
 if h is None:issue('missing_section_h1',path,1);continue
 match=re.match(r'^(?:Section\s+)?(\d+)\.(\d+)\s*[—–-]\s*(.*)$',plain(h['text']))
 if not match:issue('unrecognized_section_title',path,h['line'],actual=h['text']);continue
 if (int(match[1]),int(match[2]))!=key or plain(match[3])!=title:issue('section_title_mismatch',path,h['line'],section=f'{key[0]}.{key[1]}',expected=title,actual=plain(match[3]))
for key,files in canonical.items():
 if key not in expected:issue('unexpected_section_file',files[0],1,section=f'{key[0]}.{key[1]}')
# Chapter indexes: exact title, complete ordered table, row labels, companion IDs.
for ch,title in chapters.items():
 path=f'{BOOK}/chapter-{ch:02}/README.md'
 if path not in docs:issue('missing_chapter_index',path,1);continue
 d=docs[path];h=next((x for x in d['headings'] if x['level']==1),None)
 if h is None or plain(h['text'])!=f'Chapter {ch} — {title}':issue('chapter_index_title_mismatch',path,h['line'] if h else 1,expected=f'Chapter {ch} — {title}',actual=h['text'] if h else None)
 found=[]
 for row in next((table[1:] for table in d['table_rows'] if table and plain(table[0][0])=='Section'),[]):
  if not row:continue
  m=re.fullmatch(r'(\d+)\.(\d+)',plain(row[0]))
  if not m:continue
  key=(int(m[1]),int(m[2]));found.append(key)
  if key not in expected:issue('chapter_index_unknown_id',path,1,section=row[0])
  elif len(row)>1 and plain(row[1])!=expected[key]:issue('chapter_index_row_title_mismatch',path,1,section=row[0],expected=expected[key],actual=plain(row[1]))
 wanted=[k for k in expected if k[0]==ch]
 if found!=wanted:issue('chapter_index_inventory_mismatch',path,1,expected=[f'{a}.{b}' for a,b in wanted],actual=[f'{a}.{b}' for a,b in found])
for path in companions:
 m=re.search(r'/chapter-(\d{2})/(?:solutions/)?(\d+)\.(\d+)-',path);key=(int(m[2]),int(m[3])) if m else None
 if not m or int(m[1])!=key[0] or key not in expected:issue('companion_identity_mismatch',path,1)
# Book index chapter headings and any section-labelled links must retain locked titles.
for path in (BOOK+'/README.md','README.md'):
 d=docs[path]
 bookheads=[h for h in d['headings'] if re.match(r'^Chapter \d+ — ',plain(h['text']))]
 if path==BOOK+'/README.md':
  ids=[]
  for h in bookheads:
   m=re.match(r'^Chapter (\d+) — (.+)$',plain(h['text']));ch=int(m[1]);ids.append(ch)
   if ch not in chapters or m[2]!=chapters[ch]:issue('book_index_chapter_title_mismatch',path,h['line'],chapter=ch,actual=m[2],expected=chapters.get(ch))
  if ids!=list(chapters):issue('book_index_chapter_inventory_mismatch',path,1,expected=list(chapters),actual=ids)
# Extract target documents, including any external-to-book Markdown targets, before slugging.
resolved=[];processed=0
while processed<len(links):
 link=links[processed];processed+=1;dest=link['destination'];u=urlsplit(dest);target=None
 if u.scheme in ('http','https'):
  parts=unquote(u.path).split('/')
  if u.netloc.lower() in ('github.com','www.github.com') and len(parts)>=6 and parts[1:3]==['sssamant21','python-financial-mathematics'] and parts[3] in ('blob','tree') and parts[4] in ('main',subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True).stdout.strip()):target='/'.join(parts[5:])
  elif u.netloc.lower()=='raw.githubusercontent.com' and len(parts)>=5 and parts[1:3]==['sssamant21','python-financial-mathematics'] and parts[3]=='main':target='/'.join(parts[4:])
  else:external.append(link);continue
 elif u.scheme or u.netloc:external.append(link);continue
 else:target=posixpath.normpath(posixpath.join(posixpath.dirname(link['file']),unquote(u.path))) if u.path else link['file']
 if target.startswith('../') or target.startswith('/'):
  issue('repository_escape_or_root_absolute_review',link['file'],link['line'],destination=dest,target=target);continue
 if link['file']=='README.md' and not target.startswith(BOOK+'/'):
  external.append({**link,'scope':'outside Book 1 landing-index scope'});continue
 actual=ROOT/target
 if not actual.exists():issue('missing_internal_target',link['file'],link['line'],destination=dest,target=target);link_results.append({**link,'target':target,'status':'FAIL'});continue
 if actual.is_dir():
  readme=next((actual/x for x in ('README.md','readme.md') if (actual/x).is_file()),None)
  if readme:target=str(readme.relative_to(ROOT));actual=readme
 if actual.is_file() and actual.suffix.lower()=='.md' and target not in docs and u.fragment:
  link_count,finding_count=len(links),len(findings);parse_document(target);del links[link_count:];del findings[finding_count:]
 resolved.append({**link,'target':target,'fragment':unquote(u.fragment)})
# Use the upstream github-slugger package for duplicate and Unicode heading semantics.
helper=OUT/'slugger-helper.mjs';helper.write_text("import fs from 'node:fs';import {pathToFileURL} from 'node:url';const {default:Slugger}=await import(pathToFileURL(process.argv[2]).href);const input=JSON.parse(fs.readFileSync(0,'utf8'));const output={};for(const [file,names] of Object.entries(input)){const s=new Slugger();output[file]=names.map(n=>s.slug(n));}process.stdout.write(JSON.stringify(output));\n")
payload={p:[h['text'] for h in d['headings']] for p,d in docs.items()};proc=subprocess.run(['node',str(helper),str(SLUGGER)],input=json.dumps(payload),text=True,capture_output=True,check=True,timeout=45);slugs=json.loads(proc.stdout)
anchors={p:set(slugs[p]+d['explicit_anchors']+['user-content-'+x for x in slugs[p]+d['explicit_anchors']]) for p,d in docs.items()}
for link in resolved:
 fragment=link['fragment'];target=link['target'];status='PASS'
 if fragment:
  if target in anchors:
   if fragment not in anchors[target]:issue('missing_internal_anchor',link['file'],link['line'],destination=link['destination'],target=target,fragment=fragment);status='FAIL'
  elif re.fullmatch(r'L\d+(?:-L?\d+)?',fragment):
   try:count=len((ROOT/target).read_text().splitlines());nums=[int(x) for x in re.findall(r'\d+',fragment)];ok=all(1<=n<=count for n in nums)
   except (UnicodeError,IsADirectoryError):ok=False
   if not ok:issue('invalid_file_line_anchor',link['file'],link['line'],destination=link['destination']);status='FAIL'
  else:issue('non_markdown_anchor_review',link['file'],link['line'],destination=link['destination'],target=target);status='REVIEW'
 link_results.append({**link,'status':status})
# Navigation completeness and labels in current indexes.
indexes={BOOK+'/README.md','README.md',*[f'{BOOK}/chapter-{ch:02}/README.md' for ch in chapters]}
path_ids={paths[0]:key for key,paths in canonical.items() if len(paths)==1}
for key,paths in canonical.items():
 if len(paths)!=1:continue
 index=f'{BOOK}/chapter-{key[0]:02}/README.md'
 if not any(x['file']==index and x['target']==paths[0] and x['status']=='PASS' for x in link_results):issue('missing_section_index_link',index,1,section=f'{key[0]}.{key[1]}',target=paths[0])
for path in companions:
 ch=int(re.search(r'/chapter-(\d{2})/',path)[1]);index=f'{BOOK}/chapter-{ch:02}/README.md'
 if not any(x['file']==index and x['target']==path and x['status']=='PASS' for x in link_results):issue('missing_companion_index_link',index,1,target=path)
for ch in chapters:
 target=f'{BOOK}/chapter-{ch:02}/README.md'
 if not any(x['file']==BOOK+'/README.md' and x['target']==target and x['status']=='PASS' for x in link_results):issue('missing_book_to_chapter_index_link',BOOK+'/README.md',1,chapter=ch,target=target)
for link in link_results:
 if link['file'] not in indexes or link['target'] not in path_ids:continue
 label=plain(link.get('label',''));m=re.fullmatch(r'(?:Section\s+)?(\d+)\.(\d+)(?:\s*[—–-]\s*(.+))?',label)
 if not m:continue
 key=path_ids[link['target']];claimed=(int(m[1]),int(m[2]))
 if claimed!=key or (m[3] is not None and plain(m[3])!=expected[key]):issue('index_link_label_mismatch',link['file'],link['line'],label=label,target=link['target'],expected=f'{key[0]}.{key[1]} — {expected[key]}')
summary={'book1_markdown_files':len(scan)-1,'repository_landing_indexes':1,'additional_target_markdown_files':len(docs)-len(scan),'locked_chapters':len(chapters),'locked_sections':len(expected),'canonical_section_files':sum(len(x) for x in canonical.values()),'companions':len(companions),'parsed_documents':len(docs),'headings':sum(len(d['headings']) for d in docs.values()),'fenced_blocks':sum(d['fences'] for d in docs.values()),'tables':sum(d['tables'] for d in docs.values()),'explicit_internal_links_checked':len(link_results),'internal_links_with_fragments':sum(bool(x.get('fragment')) for x in link_results),'chapter_indexes_verified':len(chapters),'section_index_links_verified':sum(any(x['file']==f'{BOOK}/chapter-{key[0]:02}/README.md' and x['target']==paths[0] and x['status']=='PASS' for x in link_results) for key,paths in canonical.items() if len(paths)==1),'companion_index_links_verified':sum(any(x['file']==f'{BOOK}/chapter-{int(re.search(r"/chapter-(\d{2})/",path)[1]):02}/README.md' and x['target']==path and x['status']=='PASS' for x in link_results) for path in companions),'internal_links_passed':sum(x['status']=='PASS' for x in link_results),'external_historical_or_out_of_scope_links_not_checked':len(external),'findings':len(findings),'findings_by_kind':dict(collections.Counter(x['kind'] for x in findings))}
manifest={'base_revision':subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip(),'parser':{'markdown-it-py':version('markdown-it-py'),'mdurl':version('mdurl'),'github-slugger':'2.0.0'},'documents':{p:{'sha256':d['sha256'],'heading_count':len(d['headings']),'anchor_count':len(slugs[p])} for p,d in docs.items()}}
for name,value in [('summary.json',summary),('findings.json',findings),('internal-links.json',link_results),('external-links-deferred.json',external),('input-manifest.json',manifest)]: (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2));
if findings:sys.exit(1)
