"""New public helper in the temporary exercise package copy."""
from .core import analyze

def inflow_count(data_raw: bytes, config_raw: bytes) -> int:
    """Return the count after the complete original financial validation."""
    return analyze(data_raw, config_raw)['count']
