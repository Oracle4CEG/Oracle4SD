"""Independent arithmetic expectations and negative-path tests using synthetic fixtures only."""
from pathlib import Path
import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"code"))
from common import AuthorInputRequired, contained, read_csv, read_json, sha256, write_csv, write_json


def module(name,path):
    source=ROOT/path
    if not source.is_file():
        raise ImportError(f"Cannot load test module {name}: missing source {source}")
    spec=importlib.util.spec_from_file_location(name,source)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load test module {name} from {source}: no import loader")
    loaded=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


pipeline=module("pipeline","scripts/run_pipeline.py")
query=module("query","code/query_data/query.py")
processing=module("processing","code/process_data/process.py")
validation=module("validation","code/technical_validation/validate.py")
packaging=module("packaging","scripts/prepare_huggingface.py")


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.base=Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_demo(self,name="run"):
        return pipeline.run(ROOT/"configs/demo.json",self.base/name)

    def altered_config(self,mutator):
        cfg=read_json(ROOT/"configs/demo.json")
        mutator(cfg)
        path=self.base/"config.json";write_json(path,cfg)
        return path

    def test_complete_run_has_independent_arithmetic_and_no_scientific_claim(self):
        out=self.run_demo()
        rows=read_csv(out/"processed_data/observations.csv")
        by_id={row["observation_id"]:row for row in rows}
        self.assertEqual(set(by_id),{"demo-001","demo-002","demo-003","demo-005","demo-006","demo-007"})
        self.assertEqual(by_id["demo-001"]["temperature_k"],"283.15")
        self.assertEqual(by_id["demo-006"]["temperature_k"],"268.15")
        self.assertEqual(by_id["demo-003"]["temperature_k"],"")
        summary=read_csv(out/"analysis/summary.csv")[0]
        self.assertEqual((summary["n_records"],summary["n_nonmissing"],summary["n_missing"]),("6","5","1"))
        self.assertEqual(summary["mean_temperature_c"],"14.0000")
        self.assertEqual(read_json(out/"reports/validation.json")["scientific_readiness"],"not_evaluated")
        self.assertEqual(sha256(out/"queried_data/observations.csv"),sha256(ROOT/"data/data_source/demo/observations.csv"))

    def test_blank_project_stops_before_outputs(self):
        target=self.base/"missing"
        with self.assertRaises(AuthorInputRequired):
            pipeline.run(ROOT/"configs/project.template.json",target)
        self.assertFalse(target.exists())

    def test_wrong_checksum_rejected_and_partial_removed(self):
        cfg=self.altered_config(lambda d:d["sources"][0].update(sha256="0"*64))
        target=self.base/"bad"
        with self.assertRaisesRegex(ValueError,"checksum"):
            query.acquire(cfg,target)
        self.assertFalse(list(target.rglob("*.partial")))

    def test_size_cap(self):
        cfg=self.altered_config(lambda d:d["sources"][0].update(max_bytes=1))
        with self.assertRaisesRegex(ValueError,"oversized"):
            query.acquire(cfg,self.base/"small")

    def test_path_escape_and_symlink(self):
        with self.assertRaises(ValueError): contained(self.base,"../escape")
        (self.base/"link").symlink_to(ROOT/"LICENSE")
        with self.assertRaises(ValueError): contained(self.base,"link")

    def test_conflicting_duplicate_is_not_silently_discarded(self):
        target=self.base/"conflict"
        query.acquire(ROOT/"configs/demo.json",target)
        raw=target/"queried_data/observations.csv"
        rows=read_csv(raw);rows[2]["temperature_c"]="21"
        write_csv(raw,list(rows[0]),rows)
        with self.assertRaisesRegex(ValueError,"Conflicting duplicate"):
            processing.process(ROOT/"configs/demo.json",target)

    def test_nonfinite_value_rejected(self):
        target=self.base/"nonfinite";query.acquire(ROOT/"configs/demo.json",target)
        raw=target/"queried_data/observations.csv"
        rows=read_csv(raw);rows[0]["temperature_c"]="NaN"
        write_csv(raw,list(rows[0]),rows)
        with self.assertRaisesRegex(ValueError,"Non-finite"):
            processing.process(ROOT/"configs/demo.json",target)

    def test_invalid_timestamp_has_actionable_message(self):
        target=self.base/"timestamp";query.acquire(ROOT/"configs/demo.json",target)
        raw=target/"queried_data/observations.csv"
        rows=read_csv(raw);rows[0]["timestamp_utc"]="not-a-time"
        write_csv(raw,list(rows[0]),rows)
        with self.assertRaisesRegex(ValueError,"ISO 8601 UTC"):
            processing.process(ROOT/"configs/demo.json",target)
        self.assertFalse((target/"processed_data/observations.csv").exists())

    def test_optimized_python_cannot_skip_template_checks(self):
        result=subprocess.run([sys.executable,"-O",str(ROOT/"scripts/check_template.py")],
                              capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn("run Python without -O",result.stderr)
        self.assertNotIn("Scaffold checks passed",result.stdout)

    def test_wrong_conversion_detected(self):
        target=self.run_demo()
        path=target/"processed_data/observations.csv";rows=read_csv(path)
        rows[0]["temperature_k"]="300.00";write_csv(path,list(rows[0]),rows)
        report=validation.validate(ROOT/"configs/demo.json",target)
        self.assertEqual(next(x for x in report["checks"] if x["check"]=="unit_conversion")["status"],"fail")

    def test_empty_population_not_passed(self):
        target=self.run_demo()
        path=target/"processed_data/observations.csv";rows=read_csv(path)
        write_csv(path,list(rows[0]),[])
        report=validation.validate(ROOT/"configs/demo.json",target)
        self.assertTrue(all(x["status"]=="not_evaluated" for x in report["checks"]))

    def test_wrong_reference_detected(self):
        target=self.run_demo()
        manifest=copy.deepcopy(read_json(ROOT/"tests/reference/demo_manifest.json"))
        manifest["files"][0]["sha256"]="0"*64
        self.assertEqual(pipeline.compare(target,manifest)[0]["status"],"fail")

    def test_wrong_reference_data_version_stops_before_outputs(self):
        cfg=self.altered_config(lambda d:d.update(data_version="teaching-example-2"))
        target=self.base/"wrong_version"
        with self.assertRaisesRegex(ValueError,"Reference data_version"):
            pipeline.run(cfg,target)
        self.assertFalse(target.exists())

    def test_stale_output_rejected(self):
        target=self.run_demo()
        with self.assertRaises(FileExistsError):
            pipeline.run(ROOT/"configs/demo.json",target)

    def test_demo_bundle_allowlist(self):
        target=packaging.prepare(ROOT/"configs/huggingface.demo.json",self.base/"bundle")
        files={p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()}
        self.assertEqual(files,{"README.md","LICENSE","data/observations.csv",
                                "metadata/data_dictionary.csv","release_manifest.json"})
        self.assertFalse(read_json(target/"release_manifest.json")["uploaded"])

    def test_project_bundle_stops_with_unfinished_inputs(self):
        target=self.base/"project_bundle"
        with self.assertRaises(AuthorInputRequired):
            packaging.prepare(ROOT/"configs/huggingface.project.template.json",target)
        self.assertFalse(target.exists())

    def test_project_bundle_rejects_evidence_from_another_data_version(self):
        cfg=read_json(ROOT/"configs/huggingface.demo.json")
        for item in cfg["files"]:
            dest=self.base/item["source"];dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/item["source"],dest)
        cfg.update(release_kind="project",data_version="test-v2",
                   source_register_path="evidence/source_register.csv",
                   validation_report_path="evidence/scientific.json",
                   croissant_path="evidence/croissant.json",
                   croissant_validation_report_path="evidence/metadata_check.json")
        evidence=self.base/"evidence";evidence.mkdir()
        (evidence/"source_register.csv").write_text("source_id\nsynthetic-test-fixture\n")
        write_json(evidence/"scientific.json",{
            "data_version":"test-v1","release_review_complete":True,"unresolved_blockers":[]})
        write_json(evidence/"croissant.json",{})
        write_json(evidence/"metadata_check.json",{})
        manifest=self.base/"release.json";write_json(manifest,cfg)
        target=self.base/"stale_evidence_bundle"
        with patch.object(packaging,"ROOT",self.base):
            with self.assertRaisesRegex(ValueError,"Scientific validation report data_version"):
                packaging.prepare(manifest,target)
        self.assertFalse(target.exists())

    def test_release_checksum_mismatch(self):
        cfg=read_json(ROOT/"configs/huggingface.demo.json")
        cfg["files"][0]["sha256"]="0"*64
        path=self.base/"release.json";write_json(path,cfg)
        with self.assertRaisesRegex(ValueError,"checksum"):
            packaging.prepare(path,self.base/"bundle")


if __name__=="__main__":
    unittest.main()
