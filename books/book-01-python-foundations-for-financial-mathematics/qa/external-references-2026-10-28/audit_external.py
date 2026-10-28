"""Inventory explicit Book 1 external Markdown URLs and record bounded GET probes.

Usage: python audit_external.py REPO_ROOT NEW_OUTPUT_DIR
Requires markdown-it-py 4.0.0 and mdurl 0.1.2. Uses standard-library HTTP.
HTTP success is availability evidence, not claim-level attribution approval.
"""
from __future__ import annotations
import collections,concurrent.futures,datetime,hashlib,json,pathlib,re,ssl,sys,threading,time,urllib.error,urllib.parse,urllib.request
from html.parser import HTMLParser
from markdown_it import MarkdownIt
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve();
if out.exists():raise SystemExit('Choose a new output directory to preserve prior evidence.')
out.mkdir(parents=True);book=root/'books/book-01-python-foundations-for-financial-mathematics';md=MarkdownIt('commonmark',{'html':True}).enable(['table','strikethrough']);occurrences=[];sources={}
def plain(tokens):return ''.join(t.content for t in tokens or [] if t.type in ('text','code_inline'))
for f in sorted(book.rglob('*.md')):
 text=f.read_text();sources[str(f.relative_to(root))]=hashlib.sha256(text.encode()).hexdigest();tokens=md.parse(text);heading=''
 for i,t in enumerate(tokens):
  if t.type=='heading_open':heading=plain(tokens[i+1].children)
  if t.type!='inline':continue
  children=t.children or []
  for j,c in enumerate(children):
   if c.type!='link_open':continue
   url=c.attrGet('href') or '';parts=urllib.parse.urlsplit(url)
   if parts.scheme not in ('http','https'):continue
   if parts.netloc.lower() in ('github.com','raw.githubusercontent.com') and '/sssamant21/python-financial-mathematics/' in parts.path and ('/blob/main/' in parts.path or '/tree/main/' in parts.path):continue
   end=next((k for k in range(j+1,len(children)) if children[k].type=='link_close'),len(children));base,_=urllib.parse.urldefrag(url)
   occurrences.append({'file':str(f.relative_to(root)),'line':t.map[0]+1,'heading':heading,'label':plain(children[j+1:end]),'url':url,'request_url':base,'fragment':urllib.parse.unquote(parts.fragment)})
urls=sorted({x['url'] for x in occurrences});bases=sorted({x['request_url'] for x in occurrences});(out/'occurrences.json').write_text(json.dumps(occurrences,ensure_ascii=False,indent=2)+'\n');(out/'source-manifest.json').write_text(json.dumps(sources,indent=2)+'\n')
class Metadata(HTMLParser):
 def __init__(self):super().__init__();self.in_title=False;self.title=[];self.ids=set();self.h1=False;self.heading=[];self.canonical=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='title':self.in_title=True
  if tag=='h1':self.h1=True
  for n in ('id','name'):
   if a.get(n):self.ids.add(a[n])
  if tag=='link' and 'canonical' in (a.get('rel') or '').split() and a.get('href'):self.canonical.append(a['href'])
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
  if tag=='h1':self.h1=False
 def handle_data(self,data):
  if self.in_title:self.title.append(data)
  if self.h1:self.heading.append(data)
class Redirects(urllib.request.HTTPRedirectHandler):
 def __init__(self):self.chain=[]
 def redirect_request(self,req,fp,code,msg,headers,newurl):self.chain.append({'status':code,'from':req.full_url,'to':newurl});return super().redirect_request(req,fp,code,msg,headers,newurl)
hosts={urllib.parse.urlsplit(u).netloc:threading.Semaphore(2) for u in bases};context=ssl.create_default_context();limit=2*1024*1024

def fetch(url):
 start=time.monotonic();redirect=Redirects();record={'url':url,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'GET'}
 try:
  with hosts[urllib.parse.urlsplit(url).netloc]:
   opener=urllib.request.build_opener(urllib.request.HTTPSHandler(context=context),redirect)
   req=urllib.request.Request(url,headers={'User-Agent':'Book1ReferenceAudit/1.0 (educational documentation availability audit)','Accept':'text/html,application/pdf,text/plain;q=0.8,*/*;q=0.1'})
   try:response=opener.open(req,timeout=18)
   except urllib.error.HTTPError as e:response=e
   with response:
    body=response.read(limit+1);truncated=len(body)>limit;body=body[:limit];status=response.code;record.update(http_status=status,final_url=response.geturl(),content_type=response.headers.get('Content-Type',''),body_truncated=truncated,body_bytes=len(body),body_sha256=hashlib.sha256(body).hexdigest(),redirects=redirect.chain)
    if 200<=status<300:
     record['availability']='AVAILABLE'
     if 'html' in record['content_type']:
      charset=response.headers.get_content_charset() or 'utf-8';text=body.decode(charset,errors='replace');parser=Metadata();parser.feed(text);record.update(title=' '.join(''.join(parser.title).split()),h1=' '.join(''.join(parser.heading).split()),canonical_urls=parser.canonical,anchor_ids=sorted(parser.ids))
      if re.search(r'\b(?:404|page not found|not found|access denied|just a moment)\b',record['title'],re.I):record['availability']='SOFT_ERROR_REVIEW'
    elif status in (401,403,429):record['availability']='ACCESS_RESTRICTED'
    elif status in (404,410):record['availability']='MISSING_CANDIDATE'
    else:record['availability']='HTTP_ERROR_REVIEW'
 except Exception as e:record.update(availability='NETWORK_INCONCLUSIVE',error=type(e).__name__+': '+str(e))
 record['elapsed_seconds']=round(time.monotonic()-start,3);return record
# Interleave domains so polite per-host limits do not block all worker slots.
byhost=collections.defaultdict(collections.deque)
for u in bases:byhost[urllib.parse.urlsplit(u).netloc].append(u)
ordered=[]
while any(byhost.values()):
 for values in byhost.values():
  if values:ordered.append(values.popleft())
cache={}
if len(sys.argv)>3:
 for record in json.loads(pathlib.Path(sys.argv[3]).read_text()):
  if record.get('availability')=='AVAILABLE' and record.get('checked_at_utc','').startswith(datetime.datetime.now(datetime.timezone.utc).date().isoformat()):cache[record['url']]=record
results=[]
for url in ordered:
 if url in cache:
  record=dict(cache[url]);record.pop('reused_same_session_probe',None);record['reused_same_utc_day_probe']=True;results.append(record)
ordered=[u for u in ordered if u not in cache]
print(json.dumps({'occurrences':len(occurrences),'unique_urls_including_fragments':len(urls),'unique_request_urls':len(bases),'hosts':len(byhost),'reused_successful_probes':len(results),'new_requests':len(ordered)}),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
 pending={executor.submit(fetch,u):u for u in ordered}
 for future in concurrent.futures.as_completed(pending):
  record=future.result();results.append(record)
  if record['availability']!='AVAILABLE':print(record['availability'],record.get('http_status'),record['url'],flush=True)
  if len(results)%30==0:print('PROGRESS',len(results),'of',len(bases),flush=True)
  (out/'requests.json').write_text(json.dumps(sorted(results,key=lambda x:x['url']),ensure_ascii=False,indent=2)+'\n')
(out/'requests.json').write_text(json.dumps(sorted(results,key=lambda x:x['url']),ensure_ascii=False,indent=2)+'\n')
byurl={x['url']:x for x in results};links=[]
for url in urls:
 base,fragment=urllib.parse.urldefrag(url);fragment=urllib.parse.unquote(fragment);r=byurl[base];status=r['availability'];anchor='NOT_APPLICABLE'
 if fragment:
  if status!='AVAILABLE':anchor='NOT_CHECKED_UNAVAILABLE'
  elif r.get('body_truncated'):anchor='NOT_CHECKED_TRUNCATED'
  elif 'html' not in r.get('content_type',''):anchor='NON_HTML_REVIEW'
  else:anchor='FOUND' if fragment in r.get('anchor_ids',[]) else 'MISSING_REVIEW'
 links.append({'url':url,'request_url':base,'availability':status,'http_status':r.get('http_status'),'final_url':r.get('final_url'),'title':r.get('title'),'fragment':fragment,'anchor_status':anchor,'occurrences':sum(x['url']==url for x in occurrences)})
summary={'checked_on':datetime.datetime.now(datetime.timezone.utc).date().isoformat(),'markdown_documents_inventoried':len(sources),'external_link_occurrences':len(occurrences),'unique_urls_including_fragments':len(urls),'unique_request_urls':len(bases),'hosts':len(byhost),'availability':dict(collections.Counter(x['availability'] for x in results)),'fragment_results':dict(collections.Counter(x['anchor_status'] for x in links)),'reused_successful_probes':sum(bool(x.get('reused_same_utc_day_probe')) for x in results),'attribution_status':'NOT_INFERRED_FROM_HTTP_STATUS'}
(out/'url-results.json').write_text(json.dumps(links,ensure_ascii=False,indent=2)+'\n');(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)

if any(x["availability"]!="AVAILABLE" for x in results) or any(x["anchor_status"] not in ("NOT_APPLICABLE","FOUND") for x in links):sys.exit(1)
