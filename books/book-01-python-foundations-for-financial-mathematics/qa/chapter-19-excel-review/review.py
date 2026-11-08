from pathlib import Path
from decimal import Decimal,localcontext
from datetime import date,datetime,timezone
from io import BytesIO
import re,subprocess,tempfile,importlib.util,sys,hashlib,platform,json,base64,zipfile,xml.etree.ElementTree as ET
import openpyxl
from openpyxl.utils.datetime import CALENDAR_MAC_1904,CALENDAR_WINDOWS_1900
ROOT=Path(__file__).resolve().parents[4];BOOK=ROOT/'books/book-01-python-foundations-for-financial-mathematics';SOURCE=BOOK/'chapter-19/19.04-excel-data.md';OUT=Path(__file__).parent

def run():
    revision=sys.argv[1] if len(sys.argv)>1 else None;text=subprocess.check_output(['git','-C',str(ROOT),'show',revision+':'+str(SOURCE.relative_to(ROOT))],text=True) if revision else SOURCE.read_text();blocks=re.findall(r'~~~python\n(.*?)\n~~~',text,re.S);commands=[];rows=[];artifacts={}
    def check(name,call,expected=None,error=None):
        try:value=call();ok=error is None and value==expected;actual=repr(value)
        except Exception as exc:actual=type(exc).__name__+': '+str(exc);ok=type(exc) is error
        rows.append(dict(name=name,passed=ok,actual=actual,expected=error.__name__ if error else repr(expected)))
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp);p=temp/'excel_financial_data.py';p.write_text(blocks[1]);spec=importlib.util.spec_from_file_location('excel_data',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        fixture=OUT/'fixture-base64.json'
        if fixture.exists():raw=base64.b64decode(json.loads(fixture.read_text())['base64'])
        else:
            raw=m.example_workbook();fixture.write_text(json.dumps(dict(sha256=hashlib.sha256(raw).hexdigest(),base64=base64.b64encode(raw).decode()),indent=2)+'\n')
        artifacts['example.xlsx']=raw;(temp/'prices.xlsx').write_bytes(raw);(temp/'inspect_example.py').write_text(blocks[0])
        for args in [[sys.executable,'inspect_example.py'],[sys.executable,p.name],[sys.executable,'-m','compileall','-q','.'],[sys.executable,'-c','import excel_financial_data']]:
            result=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr));assert result.returncode==0
        def mutate(name,fn,epoch=None):
            wb=openpyxl.load_workbook(BytesIO(raw));ws=wb['Prices']
            if epoch is not None:wb.epoch=epoch
            fn(wb,ws);buf=BytesIO();wb.save(buf);wb.close();data=buf.getvalue();artifacts[name]=data;return data
        check('base records',lambda:len(m.parse_workbook(raw)),2);check('raw identity',lambda:m.raw_sha256(raw),hashlib.sha256(raw).hexdigest());check('base return',lambda:m.simple_return(Decimal('100'),Decimal('101.50')),Decimal('.015'))
        formula=mutate('formula-no-cache.xlsx',lambda wb,ws:setattr(ws['C3'],'value','=100+1.5'))
        def cached(data):
            output=BytesIO()
            with zipfile.ZipFile(BytesIO(data)) as src,zipfile.ZipFile(output,'w') as dst:
                for item in src.infolist():
                    content=src.read(item.filename)
                    if item.filename=='xl/worksheets/sheet1.xml':
                        root=ET.fromstring(content);ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                        cell=root.find(".//s:c[@r='C3']",ns);cell.find('s:v',ns).text='101.5';content=ET.tostring(root,encoding='utf-8')
                    dst.writestr(item,content)
            return output.getvalue()
        with_cache=cached(formula);artifacts['formula-seeded-cache.xlsx']=with_cache
        def cellvalue(data,data_only):
            wb=openpyxl.load_workbook(BytesIO(data),read_only=True,data_only=data_only)
            try:return wb['Prices']['C3'].value
            finally:wb.close()
        check('formula text visible',lambda:cellvalue(formula,False),'=100+1.5');check('cache missing',lambda:cellvalue(formula,True),None);check('seeded cache visible',lambda:cellvalue(with_cache,True),101.5);check('formula cache does not bypass policy',lambda:m.parse_workbook(with_cache),error=ValueError);check('formula rejected',lambda:m.parse_workbook(formula),error=ValueError)
        for epoch,label in [(CALENDAR_WINDOWS_1900,'1900'),(CALENDAR_MAC_1904,'1904')]:
            def dates(wb,ws):ws['B2']=date(2026,1,5);ws['B3']=datetime(2026,1,6)
            data=mutate('dates-'+label+'.xlsx',dates,epoch);check('date-system '+label,lambda:[r['date'] for r in m.parse_workbook(data)],[date(2026,1,5),date(2026,1,6)])
        variants=[('hidden row',lambda wb,ws:setattr(ws.row_dimensions[3],'hidden',True),2),('blank row',lambda wb,ws:ws.insert_rows(3),2),('numeric prices',lambda wb,ws:(setattr(ws['C2'],'value',100.),setattr(ws['C3'],'value',101.5)),2)]
        for name,fn,n in variants:
            data=mutate(name.replace(' ','-')+'.xlsx',fn);check(name,lambda:len(m.parse_workbook(data)),n)
        invalid=[('missing sheet',lambda wb,ws:setattr(ws,'title','Other')),('header order',lambda wb,ws:(setattr(ws['A1'],'value','date'),setattr(ws['B1'],'value','instrument'))),('extra width',lambda wb,ws:setattr(ws['E1'],'value','extra')),('formula header',lambda wb,ws:setattr(ws['A1'],'value','=1+1')),('duplicate key',lambda wb,ws:setattr(ws['B3'],'value','2026-01-05')),('blank price',lambda wb,ws:setattr(ws['C3'],'value',None)),('bool price',lambda wb,ws:setattr(ws['C3'],'value',True)),('bad date',lambda wb,ws:setattr(ws['B3'],'value','bad')),('nonmidnight',lambda wb,ws:setattr(ws['B3'],'value',datetime(2026,1,6,12))),('EUR',lambda wb,ws:setattr(ws['D3'],'value','EUR')),('merged instrument',lambda wb,ws:ws.merge_cells('A2:A3'))]
        for name,fn in invalid:
            data=mutate(name.replace(' ','-')+'.xlsx',fn);check(name,lambda:m.parse_workbook(data),error=ValueError)
        check('corrupt archive library error',lambda:m.parse_workbook(b'not-a-zip'),error=zipfile.BadZipFile);check('raw wrong type',lambda:m.parse_workbook(None),error=ValueError)
        for value in [True,'NaN',float('inf'),0,-1]:check('bad price '+repr(value),lambda:m.parse_price(value),error=ValueError)
        check('timezone rejected',lambda:m.parse_day(datetime(2026,1,1,tzinfo=timezone.utc)),error=ValueError);check('date string',lambda:m.parse_day('2026-01-06'),date(2026,1,6))
        for a,b,ref in [('1','1.000000000000000000000000000001','1e-30'),('2','0','-1')]:check('complete return '+repr((a,b)),lambda:m.simple_return(Decimal(a),Decimal(b)),Decimal(ref))
        with localcontext() as ctx:
            ctx.prec=2;check('private return precision',lambda:m.simple_return(Decimal(100),Decimal('101.50')),Decimal('.015'))
        archive={name:dict(sha256=hashlib.sha256(data).hexdigest(),base64=base64.b64encode(data).decode()) for name,data in artifacts.items()};(OUT/('fixtures-baseline-replay.json' if revision else 'fixtures-current.json')).write_text(json.dumps(archive,indent=2)+'\n')
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),selected_revision=revision,source_sha256=hashlib.sha256(text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),openpyxl_version=openpyxl.__version__,commands=commands,supplemental_predicates=rows,existing_unique_methods=10,new_historical_methods=0,formula_cache_note='Cache101.5 manually seeded in OOXML fixture;not Excel recalculation or native-engine validation',scope='Exact openpyxl reference execution and supplemental serialized fixtures;not native Excel UI/recalculation,macros,workbook trust,resource,source authenticity,platform or independent acceptance')
        (OUT/('baseline-replay.json' if revision else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(x['passed'] for x in rows);print(len(rows),'predicates;4 source commands;10 existing methods passed')
if __name__=='__main__':run()
