"""Generate truth JSON files for hill-instability-tongues benchmark cases."""

import sys
import os
import json
import pathlib
import math

import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from hill_core import instability_intervals, monodromy_delta

# ---------------------------------------------------------------------------
# Case definitions
# ---------------------------------------------------------------------------

CASES = [
    {
        "name": "public",
        "c0": 0.0,
        "cos": [4.0],
        "sin": [],
        "period": 6.283185307179586,
        "lambda_min": -5.0,
        "lambda_max": 20.0,
        "min_width": 0.01,
    },
    {
        "name": "hidden_01",
        "c0": 1.0,
        "cos": [2.0, 1.0],
        "sin": [1.5],
        "period": 6.283185307179586,
        "lambda_min": -2.0,
        "lambda_max": 15.0,
        "min_width": 0.01,
    },
    {
        "name": "hidden_02",
        "c0": 0.5,
        "cos": [3.0, 1.5, 0.8],
        "sin": [2.0, 1.0],
        "period": 3.141592653589793,
        "lambda_min": 0.0,
        "lambda_max": 30.0,
        "min_width": 0.02,
    },
    {
        "name": "hidden_03",
        "c0": 0.0,
        "cos": [8.0],
        "sin": [],
        "period": 3.141592653589793,
        "lambda_min": 10.0,
        "lambda_max": 50.0,
        "min_width": 0.05,
    },
    {
        "name": "hidden_04",
        "c0": -0.5,
        "cos": [2.5, 1.2, 0.6],
        "sin": [1.8, 0.9, 0.4],
        "period": 6.283185307179586,
        "lambda_min": -3.0,
        "lambda_max": 25.0,
        "min_width": 0.01,
    },
]

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

TASK_ROOT = pathlib.Path(__file__).parent.parent.parent  # …/hill-instability-tongues
TRUTH_DIR = TASK_ROOT / "tests" / "truth" / "raw"
ENV_DATA_DIR = TASK_ROOT / "environment" / "data"

TRUTH_DIR.mkdir(parents=True, exist_ok=True)
ENV_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CROSS_VAL_TOL = 1e-10


def cross_validate(interval, c0, cos, sin, period):
    """Return (passed, messages) for one interval dict."""
    messages = []
    passed = True
    for key, lam_key, delta_key in [
        ("left", "lambda_left", "left_delta"),
        ("right", "lambda_right", "right_delta"),
        ("sample", "sample_lambda", "sample_delta"),
    ]:
        lam = interval[lam_key]
        reported = interval[delta_key]
        computed = monodromy_delta(lam, c0, cos, sin, period)
        err = abs(reported - computed)
        if err >= CROSS_VAL_TOL:
            messages.append(
                f"  {key} cross-val FAIL: lam={lam:.6f} "
                f"reported={reported:.6f} computed={computed:.6f} err={err:.2e}"
            )
            passed = False
    return passed, messages


def main():
    print("=" * 60)
    print("Generating hill-instability-tongues truth data")
    print("=" * 60)

    all_ok = True

    for case in CASES:
        name = case["name"]
        c0 = case["c0"]
        cos = case["cos"]
        sin = case["sin"]
        period = case["period"]
        lambda_min = case["lambda_min"]
        lambda_max = case["lambda_max"]
        min_width = case["min_width"]

        print(f"\nCase: {name}")

        intervals = instability_intervals(
            c0, cos, sin, period,
            lambda_min, lambda_max, min_width,
            M=64,
            polish=True,
        )

        print(f"  Intervals found: {len(intervals)}")

        # Cross-validate every interval
        case_ok = True
        for idx, iv in enumerate(intervals):
            passed, messages = cross_validate(iv, c0, cos, sin, period)
            if not passed:
                case_ok = False
                all_ok = False
                for msg in messages:
                    print(msg)

        status = "PASS" if case_ok else "FAIL"
        print(f"  Cross-validation: {status}")

        # Build truth JSON
        truth = {"intervals": intervals}
        out_path = TRUTH_DIR / f"{name}.json"
        with open(out_path, "w") as fh:
            json.dump(truth, fh, indent=2)
        print(f"  Written: {out_path}")

    # Write public_case.json (input parameters only, no solution data)
    public = CASES[0]
    public_input = {
        "c0": public["c0"],
        "cos": public["cos"],
        "sin": public["sin"],
        "period": public["period"],
        "lambda_min": public["lambda_min"],
        "lambda_max": public["lambda_max"],
        "min_width": public["min_width"],
    }
    pub_path = ENV_DATA_DIR / "public_case.json"
    with open(pub_path, "w") as fh:
        json.dump(public_input, fh, indent=2)
    print(f"\nWritten: {pub_path}")

    print("\n" + "=" * 60)
    print(f"Overall cross-validation: {'PASS' if all_ok else 'FAIL (see above)'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
