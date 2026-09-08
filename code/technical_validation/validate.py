"""Bounded software checks for the teaching fixture; scientific validation remains unevaluated."""
from pathlib import Path
import argparse
from collections import Counter
from decimal import Decimal, InvalidOperation
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import load_config, read_csv, write_json


def validate(config, run_root):
    load_config(config, require_demo=True)
    rows = read_csv(Path(run_root) / "processed_data/observations.csv")
    checks = []
    def add(name, n, failures, criterion):
        checks.append({"check": name, "n_examined": n, "n_failed": failures,
                       "criterion": criterion,
                       "status": "not_evaluated" if n == 0 else ("fail" if failures else "pass")})
    ids = [row["observation_id"] for row in rows]
    id_counts = Counter(ids)
    add("unique_nonempty_ids", len(rows), sum(not x or id_counts[x] > 1 for x in ids),
        "Every output row has one unique stable ID")
    bad_conversion, measured, bad_missing, bad_origin = 0, 0, 0, 0
    for row in rows:
        bad_origin += row["origin"] != "synthetic_teaching"
        if row["temperature_c"] == "":
            bad_missing += row["temperature_k"] != "" or row["value_status"] != "missing"
        else:
            measured += 1
            try:
                c, k = Decimal(row["temperature_c"]), Decimal(row["temperature_k"])
                valid = c.is_finite() and k.is_finite() and abs(k-c-Decimal("273.15")) <= Decimal("0.005")
                valid = valid and row["value_status"] == "synthetic_value"
            except InvalidOperation:
                valid = False
            bad_conversion += not valid
    add("unit_conversion", measured, bad_conversion, "K minus Celsius equals 273.15 within 0.005")
    add("missingness_encoding", len(rows), bad_missing, "Missing source values remain missing and flagged")
    add("synthetic_origin", len(rows), bad_origin, "All teaching records retain their synthetic label")
    for check in ["measurement_accuracy", "population_representativeness", "ML_construct_validity"]:
        checks.append({"check": check, "status": "not_evaluated", "n_examined": 0,
                       "reason": "Synthetic teaching data provide no project-specific scientific evidence"})
    report = {"evidence_status": "SYNTHETIC", "scope": "Bundled teaching fixture only",
              "scientific_readiness": "not_evaluated", "checks": checks}
    write_json(Path(run_root) / "reports/validation.json", report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    result = validate(args.config, Path(args.run_dir).resolve())
    raise SystemExit(1 if any(x["status"] == "fail" for x in result["checks"]) else 0)
