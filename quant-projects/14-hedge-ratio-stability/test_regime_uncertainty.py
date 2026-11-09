import pytest
from regime_uncertainty import block_intervals

def rows():
    return [dict(origin=i*13, window=52, shrinkage=0.0,
                 regime="early" if i < 4 else "late", variance_reduction=0.1*i)
            for i in range(8)]

def test_reproducible():
    assert block_intervals(rows()) == block_intervals(rows())

def test_regimes_separate():
    result = block_intervals(rows())
    assert result["early"]["mean"] == pytest.approx(.15)
    assert result["late"]["mean"] == pytest.approx(.55)
    assert result["early"]["upper"] < result["late"]["lower"]

def test_future_mutation_does_not_change_early():
    data = rows()
    before = block_intervals(data)["early"]
    data[-1]["variance_reduction"] = -100
    assert block_intervals(data)["early"] == before

def test_insufficient_blocks_not_fabricated():
    result = block_intervals(rows()[:5])
    assert result["late"]["status"] == "insufficient_blocks"
    assert result["late"]["lower"] is None

def test_nonfinite_rejected_as_unverified():
    data = rows()
    data[1]["variance_reduction"] = float("nan")
    assert block_intervals(data)["early"]["status"] == "nonfinite_reduction"

@pytest.mark.parametrize("kw", [{"draws":99}, {"draws":1.5}, {"seed":-1},
                                {"confidence":1}, {"min_blocks":1},
                                {"window":7}, {"shrinkage":1.2}])
def test_guardrails(kw):
    with pytest.raises(ValueError):
        block_intervals(rows(), **kw)

def test_duplicate_origin_rejected():
    data = rows()
    data[1]["origin"] = data[0]["origin"]
    with pytest.raises(ValueError):
        block_intervals(data)
