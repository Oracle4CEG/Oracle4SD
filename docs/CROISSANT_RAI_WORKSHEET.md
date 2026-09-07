# Croissant and Responsible AI worksheet

This planning worksheet is not a Croissant JSON file. Do not upload it as submission metadata.
Use the [hosting guide](https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting)
for the current specification, editor and validator links. Start from the actual release's
metadata export where available, then review it.
Core metadata must consistently identify the dataset, access, licence, files and records.
Confirm file extraction and field mappings against real artifacts using the
[MLCommons Croissant 1.1 specification](https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html).
Use the [MLCommons RAI specification](https://docs.mlcommons.org/croissant/docs/croissant-rai-spec.html)
for the Responsible AI vocabulary. The hosting guide currently links the
[Croissant checker](https://huggingface.co/spaces/JoaquinVanschoren/croissant-checker);
record the actual tool version/date and report.

**Dataset / version / metadata path / owner / check date:** [AUTHOR INPUT]

## Evidence questions

The names identify the current minimal RAI and provenance topics. Check permitted
structure and placement in the specification before encoding. Explain inapplicability;
an empty field does not supply that explanation.

| Field or topic | First-author input | Supporting evidence |
|---|---|---|
| rai:dataLimitations | Limits and discouraged uses | Validation and Usage Notes |
| rai:dataBiases | Known/suspected selection, source, annotation and representation effects | Sampling and bias assessment |
| rai:personalSensitiveInformation | Sensitive content present or assessed absent, with basis and handling | Governance and access records |
| rai:dataUseCases | Construct, evidence-supported uses and untested uses | Claim register and validity study |
| rai:dataSocialImpact | Plausible benefits/harms, affected groups and actual mitigations | Assessment and use guidance |
| rai:hasSyntheticData | Truthful boolean and explanation of generated content | Generator configuration |
| prov:wasDerivedFrom | Exact upstream resources or seeds | Source register |
| prov:wasGeneratedBy | Collection, preprocessing and annotation activities, agents and protocols | Process trace |

## Validation record

| Item | Evidence to enter |
|---|---|
| Metadata version/checksum | [AUTHOR INPUT] |
| Specification and validator version/date | [AUTHOR INPUT] |
| Syntax/schema checks | [AUTHOR INPUT: outcome and report] |
| Record/file mapping | [AUTHOR INPUT: checked items and exceptions] |
| Access/loading | [AUTHOR INPUT: scope, outcome and restrictions] |
| RAI factual review | [AUTHOR INPUT: reviewer, evidence and corrections] |
| Paper/data/metadata consistency | [AUTHOR INPUT: same release, licence and scope] |
| Final submission file and dataset URL | [AUTHOR INPUT] |

Parsing JSON establishes syntax only. Do not describe it as Croissant validation.
Do not copy consent, bias or intended-use statements between unrelated resources.
For controlled data, document permitted loading and unexecuted checks.
