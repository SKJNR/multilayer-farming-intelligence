from __future__ import annotations
import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import scipy
from simulation.agrisim_core import TwoLayerSoilWaterModel
from simulation.soil_generator import generate_soil_priors
from simulation.identifiability import run_screen


def main() -> None:
    n, reps = 10_000, 5
    times = []
    for _ in range(reps):
        model = TwoLayerSoilWaterModel()
        start = time.perf_counter()
        for _ in range(n):
            model.step(10.0, 4.0, 5.0, 8.0, (0.3, 0.7))
        times.append(time.perf_counter() - start)

    soils = generate_soil_priors(1000, seed=42)
    report = {
        "status": "v2.0 universal multi-strata + patched 2-layer audit",
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "timing": {
            "steps_per_rep": n,
            "repetitions": reps,
            "seconds": times,
            "mean_seconds": float(np.mean(times)),
            "std_seconds_population": float(np.std(times)),
            "microseconds_per_step": float(np.mean(times) / n * 1e6),
        },
        "soil_prior_count": len(soils),
        "soil_prior_ordering_passed": all(
            0 < s["theta_wp"] < s["theta_fc"] < s["theta_aer"] < s["theta_sat"] <= 1.0
            and s["theta_sat"] - s["theta_fc"] >= 0.08 - 1e-12
            for s in soils
        ),
        "identifiability_screen": run_screen(),
    }
    out = ROOT / "artifacts" / "candidate_audit.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
