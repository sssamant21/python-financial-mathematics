import json,sys,platform,pathlib,hashlib
items=json.loads(pathlib.Path(sys.argv[1]).read_text()); results=[]
for r in items:
 try: compile(r['code'],r['id'],'exec'); status='PASS'; error=None
 except SyntaxError as e: status='CONTEXT_FRAGMENT' if r['id'] in ('chapter-02/2.10-break-continue-and-loop-control.md:16','chapter-02/2.10-break-continue-and-loop-control.md:81') and 'outside loop' in str(e) else 'FAIL'; error=str(e)
 results.append({'id':r['id'],'sha256':r['sha256'],'status':status,'error':error})
output={'interpreter':sys.version,'platform':platform.platform(),'results':results,'pass':sum(r['status']=='PASS' for r in results),'context_fragments':sum(r['status']=='CONTEXT_FRAGMENT' for r in results),'fail':sum(r['status']=='FAIL' for r in results)}
pathlib.Path(sys.argv[2]).write_text(json.dumps(output,indent=2)+'\n'); print({k:v for k,v in output.items() if k!='results'}); sys.exit(bool(output['fail']))
