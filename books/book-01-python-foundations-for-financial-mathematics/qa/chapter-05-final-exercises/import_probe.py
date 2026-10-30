"""Observe a fresh installed import, allowing import-loader code reads only.

Common application file interfaces are denied; open audit events outside
importlib.get_data are denied too. This is scoped regression instrumentation,
not an OS sandbox or a proof covering arbitrary native/kernel operations.
"""
import builtins
import contextlib
import decimal
import importlib
import io
import json
import os
from pathlib import Path
import re
import sys
import typing

events=[]
active=True
def deny(*args,**kwargs):
    raise RuntimeError('APPLICATION_FILE_ACCESS')

def audit(event,args):
    if not active or event!='open':return
    frame=sys._getframe(1)
    loader=False
    while frame is not None:
        if frame.f_code.co_filename=='<frozen importlib._bootstrap_external>' and frame.f_code.co_name=='get_data':
            loader=True;break
        frame=frame.f_back
    events.append(dict(path=str(args[0]),loader=loader))
    if not loader:deny()

patches=[(builtins,'open'),(io,'open'),(Path,'open'),(Path,'read_bytes'),
         (Path,'read_text'),(Path,'write_bytes'),(Path,'write_text'),
         (Path,'stat'),(Path,'exists')]
originals=[(obj,name,getattr(obj,name)) for obj,name in patches]
captured_out,captured_err=io.StringIO(),io.StringIO()
sys.addaudithook(audit)
try:
    for obj,name,_ in originals:setattr(obj,name,deny)
    with contextlib.redirect_stdout(captured_out),contextlib.redirect_stderr(captured_err):
        package=importlib.import_module('financial_inflows')
        importlib.import_module('financial_inflows.cli')
finally:
    for obj,name,value in originals:setattr(obj,name,value)
    active=False
assert captured_out.getvalue()==captured_err.getvalue()==''
assert events and all(event['loader'] for event in events)
print(json.dumps(dict(stdout=captured_out.getvalue(),stderr=captured_err.getvalue(),
                     origin=package.__file__,allowed_loader_events=events)))
