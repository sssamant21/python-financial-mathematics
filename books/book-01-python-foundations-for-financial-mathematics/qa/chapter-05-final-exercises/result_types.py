"""Document the existing result shape; annotations do not validate values."""
from typing import Literal, TypedDict

class AnalyzeResult(TypedDict):
    currency: Literal['USD']
    count: int
    total: str
    method: Literal['sum_then_round']
    rounding: Literal['ROUND_HALF_EVEN']
