# Process data

Explain and implement scientific transformations in execution order.

**First-author task:** Replace the teaching adapter with justified rules for your modality. Document cleaning, duplicates, missing values, units, joins, annotation, derived fields and information loss. Preserve lineage and reconcile aggregation/expansion as well as exclusions. For ML uses, prevent dependent records and fitted preprocessing from leaking between partitions.

**Start with:** [process.py](process.py).

Run from the repository root, after required upstream stages:

~~~bash
python code/process_data/process.py --config configs/demo.json --run-dir runs/my-demo
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

**Done when:** Every output and count change traces to a rule, configuration and source.

**Requirement mapping:** [Methods: computational processing](https://www.nature.com/sdata/submission-guidelines); [experimental settings and reproducibility](https://neurips.cc/public/guides/PaperChecklist). These links identify the governing requirements;
the task instructions are teaching recommendations. Check the actual submission year.
