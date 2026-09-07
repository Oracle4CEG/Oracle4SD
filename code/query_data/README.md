# Query data

Acquire exact inputs and record their provenance.

**First-author task:** Adapt query.py for the actual source. The generic implementation verifies pinned local/HTTPS files. Add source-specific authentication, pagination, retries, rate limits and stopping rules where necessary; document secrets handling outside the repository.

**Start with:** [query.py](query.py).

Run from the repository root, after required upstream stages:

~~~bash
python code/query_data/query.py --config configs/demo.json --run-dir runs/my-demo
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

**Done when:** The acquired version, hashes, counts and failures are explainable.

**Requirement mapping:** [Methods: acquisition](https://www.nature.com/sdata/submission-guidelines); [source and collection provenance](https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting). These links identify the governing requirements;
the task instructions are teaching recommendations. Check the actual submission year.
