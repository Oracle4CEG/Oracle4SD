"""Synthetic teaching adapter: exact deduplication, flags and Celsius-to-kelvin conversion."""
from pathlib import Path
import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import load_config, read_csv, sha256, write_csv, write_json

FIELDS = ["observation_id", "group_id", "timestamp_utc", "temperature_c",
          "temperature_k", "value_status", "origin"]


def process(config, run_root):
    cfg = load_config(config, require_demo=True)
    raw = Path(run_root) / "queried_data/observations.csv"
    before = sha256(raw)
    rows = read_csv(raw)
    expected = {"observation_id", "group_id", "timestamp_utc", "temperature_c", "origin"}
    seen, output, decisions = {}, [], []
    for row in rows:
        if set(row) != expected or row["origin"] != "synthetic_teaching":
            raise ValueError("Unexpected schema or non-teaching source")
        ident = row["observation_id"]
        if not ident or not row["group_id"]:
            raise ValueError("Missing stable identifier")
        try:
            parsed_time = datetime.fromisoformat(row["timestamp_utc"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("timestamp_utc must be an ISO 8601 UTC timestamp ending in Z or +00:00") from exc
        if parsed_time.tzinfo is None or parsed_time.utcoffset().total_seconds() != 0:
            raise ValueError("Document UTC timestamps explicitly")
        if ident in seen:
            if seen[ident] != row:
                raise ValueError("Conflicting duplicate ID requires an explicit scientific decision")
            decisions.append({"id": ident, "decision": "drop_exact_duplicate"})
            continue
        seen[ident] = row
        text = row["temperature_c"]
        if text == "":
            c, k, status = "", "", "missing"
        else:
            try:
                value = Decimal(text)
            except InvalidOperation as exc:
                raise ValueError("Non-numeric temperature") from exc
            if not value.is_finite():
                raise ValueError("Non-finite temperature")
            if not Decimal("-50") <= value <= Decimal("60"):
                decisions.append({"id": ident, "decision": "exclude_teaching_range"})
                continue
            c, k, status = f"{value:.2f}", f"{value + Decimal('273.15'):.2f}", "synthetic_value"
        output.append({"observation_id": ident, "group_id": row["group_id"],
                       "timestamp_utc": row["timestamp_utc"], "temperature_c": c,
                       "temperature_k": k, "value_status": status, "origin": row["origin"]})
    output.sort(key=lambda row: row["observation_id"])
    target = Path(run_root) / "processed_data/observations.csv"
    if target.exists():
        raise FileExistsError("Refusing stale processed output")
    write_csv(target, FIELDS, output)
    if sha256(raw) != before:
        raise ValueError("Raw input changed")
    write_json(Path(run_root) / "reports/processing.json", {
        "evidence_status": "SYNTHETIC", "input_rows": len(rows), "output_rows": len(output),
        "decisions": decisions, "range_rule_scope": "Arbitrary teaching rule, not a domain recommendation",
        "missing_rule": "Retain and flag; never impute zero", "raw_sha256": before,
        "processed_sha256": sha256(target)})
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    process(args.config, Path(args.run_dir).resolve())
