from pathlib import Path
import subprocess,sys,re,tempfile,importlib,json,hashlib
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;pin='9ebd2355077d8c7e8b9348b8f44eb78f57017402';p='books/book-01-python-foundations-for-financial-mathematics/chapter-21/21.01-capstone-architecture.md';raw=subprocess.check_output(['git','show',pin+':'+p],cwd=ROOT,text=True);f=re.findall(r'```python\n(.*?)\n```',raw,re.S);assert len(f)==2
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);(t/'capstone_architecture.py').write_text(f[0]);sys.path.insert(0,tmp);m=importlib.import_module('capstone_architecture')
 request=m.ValuationRequest(110.,.1,'  XYZ  ');a=m.evaluate(request)
 tiny=float.fromhex('0x0.0000000000001p-1022');b=m.present_value_one_period(tiny,1.)
 d=dict(source_revision=pin,source_sha256=hashlib.sha256(raw.encode()).hexdigest(),observations=[dict(name='metadata label preserved',actual=a.__dict__,status='Documented acceptance;not ISO validation or FX conversion;no new defect.'),dict(name='documented subnormal underflow',actual=repr(b),exact_rational=str(Fraction(tiny)/2),status='Documented range limitation;not new failing acceptance predicate.')],limits='Two exact-source observations only;reference suite,40answers/12lab steps and broader contracts not yet reviewed. Resume21.1 formal review;not completed.')
(OUT/(sys.argv[1] if len(sys.argv)>1 else 'initial.json')).write_text(json.dumps(d,indent=2)+'\n');print('2 scoped resume observations;not formal validation completion')
