"""Describe the synthetic teaching sample with explicit missing-value denominators."""
from pathlib import Path
import argparse
from decimal import Decimal
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import load_config, read_csv, write_csv


def analyze(config, run_root):
    load_config(config, require_demo=True)
    rows = read_csv(Path(run_root) / "processed_data/observations.csv")
    values = [Decimal(row["temperature_c"]) for row in rows if row["temperature_c"] != ""]
    result = {
        "evidence_status": "SYNTHETIC", "n_records": len(rows), "n_nonmissing": len(values),
        "n_missing": len(rows)-len(values),
        "mean_temperature_c": f"{sum(values) / len(values):.4f}" if values else "",
        "unit": "degree_Celsius", "interpretation": "Teaching example only; no real-world inference"}
    target = Path(run_root) / "analysis/summary.csv"
    if target.exists():
        raise FileExistsError("Refusing stale analysis output")
    write_csv(target, list(result), [result])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    analyze(args.config, Path(args.run_dir).resolve())
