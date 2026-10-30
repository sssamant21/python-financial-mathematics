"""Supplemental exercise policies; the manuscript research.py stays unchanged."""
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
import hashlib
import json
import re
from research import analyze, decode

def round_each_then_sum(data_raw, config_raw):
    """Reuse original validation, then deliberately change the rounding stage."""
    baseline = analyze(data_raw, config_raw)
    with localcontext(Context(prec=28, rounding=ROUND_HALF_EVEN)):
        rounded = sum((Decimal(row['amount']).quantize(Decimal('0.01'))
                       for row in decode(data_raw)), Decimal('0'))
    return dict(baseline, total=format(rounded, '.2f'), method='round_each_then_sum')

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate artifact key')
        result[key] = value
    return result

def validate_artifact(raw, *, returncode, data_raw, config_raw, source_raw,
                      expected_result, expected_runtime):
    """Accept only a complete, bound artifact from a successful controlled run.

    expected_result is a caller-supplied reviewed benchmark, not derived by
    calling analyze. Runtime values come from the selected controlled runner.
    Shape/hash agreement is not authentication or independent acceptance.
    """
    if type(returncode) is not int or returncode != 0:
        raise ValueError('unsuccessful process')
    obj = json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                     parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    if type(obj) is not dict or set(obj) != {'schema_version', 'result', 'evidence'}:
        raise ValueError('artifact schema')
    if type(obj['schema_version']) is not int or obj['schema_version'] != 1:
        raise ValueError('schema version')
    result = obj['result']
    if type(result) is not dict or set(result) != {'count','currency','total','method','rounding'}:
        raise ValueError('result schema')
    if type(result['count']) is not int or not 1 <= result['count'] <= 1000:
        raise ValueError('count')
    for field, fixed in [('currency','USD'), ('method','sum_then_round'), ('rounding','ROUND_HALF_EVEN')]:
        if type(result[field]) is not str or result[field] != fixed:
            raise ValueError('unsupported result policy')
    total = result['total']
    if type(total) is not str or re.fullmatch(r'(0|[1-9][0-9]{0,9})\.[0-9]{2}',total) is None:
        raise ValueError('total text')
    # Integer cents avoids inherited decimal context during acceptance.
    whole, fraction = total.split('.')
    if int(whole)*100+int(fraction) > 100_000_000_000:
        raise ValueError('total bound')
    evidence = obj['evidence']
    runtime_keys = {'python','implementation','system'}
    digest_keys = {'input_sha256','config_sha256','source_sha256'}
    if type(evidence) is not dict or set(evidence) != runtime_keys | digest_keys | {'third_party_runtime_dependencies'}:
        raise ValueError('evidence schema')
    for field in digest_keys:
        if type(evidence[field]) is not str or re.fullmatch('[0-9a-f]{64}',evidence[field]) is None:
            raise ValueError('digest text')
    for field in runtime_keys:
        if type(evidence[field]) is not str or not evidence[field] or evidence[field].strip() != evidence[field]:
            raise ValueError('runtime text')
    if type(evidence['third_party_runtime_dependencies']) is not list or evidence['third_party_runtime_dependencies']:
        raise ValueError('unsupported dependency profile')
    for key, value in [('input_sha256',data_raw), ('config_sha256',config_raw), ('source_sha256',source_raw)]:
        if evidence[key] != hashlib.sha256(value).hexdigest():
            raise ValueError('snapshot binding mismatch')
    if set(expected_runtime) != runtime_keys or any(evidence[key] != expected_runtime[key] for key in runtime_keys):
        raise ValueError('runtime mismatch')
    if result != expected_result:
        raise ValueError('reviewed benchmark mismatch')
    return obj
