"""Metadata audit, separate from manuscript execution and acceptance."""
import hashlib,json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
queue=json.loads((HERE.parent/'chapter-06-answer-review/section-exercise-queue.json').read_text())
records=queue['records'];assert len(records)==128 and len({r['id'] for r in records})==128
assert queue['reviewed']==128 and queue['pending']==0 and all(r['status']=='REVIEWED_SCOPED' for r in records)
assert all(hashlib.sha256((BOOK/r['source']).read_bytes()).hexdigest()==r['source_sha256'] for r in records)
assert all((HERE.parent/'chapter-06-answer-review'/r['evidence']).resolve().exists() for r in records)
counts=Counter(r['id'].split('-E')[0] for r in records);assert len(counts)==16 and set(counts.values())=={8}
result=dict(scope='metadata consistency only; not rerun of prior runtime evidence',records=128,unique_ids=128,reviewed=128,pending=0,source_files=len({r['source'] for r in records}),source_hash_mismatches=0,evidence_links_missing=0,counts=dict(counts))
(HERE/'queue-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
