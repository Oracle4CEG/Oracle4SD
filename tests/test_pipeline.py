"""Independent arithmetic expectations and negative-path tests using synthetic fixtures only."""
from pathlib import Path
import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"code"))
from common import AuthorInputRequired, contained, read_csv, read_json, sha256, write_csv, write_json


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
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

    def test_release_checksum_mismatch(self):
        cfg=read_json(ROOT/"configs/huggingface.demo.json")
        cfg["files"][0]["sha256"]="0"*64
        path=self.base/"release.json";write_json(path,cfg)
        with self.assertRaisesRegex(ValueError,"checksum"):
            packaging.prepare(path,self.base/"bundle")


if __name__=="__main__":
    unittest.main()
