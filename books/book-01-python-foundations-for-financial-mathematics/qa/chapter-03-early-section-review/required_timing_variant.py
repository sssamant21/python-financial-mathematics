from decimal import Decimal

def advance_balance(balance, periodic_rate, *, contribution=Decimal('0'), contribution_timing):
    values = [('balance', balance), ('periodic_rate', periodic_rate), ('contribution', contribution)]
    for name, value in values:
        if not isinstance(value, Decimal):
            raise TypeError(f'{name} must be Decimal')
        if not value.is_finite():
            raise ValueError(f'{name} must be finite')
    if balance < 0 or contribution < 0:
        raise ValueError('balance and contribution must be nonnegative')
    if periodic_rate <= Decimal('-1'):
        raise ValueError('periodic_rate must be greater than -1')
    if not isinstance(contribution_timing, str):
        raise TypeError('contribution_timing must be a string')
    if contribution_timing not in ('end', 'beginning'):
        raise ValueError('Unsupported contribution timing')
    factor = Decimal('1') + periodic_rate
    if contribution_timing == 'beginning':
        return (balance + contribution) * factor
    return balance * factor + contribution

def append_cash_flow(cash_flow, cash_flows=None):
    if cash_flows is None:
        cash_flows = []
    cash_flows.append(cash_flow)
    return cash_flows
principal = Decimal('1000')
rate = Decimal('0.05')
default_result = advance_balance(principal, rate, contribution_timing='end')
assert default_result == Decimal('1050')
explicit_result = advance_balance(balance=principal, periodic_rate=rate, contribution=Decimal('0'), contribution_timing='end')
assert default_result == explicit_result
end_result = advance_balance(principal, rate, contribution=Decimal('100'), contribution_timing='end')
beginning_result = advance_balance(principal, rate, contribution=Decimal('100'), contribution_timing='beginning')
assert end_result == Decimal('1150')
assert beginning_result == Decimal('1155')
assert beginning_result - end_result == Decimal('5')
assert advance_balance(principal, Decimal('0'), contribution=Decimal('100'), contribution_timing='end') == Decimal('1100')
assert advance_balance(principal, Decimal('-0.10'), contribution_timing='end') == Decimal('900')
assert advance_balance(Decimal('0'), rate, contribution_timing='end') == Decimal('0')
first = append_cash_flow(Decimal('100'))
second = append_cash_flow(Decimal('200'))
assert first == [Decimal('100')]
assert second == [Decimal('200')]
assert first is not second
supplied = []
assert append_cash_flow(Decimal('300'), supplied) is supplied
assert supplied == [Decimal('300')]
binding_failures = [lambda: advance_balance(principal, rate, Decimal('100'), contribution_timing='end'), lambda: advance_balance(principal, rate, annual_rate=rate, contribution_timing='end'), lambda: advance_balance(principal, rate, balance=principal, contribution_timing='end'), lambda: advance_balance(principal, contribution_timing='end')]
for call in binding_failures:
    try:
        call()
    except TypeError:
        pass
    else:
        raise AssertionError('Expected binding failure')
invalid_values = [({'contribution': None}, TypeError), ({'contribution': 100}, TypeError), ({'contribution': Decimal('-1')}, ValueError), ({'contribution': Decimal('NaN')}, ValueError), ({'contribution_timing': None}, TypeError), ({'contribution_timing': 'monthly'}, ValueError)]
for options, expected_error in invalid_values:
    try:
        advance_balance(principal, rate, **{'contribution_timing': 'end', **options})
    except expected_error:
        pass
    else:
        raise AssertionError('Expected invalid-value rejection')
print(f'No contribution: {default_result:.2f}')
print(f'End contribution: {end_result:.2f}')
print(f'Beginning contribution: {beginning_result:.2f}')
print('PASS: default and keyword argument checks')
