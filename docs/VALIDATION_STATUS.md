# Validation status and limits

The bundled data are eight invented teaching observations. No empirical Oracle dataset,
measurement study, annotation audit, representativeness assessment or AI/ML benchmark
is included. Scientific adequacy for a future publication remains **NOT_EVALUATED**.

## Checks performed for the template

The 18 local Python 3.12 unit tests pass. They cover complete pipeline arithmetic,
reference comparisons, missing author configuration, checksum mismatch, size limits,
unsafe paths, conflicting duplicates, non-finite numbers, a deliberately wrong unit
conversion, empty validation populations, stale outputs and allowlisted release packaging.
They also check actionable malformed-timestamp errors and refusal to skip template
checks when Python is run with optimizations. Additional tests reject a reference
manifest or scientific-validation report belonging to another data release.

The offline example produces 6 processed records, including 1 missing temperature and
5 numeric temperatures with a mean of 14.0000 degrees Celsius. The source remains
unchanged. Deterministic results are checked against committed SHA-256 references.

Static checks cover required folders, README links, Python/JSON/notebook syntax,
unexecuted notebook outputs and the editable SVG. See
[the validation record](../reports/template_validation.json) for the completed checks.

## Scope of the available workflows

- The runnable notebook teaches all eight stages using synthetic data. All seven
  code cells executed locally in a fresh temporary directory using a public clone
  of the pinned commit, and all five reference files matched. Google Colab's hosted
  runtime has not been separately exercised; see the validation record for scope.
- The general author notebook intentionally requires real project inputs before
  running project operations. Its scientific content has not been completed for you.
- GitHub Actions is provided as a manual workflow. No hosted Actions run is claimed.
- Hugging Face preparation creates a local allowlisted bundle. Nothing has been
  uploaded to Hugging Face by this template setup.
- Croissant and RAI worksheets are incomplete author templates. They are not valid
  metadata for an actual dataset until completed and independently checked.

For your publication, provide actual validation evidence as described in
[Scientific Data's guidance](https://www.nature.com/sdata/submission-guidelines) and,
where applicable, the [NeurIPS dataset hosting requirements](https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting).
A successful software test is evidence about implementation; it does not establish
measurement validity, scientific utility or publication readiness.
