"""One-currency transfer formulation with extra source-paid fees."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def scenario(*, source, destination, reserve, target, fixed_fee, fee_rate):
    values = dict(source=source, destination=destination, reserve=reserve,
                  target=target, fixed_fee=fixed_fee, fee_rate=fee_rate)
    values = {name: rational(value) for name, value in values.items()}
    if any(value < 0 for value in values.values()):
        raise ValueError("scenario inputs must be nonnegative")
    return values


def evaluate_transfer(*, transfer, **inputs):
    p = scenario(**inputs)
    x = rational(transfer)
    if x < 0:
        raise ValueError("transfer must be nonnegative")
    fee = p["fixed_fee"] + p["fee_rate"] * x if x > 0 else Fraction(0)
    source_after = p["source"] - x - fee
    destination_after = p["destination"] + x
    checks = {"source_reserve": source_after >= p["reserve"],
              "destination_target": destination_after >= p["target"]}
    return {"transfer": x, "fee": fee, "source_after": source_after,
            "destination_after": destination_after, "checks": checks,
            "feasible": all(checks.values())}


def minimum_transfer(**inputs):
    p = scenario(**inputs)
    needed = max(Fraction(0), p["target"] - p["destination"])
    candidate = evaluate_transfer(transfer=needed, **p)
    return {"feasible": candidate["feasible"], "needed": needed,
            "transfer": needed if candidate["feasible"] else None,
            "candidate_report": candidate}


def main():
    inputs = dict(source=1000, destination=200, reserve=300,
                  target=700, fixed_fee=5, fee_rate="0.01")
    result = minimum_transfer(**inputs)
    report = result["candidate_report"]
    print(f"Minimum transfer: {result['transfer']}")
    print(f"Fee: {report['fee']}")
    print(f"Final balances: source={report['source_after']}, "
          f"destination={report['destination_after']}")
    impossible = minimum_transfer(**(inputs | {"target": 900}))
    print(f"Higher target feasible: {impossible['feasible']}")
    print(f"Higher target transfer: {impossible['transfer']}")
    no_action = minimum_transfer(**(inputs | {"target": 200}))
    print(f"Already at target: transfer={no_action['transfer']}, "
          f"fee={no_action['candidate_report']['fee']}")


if __name__ == "__main__":
    main()
