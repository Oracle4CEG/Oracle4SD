"""Validate scaffold structure and local links without treating author placeholders as data."""
from pathlib import Path
import ast
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
REQUIRED=["data/data_source","data/queried_data","data/processed_data","code/query_data",
          "code/process_data","code/analyze_data","code/technical_validation"]


def check():
    if not __debug__:
        raise RuntimeError("Template validation requires assertions; run Python without -O or -OO.")
    for folder in REQUIRED:
        assert (ROOT/folder/"README.md").is_file(),folder
    public=[]
    for f in ROOT.rglob("*"):
        rel=f.relative_to(ROOT)
        if any(x in {".git","runs","__pycache__",".venv"} for x in rel.parts):
            continue
        if f.is_file():
            assert not f.is_symlink(),rel
            assert f.stat().st_size < 5_000_000,rel
            public.append(f)
    for f in public:
        if f.suffix==".py":
            ast.parse(f.read_text())
        elif f.suffix==".json":
            json.loads(f.read_text())
        elif f.suffix==".ipynb":
            nb=json.loads(f.read_text())
            assert nb["nbformat"]==4
            ids=[c["id"] for c in nb["cells"]]
            assert len(ids)==len(set(ids))
            for c in nb["cells"]:
                if c["cell_type"]=="code":
                    ast.parse("".join(c["source"]))
                    assert c["outputs"]==[] and c["execution_count"] is None
        elif f.suffix==".md":
            for link in re.findall(r"\]\(([^ )]+)(?: [^)]*)?\)",f.read_text()):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:",link) or link.startswith("#"):
                    continue
                target=link.split("#",1)[0]
                assert (f.parent/target).exists(),f"{f.relative_to(ROOT)} -> {link}"
    svg=ET.parse(ROOT/"assets/workflow.svg").getroot()
    assert len(svg.findall(".//{http://www.w3.org/2000/svg}text"))>=15
    assert not svg.findall(".//{http://www.w3.org/2000/svg}image")
    assert not svg.findall(".//{http://www.w3.org/2000/svg}foreignObject")
    print(f"Scaffold checks passed: {len(public)} files; required folders, local links, syntax and editable SVG.")
    print("Author placeholders are expected in template files. Project release checks are separate.")


if __name__=="__main__":
    check()
