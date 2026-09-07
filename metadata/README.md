# Metadata

Provide human-readable records and machine-readable release descriptions.

**First-author task:** Complete the source register, dictionary, claim index and governance records. The Croissant template is intentionally incomplete; remove instructional fields and use the actual specification. Validate core/RAI content and loading, keep the report, and review factual completeness.

**Start with:** [croissant.template.json](croissant.template.json).

Complete [the file manifest](file_manifest.csv) with one row per deposited file or
documented shard. Record bytes and SHA-256 from the actual release, and define what
the record count means for its modality. A restricted resource still needs a clear
access route. Cross-reference the [source register](source_register.csv),
[dictionary](data_dictionary.csv), [processing trace](process_trace.csv) and
[validation plan](validation_plan.csv). Empty CSV headers are author worksheets.


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

**Done when:** The release and metadata describe the same files, rights, fields and limits.

**Requirement mapping:** [Data Records](https://www.nature.com/sdata/submission-guidelines); [required core and minimal RAI metadata](https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting); [dataset-card metadata](https://huggingface.co/docs/hub/datasets-cards). These links identify the governing requirements;
the task instructions are teaching recommendations. Check the actual submission year.
