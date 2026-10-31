"""Supplemental E5 guard; caller supplies an aligned Boolean Series.

Preconditions: validated table; unique matching mask identities and Boolean
(or nullable Boolean) dtype. This helper adds an unknown-condition policy,
not an arbitrary mask parser or financial valuation validator.
"""
def select_known(table,mask):
    if mask.isna().any():
        raise ValueError('unknown Boolean condition: selection withheld')
    return table.loc[mask].copy(deep=True)
