# Technical validation

Test scientific failure modes as well as file and software integrity.

**First-author task:** Define quality claims, test population, sampling, sample size, independent reference, metric, criterion/rationale, timing, uncertainty and failures. Distinguish pass, fail, not evaluated and justified not applicable. Add discipline-specific validity studies; successful execution and correct metadata do not establish measurement validity.

**Start with:** [validate.py](validate.py).

Run from the repository root, after required upstream stages:

~~~bash
python code/technical_validation/validate.py --config configs/demo.json --run-dir runs/my-demo
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

**Done when:** Every claimed quality dimension has evidence and an honest limit.

**Requirement mapping:** [Technical Validation](https://www.nature.com/sdata/submission-guidelines); [quality and expert judgment](https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines); [Croissant validation](https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting). These links identify the governing requirements;
the task instructions are teaching recommendations. Check the actual submission year.
