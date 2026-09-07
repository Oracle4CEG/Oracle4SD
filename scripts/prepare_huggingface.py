"""Prepare an allowlisted local dataset bundle. This script never uploads or publishes."""
from pathlib import Path
import argparse
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"code"))
from common import AuthorInputRequired, contained, fresh_output, read_json, sha256, write_json


def prepare(manifest_path, output):
    cfg=read_json(manifest_path)
    for field in ["dataset_title","data_version","dataset_license","card_path","files"]:
        if not cfg.get(field):
            raise AuthorInputRequired(f"Complete release manifest field: {field}")
    if cfg.get("redistribution_confirmed") is not True:
        raise AuthorInputRequired("Document redistribution permission before packaging")
    mode=cfg.get("release_kind")
    if mode not in ["synthetic_teaching","project"]:
        raise AuthorInputRequired("Choose release_kind explicitly")
    paths=[]
    names=set()
    for item in cfg["files"]:
        source=contained(ROOT,item["source"])
        destination=Path(item["destination"])
        contained(ROOT,destination) # syntax/path check
        if destination == Path("release_manifest.json"):
            raise ValueError("release_manifest.json is reserved for the generated manifest")
        if destination.as_posix() in names:
            raise ValueError("Duplicate bundle destination")
        names.add(destination.as_posix())
        if any(part.startswith(".") for part in destination.parts) or source.suffix in [".env",".pem",".key"]:
            raise ValueError("Private/configuration artifacts cannot be bundled by this helper")
        if not source.is_file() or not re.fullmatch(r"[0-9a-f]{64}",item.get("sha256","")):
            raise ValueError("Every allowlisted file needs verified bytes and SHA-256")
        if sha256(source)!=item["sha256"]:
            raise ValueError("Release input checksum mismatch")
        paths.append((source,destination))
    if "README.md" not in names or "LICENSE" not in names:
        raise ValueError("Bundle must include a completed dataset card and data license")
    card=contained(ROOT,cfg["card_path"])
    if not any(a==card and b==Path("README.md") for a,b in paths):
        raise ValueError("card_path must be the allowlisted README source")
    if re.search(r"AUTHOR INPUT|TODO|REPLACE_WITH",card.read_text()):
        raise AuthorInputRequired("Complete the dataset card; do not upload a template")
    if mode=="project":
        for field in ["source_register_path","validation_report_path","croissant_path","croissant_validation_report_path"]:
            item=cfg.get(field)
            if not item or not contained(ROOT,item).is_file():
                raise AuthorInputRequired(f"Supply release evidence: {field}")
        scientific=read_json(contained(ROOT,cfg["validation_report_path"]))
        if scientific.get("release_review_complete") is not True or scientific.get("unresolved_blockers"):
            raise AuthorInputRequired("Complete and document the release review; explain unresolved scientific limits")
        metadata=read_json(contained(ROOT,cfg["croissant_validation_report_path"]))
        if metadata.get("status")!="pass" or not metadata.get("tool") or not metadata.get("checked_at"):
            raise AuthorInputRequired("Supply the actual Croissant validation report")
        if metadata.get("metadata_sha256") != sha256(contained(ROOT,cfg["croissant_path"])):
            raise ValueError("Croissant report does not match the metadata file")
        if not any(a==contained(ROOT,cfg["croissant_path"]) for a,b in paths):
            raise ValueError("Include the validated Croissant file in the bundle")
    target=fresh_output(output)
    entries=[]
    for source,destination in paths:
        dest=contained(target,destination);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,dest)
        entries.append({"path":destination.as_posix(),"bytes":dest.stat().st_size,"sha256":sha256(dest)})
    write_json(target/"release_manifest.json",{
        "dataset_title":cfg["dataset_title"],"data_version":cfg["data_version"],
        "dataset_license":cfg["dataset_license"],"release_kind":mode,"files":entries,
        "uploaded":False,"scientific_certification":False})
    print("Local bundle ready for inspection:",target)
    print("No upload performed.")
    return target


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest",required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    prepare(args.manifest,args.output)
