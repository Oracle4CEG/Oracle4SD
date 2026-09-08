"""Run all four stages in a new directory and compare to the governed teaching reference."""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import platform
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from common import contained, fresh_output, load_config, read_json, sha256, write_json


def compare(run_root, manifest):
    checks = []
    for item in manifest["files"]:
        file = contained(run_root, item["path"])
        checks.append({"path": item["path"], "status": "pass" if file.is_file() and
                       sha256(file) == item["sha256"] else "fail"})
    if not checks:
        raise ValueError("Reference contains no files")
    return checks


def run(config, output=None, verify=True):
    cfg = load_config(config, require_demo=True)  # stops blank project runs before any output
    reference = read_json(ROOT/"tests/reference/demo_manifest.json") if verify else None
    if verify and reference.get("data_version") != cfg["data_version"]:
        raise ValueError("Reference data_version does not match the configured data release")
    output = output or ROOT / "runs" / ("demo-" + uuid.uuid4().hex[:10])
    target = fresh_output(output)
    started = time.monotonic()
    for folder, script in [("query_data","query.py"), ("process_data","process.py"),
                           ("analyze_data","analyze.py"), ("technical_validation","validate.py")]:
        subprocess.run([sys.executable, str(ROOT/"code"/folder/script), "--config", str(Path(config).resolve()),
                        "--run-dir", str(target)], check=True, cwd=ROOT)
    comparison = compare(target, reference) if verify else []
    write_json(target/"reports/reproduction.json", {
        "evidence_status": "SYNTHETIC", "data_version": cfg["data_version"], "checks": comparison,
        "comparison": "Byte identity of selected deterministic teaching outputs",
        "limits": "Does not validate research measurements or representativeness"})
    git = subprocess.run(["git","rev-parse","HEAD"], cwd=ROOT,capture_output=True,text=True)
    worktree = subprocess.run(["git","status","--porcelain"],cwd=ROOT,capture_output=True,text=True)
    source_files = sorted(list((ROOT/"code").rglob("*.py")) + [Path(__file__).resolve()])
    write_json(target/"reports/run_environment.json",{
        "python": platform.python_version(), "platform": platform.platform(),
        "code_commit": git.stdout.strip() if git.returncode == 0 else None,
        "code_worktree_dirty": bool(worktree.stdout.strip()) if worktree.returncode == 0 else None,
        "source_file_hashes": {f.relative_to(ROOT).as_posix():sha256(f) for f in source_files},
        "config_sha256": sha256(config),
        "elapsed_seconds": round(time.monotonic()-started,4),
        "created_utc": datetime.now(timezone.utc).isoformat(), "scope": "synthetic teaching sample"})
    if any(x["status"] == "fail" for x in comparison):
        raise ValueError("Reference mismatch; inspect reports/reproduction.json")
    print("Teaching pipeline complete:", target)
    print("Scientific validation: NOT EVALUATED")
    return target


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config",default=str(ROOT/"configs/demo.json"))
    p.add_argument("--output")
    args=p.parse_args()
    run(args.config,args.output)
