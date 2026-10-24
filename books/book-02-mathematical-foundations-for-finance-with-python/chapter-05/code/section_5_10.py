"""Section 5.10: cumulative Chapter 05 assessment calculations."""
import math

def assessment_values():
    geometric = 500 * 1.04 ** 3
    recurrence_first = 1000 * 1.02 + 100
    recurrence_second = recurrence_first * 1.02 + 100
    timing_end = 1000 * 1.05 + 100
    timing_begin = (1000 + 100) * 1.05
    stable_equilibrium = 50 / (1 - 0.9)
    tolerance_period = math.ceil(math.log(10 / 400) / math.log(0.9))
    sensitivity = 20 * 0.8 ** 5
    shock = 100 * 1.02 ** 3
    rates = (0.02, -0.01, 0.03)
    flows = (100, -50, 0)
    end_balance = 1000.0
    begin_balance = 1000.0
    for rate, flow in zip(rates, flows):
        end_balance = end_balance * (1 + rate) + flow
        begin_balance = (begin_balance + flow) * (1 + rate)
    return {
        "geometric": geometric,
        "recurrence_first": recurrence_first,
        "recurrence_second": recurrence_second,
        "timing_end": timing_end,
        "timing_begin": timing_begin,
        "stable_equilibrium": stable_equilibrium,
        "tolerance_period": tolerance_period,
        "sensitivity": sensitivity,
        "shock": shock,
        "variable_end": end_balance,
        "variable_begin": begin_balance,
    }

if __name__ == "__main__":
    for key, value in assessment_values().items():
        print(f"{key}: {value}")
