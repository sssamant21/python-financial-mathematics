"""Supplemental Y/N vocabulary adapter; original converter remains unchanged."""
import pandas as pd
from conversion import convert_records

def convert_yn(raw):
    """Exact Y/N text maps to true/false; preserve all other source contracts."""
    columns=['asset','lot_count','price','reviewed']
    if not isinstance(raw,pd.DataFrame) or not raw.columns.is_unique or raw.columns.tolist()!=columns:
        raise ValueError('exact ordered source schema required')
    if not raw['reviewed'].map(lambda x:isinstance(x,str) and x in ('Y','N')).all():
        raise ValueError('reviewed must be exactly Y or N')
    mapped=raw.copy(deep=True)
    mapped['reviewed']=mapped['reviewed'].map({'Y':'true','N':'false'})
    return convert_records(mapped)
