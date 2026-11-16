"""F209 explicit shape policy: baseline/prose-corrected exact-fence execution."""
from pathlib import Path
import sys,subprocess,re,hashlib,json,tempfile,importlib.util,math,platform
from fractions import Fraction as F
from collections import OrderedDict
from types import MappingProxyType
here=Path(__file__).resolve().parent;root=here.parents[3];pin='00b08db5c71f1f72f53395728d25dcf1d4fffcb0';path='books/book-01-python-foundations-for-financial-mathematics/chapter-20/20.08-input-validation.md';mode,stem=sys.argv[1:3]
assert mode in ('baseline','working','corrected')
raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root) if mode=='baseline' else (subprocess.check_output(['git','show','2ee81822af67357087e2af6193348f2b3c5dbdf8:'+path],cwd=root) if mode=='corrected' else (root/path).read_bytes());code=re.search(r'~~~python\n(.*?)\n~~~',raw.decode(),re.S)[1];records=[]
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'source.py';p.write_text(code);spec=importlib.util.spec_from_file_location('source',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for label,value in [('mapping',{0:100,1:110}),('ordered mapping',OrderedDict([(0,100),(1,110)])),('proxy mapping',MappingProxyType({0:100,1:110})),('set',{100,110}),('frozenset',frozenset([100,110])),('key view',{1:1,2:2}.keys()),('bytes',b'100'),('bytearray',bytearray(b'100')),('buffer',memoryview(b'100')),('text','100')]:
  for api in ('validate_cashflows','npv'):
   try:a=getattr(m,api)(value,*([.1] if api=='npv' else []));actual=repr(a);exc=None;ok=False
   except Exception as e:actual=str(e);exc=type(e).__name__;ok=isinstance(e,ValueError) and 'ordered cash-flow iterable' in str(e)
   records.append(dict(case=label+' '+api,kind='explicit shape policy',actual=actual,exception=exc,passed=ok))
 for label,make,want in [('list',lambda:[-100,110],[-100,110]),('tuple',lambda:(-100,110),[-100,110]),('generator',lambda:(x for x in [-100,110]),[-100,110]),('range',lambda:range(1,4),[1,2,3]),('reversed',lambda:reversed([110,-100]),[-100,110]),('explicit values view',lambda:OrderedDict([(0,-100),(1,110)]).values(),[-100,110])]:
  got=m.validate_cashflows(make());records.append(dict(case=label,kind='retained ordered iterable',actual=got,expected=want,passed=got==want))
 seen=[]
 class TracedMapping(dict):
  def __iter__(self):seen.append('iterated');return super().__iter__()
 try:m.validate_cashflows(TracedMapping({0:100,1:110}))
 except ValueError:pass
 records.append(dict(case='reject mapping before iteration',kind='consumption contract',actual=seen,passed=seen==[]))
 for kind in (TypeError,RuntimeError):
  error=kind('late failure');seen=[]
  def broken():seen.append(1);yield 1;raise error
  try:m.validate_cashflows(broken())
  except Exception as e:ok=e is error and seen==[1]
  else:ok=False
  records.append(dict(case='late '+kind.__name__,kind='consumption contract',passed=ok))
 original=[-100,110];got=m.validate_cashflows(original);records.append(dict(case='fresh copy',kind='ownership',passed=got==original and got is not original));got[0]=0;records.append(dict(case='caller preserved',kind='ownership',passed=original==[-100,110]))
 for flows,rate in [([-100,110],.1),([-100,110],0.),([-100,10,110],-.05),([0,25,-10],.1)]:
  expected=sum((F(c)/(1+F(rate))**t for t,c in enumerate(flows)),F(0));actual=m.npv(flows,rate)
  records.append(dict(case='rational NPV '+repr((flows,rate)),kind='independent finance',actual=actual,expected=str(expected),absolute_tolerance=1e-10,passed=math.isclose(actual,float(expected),rel_tol=0,abs_tol=1e-10)))
result=dict(mode=mode,baseline_revision=pin,source_path=path,source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),python=sys.version,platform=platform.platform(),records=records,passed=sum(x['passed'] for x in records),failed=sum(not x['passed'] for x in records),limits='Shape policy probes separate from original observed acceptances. Ordered iterables retained;upstream origin/financial order and resource limits not established.')
(here/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(mode,result['passed'],result['failed']);raise SystemExit(bool(result['failed']))
