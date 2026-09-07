"""Small shared helpers; project-specific scientific decisions belong in stage code."""
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


class AuthorInputRequired(ValueError):
    pass


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def contained(root, relative):
    root = Path(root).resolve()
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts:
        raise ValueError(f"Expected a non-empty relative path: {relative}")
    current = root
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symbolic links are not accepted in release inputs")
    path = (root / rel).resolve()
    path.relative_to(root)
    return path


def fresh_output(path):
    path = Path(path).resolve()
    if path == ROOT or ROOT.is_relative_to(path) or path.is_relative_to(ROOT / "data"):
        raise ValueError("Run outputs must not overwrite repository data or its parent")
    if path.exists():
        raise FileExistsError(f"Choose a new output directory: {path}")
    path.mkdir(parents=True)
    return path


def load_config(path, require_demo=False):
    value = read_json(path)
    if not value.get("dataset_id") or not value.get("data_version") or not value.get("sources"):
        raise AuthorInputRequired("Complete dataset_id, data_version and sources in the project configuration")
    if require_demo and value.get("pipeline") != "synthetic_temperature_teaching_v1":
        raise AuthorInputRequired("Implement and validate your scientific processing adapter; the supplied adapter is a teaching example")
    return value


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, fields, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
