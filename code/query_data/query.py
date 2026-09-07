"""Acquire checksum-pinned local or HTTPS files; no credentials or live API assumptions."""
from pathlib import Path
import argparse
import re
import shutil
import sys
from urllib.parse import urlsplit
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, contained, load_config, sha256, write_json


def acquire(config, run_root):
    cfg = load_config(config)
    raw = Path(run_root) / "queried_data"
    raw.mkdir(parents=True, exist_ok=False)
    evidence = []
    names = set()
    for source in cfg["sources"]:
        if not source.get("source_id") or not re.fullmatch(r"[0-9a-f]{64}", source.get("sha256", "")):
            raise ValueError("Every source needs an ID and verified SHA-256")
        target = contained(raw, source["filename"])
        if target in names:
            raise ValueError("Duplicate source destination")
        names.add(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + ".partial")
        limit = source.get("max_bytes", 50_000_000)
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("max_bytes must be positive")
        try:
            if source["kind"] == "local":
                origin = contained(ROOT, source["path"])
                if not origin.is_file() or origin.stat().st_size > limit:
                    raise ValueError("Missing or oversized source")
                shutil.copyfile(origin, tmp)
            elif source["kind"] == "https":
                url = source["url"]
                parsed = urlsplit(url)
                if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                    raise ValueError("Use a public HTTPS URL without embedded credentials")
                with urlopen(url, timeout=30) as response, tmp.open("wb") as dest:
                    if urlsplit(response.geturl()).scheme != "https":
                        raise ValueError("HTTPS redirects must remain HTTPS")
                    total = 0
                    while chunk := response.read(1024 * 1024):
                        total += len(chunk)
                        if total > limit:
                            raise ValueError("Source exceeds the configured size cap")
                        dest.write(chunk)
            else:
                raise ValueError("Supported source kinds are local and https; add an explicit adapter for APIs")
            if sha256(tmp) != source["sha256"]:
                raise ValueError("Source checksum mismatch")
            tmp.replace(target)
        finally:
            tmp.unlink(missing_ok=True)
        evidence.append({"source_id": source["source_id"], "path": target.relative_to(run_root).as_posix(),
                         "sha256": sha256(target), "bytes": target.stat().st_size,
                         "data_version": cfg["data_version"], "evidence_status": cfg["evidence_status"]})
    write_json(Path(run_root) / "reports/acquisition.json", evidence)
    return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    acquire(args.config, Path(args.run_dir).resolve())
