"""Exercise actual file creation, retry and no-overwrite boundaries."""
import json
from pathlib import Path
import tempfile
import section_20_07 as lab


def attempt(path,data):
    try:
        lab.write_manifest(path,data)
    except (TypeError,ValueError,FileExistsError) as exc:
        return type(exc).__name__
    return 'written'


def check():
    rows=[]
    def record(case,expected,actual):
        rows.append(dict(case=case,expected=expected,actual=actual,passed=expected==actual))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for name,data in [('text','abc'),('mutable-bytes',bytearray(b'abc'))]:
            p=root/(name+'.json')
            status=attempt(p,data)
            record(name,['TypeError',False],[status,p.exists()])
            record(name+' retry','written',attempt(p,b'abc'))
        old=lab.make_manifest
        try:
            for name,value,error in [('non-json',object(),'TypeError'),
                                     ('nonfinite',float('nan'),'ValueError')]:
                lab.make_manifest=lambda data:{'synthetic':value}
                p=root/(name+'.json')
                status=attempt(p,b'abc')
                record(name,[error,False],[status,p.exists()])
        finally:
            lab.make_manifest=old
        p=root/'valid.json'
        record('valid write','written',attempt(p,b'abc'))
        written=p.read_bytes()
        payload=json.loads(written)
        keys=['input_sha256','execution_status','source_commit','working_tree_dirty',
              'command','exit_code','actual_result','review_status','approval_status']
        expected=['ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
                  'not run',None,None,None,None,None,'pending','pending']
        record('known digest and pending fields',expected,[payload[k] for k in keys])
        status=attempt(p,b'changed')
        record('valid collision',['FileExistsError',True],[status,p.read_bytes()==written])
        status=attempt(p,'invalid')
        record('invalid input precedes opening',['TypeError',True],[status,p.read_bytes()==written])
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
