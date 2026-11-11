"""Synthetic binary-payoff Kelly sizing with estimation-error diagnostics; not trading advice."""
import argparse
import math

def optimal_fraction(probability, win_return, loss_fraction, cap=1.0):
    """Maximize expected log growth for +win_return or -loss_fraction, long-only."""
    for value in (probability, win_return, loss_fraction, cap):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("all parameters must be finite real numbers")
    if not 0 < probability < 1 or win_return <= 0 or not 0 < loss_fraction <= 1 or not 0 < cap <= 1:
        raise ValueError("invalid probability, payoff or cap")
    raw = (probability * win_return - (1-probability)*loss_fraction) / (win_return * loss_fraction)
    return max(0.0, min(cap, raw))

def expected_log_growth(fraction, probability, win_return, loss_fraction):
    if isinstance(fraction, bool) or not isinstance(fraction, (int, float)) or not math.isfinite(fraction) or not 0 <= fraction <= 1:
        raise ValueError("fraction must be in [0,1]")
    optimal_fraction(probability, win_return, loss_fraction)
    if fraction * loss_fraction >= 1:
        return -math.inf
    return probability * math.log1p(fraction*win_return) + (1-probability)*math.log1p(-fraction*loss_fraction)

def stress_grid(estimated_probability, win_return, loss_fraction, probability_shocks=(-0.1, 0.0, 0.1), cap=1.0):
    fraction = optimal_fraction(estimated_probability, win_return, loss_fraction, cap)
    outcomes = []
    for shock in probability_shocks:
        if isinstance(shock, bool) or not isinstance(shock, (int,float)) or not math.isfinite(shock):
            raise ValueError("invalid shock")
        true_probability = estimated_probability + shock
        if not 0 < true_probability < 1:
            raise ValueError("shocked probability outside (0,1)")
        outcomes.append((true_probability, expected_log_growth(fraction, true_probability, win_return, loss_fraction)))
    return fraction, outcomes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hypothetical binary-payoff Kelly estimation stress")
    parser.add_argument("--probability", type=float, default=0.55)
    parser.add_argument("--cap", type=float, default=0.5)
    args = parser.parse_args()
    fraction, rows = stress_grid(args.probability, 1.0, 1.0, cap=args.cap)
    print(f"Illustrative fraction: {fraction:.4f}")
    for probability, growth in rows:
        print(f"True probability {probability:.2f}: expected log growth {growth:.6f}")
