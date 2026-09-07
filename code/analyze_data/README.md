# Analyze data

Produce reproducible summaries or justified project analyses.

**First-author task:** Define questions, populations, denominators, units, missingness, uncertainty and interpretation. Save the input/version-to-output map. The Data Descriptor should retain only its permitted overview and technical-quality checks; place extended substantive analyses in a suitable research paper.

**Start with:** [analyze.py](analyze.py).

Run from the repository root, after required upstream stages:

~~~bash
python code/analyze_data/analyze.py --config configs/demo.json --run-dir runs/my-demo
~~~

For the complete ordered example, use <code>python scripts/run_pipeline.py</code>.


## Author inputs for the completed project

| Item | Fill with verified information |
|---|---|
| Scientific purpose and observation unit | AUTHOR INPUT |
| Exact inputs, versions and source/DOI URLs | AUTHOR INPUT |
| Permanent GitHub code or folder links | AUTHOR INPUT |
| Commands, parameters and manual prerequisites | AUTHOR INPUT |
| Expected output paths, counts and units | AUTHOR INPUT |
| Access, rights, limitations and untested dimensions | AUTHOR INPUT |
| Independent check and evidence location | AUTHOR INPUT |

**Done when:** Each output has an exact command, evidence path and bounded interpretation.

**Requirement mapping:** [Data Overview and Technical Validation](https://www.nature.com/sdata/submission-guidelines); [meaningful evaluative purpose](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets). These links identify the governing requirements;
the task instructions are teaching recommendations. Check the actual submission year.
