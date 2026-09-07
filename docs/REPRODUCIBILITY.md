# Reproduce the teaching workflow

The example is fully local after cloning. Python 3.12 and its standard library are sufficient.
It uses eight invented observations, not actual study data.

~~~bash
python scripts/run_pipeline.py
~~~

Every invocation creates a new runs/demo-* directory. To name it yourself:

~~~bash
python scripts/run_pipeline.py --output runs/my-first-demo
~~~

Use a new directory for another run. Existing output directories are rejected to prevent
stale results from being mistaken for a successful run.

| Stage | Command after creating a fresh run directory | Output relative to run directory |
|---|---|---|
| Query | python code/query_data/query.py --config configs/demo.json --run-dir runs/manual | queried_data/observations.csv; reports/acquisition.json |
| Process | python code/process_data/process.py --config configs/demo.json --run-dir runs/manual | processed_data/observations.csv; reports/processing.json |
| Analyze | python code/analyze_data/analyze.py --config configs/demo.json --run-dir runs/manual | analysis/summary.csv |
| Validate | python code/technical_validation/validate.py --config configs/demo.json --run-dir runs/manual | reports/validation.json |

The top-level runner also compares selected deterministic outputs with tests/reference/demo_manifest.json.
It records Python, platform, code commit, elapsed time and sample scope separately, so
runtime-specific metadata do not create false reference mismatches.
The data source, archived queried/processed teaching files and expected reports are all
included in the repository.

## Expected observations

Eight input rows become six processed rows: one exact duplicate and one out-of-range value
are removed by explicit teaching rules. One missing value is retained. The five numeric
values sum to 70 degrees Celsius and average 14.0000. Example unit checks include
10 Celsius → 283.15 kelvin and −5 Celsius → 268.15 kelvin.
These arithmetic examples do not support a claim about a physical population.

The validation report separates software checks from measurement accuracy, population
representativeness and ML construct validity, which remain not evaluated.
No statistical significance, causal effect or model performance is inferred.

## For the real project

Complete configs/project.template.json and adapt the actual scientific stage code.
The current runner explicitly rejects an unimplemented project adapter.
Document the unit, population, reference information, assumptions, missing values,
parameters, seeds, software lock, hardware, commands, outputs and interpretation.
Record immutable external data locations and checksums for files unsuitable for Git.

Have another researcher use a fresh environment and compare to a separate archived run
using stable keys and justified tolerances. A sample-only rerun must be labelled as such.
Use [Scientific Data Methods and Technical Validation](https://www.nature.com/sdata/submission-guidelines)
and [NeurIPS reproducibility guidance](https://neurips.cc/public/guides/PaperChecklist).
