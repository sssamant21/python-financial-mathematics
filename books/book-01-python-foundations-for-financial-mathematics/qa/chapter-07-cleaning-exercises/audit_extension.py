"""Supplemental field-change and canonical-record batch audit, not a CSV reader."""
import hashlib,json
import pandas as pd
from cleaning import clean,FIELDS
POLICY_VERSION='book1-7.8-strip-uppercase-currency-v1'
HASH_KIND='sha256-canonical-utf8-json-records-v1'

def audited_clean(raw):
    good,bad,log=clean(raw)  # Original boundary validates first; no source changes.
    source=raw.reset_index(drop=True).copy(deep=True)
    # Exact, documented serialization of parsed source records; not original file bytes.
    payload=(json.dumps(source.to_dict(orient='records'),ensure_ascii=False,
                        separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')
    digest=hashlib.sha256(payload).hexdigest()
    changes=[]
    for ordinal,row in source.iterrows():
        for field in FIELDS:
            before=row[field];after=before.strip()
            if field=='currency':after=after.upper()
            if before!=after:
                changes.append(dict(source_row=ordinal,field=field,before=before,after=after,
                                    source_batch_sha256=digest,policy_version=POLICY_VERSION))
    fields=['source_row','field','before','after','source_batch_sha256','policy_version']
    field_changes=pd.DataFrame(changes,columns=fields)
    decision=log.assign(source_batch_sha256=digest,source_hash_kind=HASH_KIND,
                        policy_version=POLICY_VERSION)
    return dict(accepted=good,rejected=bad,decision_log=decision,field_changes=field_changes,
                source_payload=payload,source_batch_sha256=digest,source_hash_kind=HASH_KIND,
                policy_version=POLICY_VERSION)
