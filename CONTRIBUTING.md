# Contributing

Read [the first-author guide](docs/FIRST_AUTHOR_GUIDE.md), work on a branch, and open a pull
request explaining the scientific reason for the change. Keep the existing licence notice.
Run the local checks below and report failures and scope honestly.

~~~bash
python scripts/check_template.py
python -m unittest discover -s tests -v
python scripts/run_pipeline.py
~~~

Update dictionaries, manifests, notebooks and instructions when a schema or method changes.
Never approve a reference mismatch by simply overwriting its expected hash. Record the reason,
independent review and data/code version. Keep confidential material and credentials out of commits.
For project datasets, follow [Scientific Data](https://www.nature.com/sdata/submission-guidelines) and [NeurIPS dataset guidance](https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting).

This repository's instructions are educational. Scientific adequacy requires project-specific evidence.
