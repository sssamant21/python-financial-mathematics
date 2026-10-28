"""Check the actual probe definitions against controlled local HTTP fixtures."""
import ast,hashlib,http.server,json,pathlib,ssl,sys,threading
script=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);tree=ast.parse(script.read_text());selected=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)) or isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in ('Metadata','Redirects','fetch')];namespace={};exec(compile(ast.Module(body=selected,type_ignores=[]),str(script),'exec'),namespace)
class Fixture(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  path=self.path
  if path=='/redirect':self.send_response(302);self.send_header('Location','/ok');self.end_headers();return
  code={'/missing':404,'/forbidden':403,'/rate-limit':429}.get(path,200)
  if path=='/pdf':body=b'%PDF-1.4 teaching fixture';ctype='application/pdf'
  elif path=='/large':body=b'x'*256;ctype='text/plain'
  elif path=='/soft':body=b'<title>404 Page not found</title>';ctype='text/html'
  else:body=b'<title>Audit fixture</title><h1>Reference</h1><a id="known"></a>';ctype='text/html'
  self.send_response(code);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Fixture);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();host='127.0.0.1:'+str(server.server_port);namespace.update(hosts={host:threading.Semaphore(2)},context=ssl.create_default_context(),limit=128);rows=[]
def check(name,condition):
 if not condition:raise AssertionError(name)
 rows.append({'check':name,'status':'PASS'})
try:
 records={name:namespace['fetch']('http://'+host+'/'+name) for name in ('ok','redirect','missing','forbidden','rate-limit','soft','pdf','large')}
 for name,expected in [('ok','AVAILABLE'),('redirect','AVAILABLE'),('missing','MISSING_CANDIDATE'),('forbidden','ACCESS_RESTRICTED'),('rate-limit','ACCESS_RESTRICTED'),('soft','SOFT_ERROR_REVIEW'),('pdf','AVAILABLE'),('large','AVAILABLE')]:check(name+' availability classification',records[name]['availability']==expected)
 check('redirect chain retained',len(records['redirect']['redirects'])==1 and records['redirect']['final_url'].endswith('/ok'))
 check('HTML title and anchor extracted',records['ok']['title']=='Audit fixture' and 'known' in records['ok']['anchor_ids'])
 check('bounded body and truncation retained',records['large']['body_truncated'] and records['large']['body_bytes']==128)
 check('hash covers retained bytes',records['large']['body_sha256']==hashlib.sha256(b'x'*128).hexdigest())
 result={'status':'PASS','checks':rows};out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(rows)}))
finally:server.shutdown();server.server_close()
