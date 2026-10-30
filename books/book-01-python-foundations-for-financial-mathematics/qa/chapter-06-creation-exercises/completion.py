"""Supplemental completed-result contract, not manuscript source."""
import numpy as np

def validate_completed(results, completed):
    """Return an independent copy only after every cell is complete and finite.

    Exact nonempty 2-D float64 results and matching bool status arrays.
    No filling, partial report, financial-domain inference or transaction claim.
    """
    if type(results) is not np.ndarray or results.dtype != np.dtype('float64'):
        raise TypeError('results must be an exact float64 ndarray')
    if type(completed) is not np.ndarray or completed.dtype != np.dtype('bool'):
        raise TypeError('status must be an exact bool ndarray')
    if results.ndim != 2 or 0 in results.shape or completed.shape != results.shape:
        raise ValueError('nonempty matching two-dimensional arrays required')
    if not completed.all():
        raise ValueError('unfinished result entries')
    if not np.isfinite(results).all():
        raise ValueError('completed results must be finite')
    return results.copy(order='C')
