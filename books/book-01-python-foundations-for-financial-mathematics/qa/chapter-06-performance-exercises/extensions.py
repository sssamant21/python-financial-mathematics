"""Supplemental experiments; not manuscript implementations or production APIs."""
import cProfile
import io
import json
import pstats
import statistics
import timeit
from pathlib import Path
import numpy as np


def validated_python(quantity, start, end):
    """Same array-to-three-array contract/checks as Section 6.5, scalar arithmetic."""
    for name, value in (('quantity',quantity),('start',start),('end',end)):
        if type(value) is not np.ndarray or value.dtype != np.dtype('float64'):
            raise TypeError(f'{name} must be an exact float64 ndarray')
        if value.ndim != 1 or value.size == 0:
            raise ValueError(f'{name} must be a nonempty vector')
        if not np.isfinite(value).all():
            raise ValueError(f'{name} must be finite')
    if quantity.shape != start.shape or start.shape != end.shape:
        raise ValueError('all vectors must have equal shape')
    if (start < 0).any() or (end < 0).any():
        raise ValueError('prices must be nonnegative')
    with np.errstate(over='raise',divide='raise',invalid='raise',under='raise'):
        # NumPy scalars retain local floating-signal behavior in this loop.
        rows=[(q*p0,q*p1,q*(p1-p0)) for q,p0,p1 in zip(quantity,start,end)]
        opening=np.array([row[0] for row in rows],dtype=np.float64)
        closing=np.array([row[1] for row in rows],dtype=np.float64)
        pnl=np.array([row[2] for row in rows],dtype=np.float64)
    if not all(np.isfinite(value).all() for value in (opening,closing,pnl)):
        raise ValueError('nonfinite output')
    return {'opening':opening,'closing':closing,'pnl':pnl}


def resident_reused_out(q, start, end, out):
    """Prevalidated, equal-shape, nonaliasing writable float64 out; overwrite it."""
    np.subtract(end,start,out=out)
    np.multiply(q,out,out=out)
    return out


def measure(operation, *, repeat=5, number=3):
    operation()  # Untimed warm-up; correctness is checked by the caller first.
    samples=[total/number for total in timeit.repeat(operation,repeat=repeat,number=number)]
    return dict(seconds_per_call=samples,minimum=min(samples),median=statistics.median(samples),repeat=repeat,number=number)


def rotated_sessions(source, size=1000):
    arrays,lists=source.prepare(size)
    methods={'python_lists':lambda:source.python_lists(*lists),
             'numpy_lists':lambda:source.numpy_lists(*lists),
             'numpy_resident':lambda:source.numpy_resident(*arrays)}
    names=tuple(methods);sessions=[]
    for shift in range(3):
        order=names[shift:]+names[:shift]
        source.verify(arrays,lists)  # Original correctness gate before timers.
        timings={name:measure(methods[name]) for name in order}
        sessions.append(dict(session=shift,method_order=order,size=size,correctness='passed',timings=timings,list_boundary_median_ratio=timings['python_lists']['median']/timings['numpy_lists']['median']))
    return sessions


def report_workflow(input_path, output_path, public_numpy):
    """Complete controlled local file -> validated API -> JSON file workflow."""
    wire=json.loads(Path(input_path).read_text())
    arrays=tuple(np.array(wire[k],dtype=np.float64) for k in ('quantity','start','end'))
    result=public_numpy(*arrays)
    record={'scope':'synthetic same-currency fixed-quantity price-only changes',
            'position_ids':wire['position_ids'],
            'results':{key:value.tolist() for key,value in result.items()}}
    Path(output_path).write_text(json.dumps(record,allow_nan=False)+'\n')
    return record


def profile_workflow(input_path, output_path, public_numpy, evidence_dir):
    profiler=cProfile.Profile()
    profiler.enable()
    result=report_workflow(input_path,output_path,public_numpy)
    profiler.disable()
    stream=io.StringIO();stats=pstats.Stats(profiler,stream=stream).sort_stats('cumulative');stats.print_stats()
    Path(evidence_dir,'workflow-profile.txt').write_text(stream.getvalue())
    compute=[(key,value) for key,value in stats.stats.items() if key[2]=='position_changes']
    assert len(compute)==1
    key,value=compute[0];total=stats.total_tt
    return result,dict(profile_total_seconds=total,public_api_cumulative_seconds=value[3],public_api_fraction=value[3]/total,
        public_api_location=dict(filename=key[0],line=key[1],name=key[2]),
        qualification='single cProfile-instrumented synthetic run; API fraction includes validation and allocation; not pure kernel fraction or production SLO')
