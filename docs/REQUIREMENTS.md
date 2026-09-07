# Requirements mapped to author evidence

Policy check: **7 September 2026**. Recheck your submission year.
This table distinguishes venue requirements from this template's teaching recommendations.
Links point directly to official guidance; the prose is a concise interpretation.

| ID and scope | Requirement | Evidence/location |
|---|---|---|
| SD-METHODS · journal | Explain data generation, exact inputs and processing | data/data_source; code/query_data; code/process_data; source register |
| SD-RECORDS · journal | Describe deposited files, formats, structure and fields | data/processed_data; dictionary; manifest |
| SD-QUALITY · journal | Support technical data quality | code/technical_validation; actual validation reports |
| SD-ACCESS · journal | Provide data and code availability statements | release identifiers, access instructions, code commit |
| SD-SCOPE · journal | Keep the descriptor focused on data and technical quality | paper section guide; bounded overview |

Source for SD rows: [Scientific Data submission guidelines](https://www.nature.com/sdata/submission-guidelines).
For repository suitability and controlled resources, consult the [data policies](https://www.nature.com/sdata/policies/data-policies).
An informal repository page alone may not meet the journal's archival requirements.
The supplied teaching example is not a completed data deposit for a paper.

| ID and scope | Requirement | Evidence/location |
|---|---|---|
| ED-ROLE · 2026 E&D | Define a meaningful AI/ML evaluative role, assumptions and limits | Background; task/construct and validity evidence |
| ED-SAMPLE · 2026 E&D | Include a small inspection sample when data exceed 4 GB | documented sample and selection method |
| ED-REVIEW · 2026 E&D | Default double-blind; declare justified dataset-centred exception | current submission form, format and appropriate URLs |
| ED-CODE · 2026 E&D | Code requirements depend on contribution; executable artifacts need accessible code | canonical scripts, commands, environment |

Source: [NeurIPS 2026 E&D call](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets). This is not a workshop-wide rulebook.
For 2026, retain the prescribed double-blind LaTeX layout even when selecting the permitted
single-blind review option. New models and state-of-the-art scores are not prerequisites;
contribution and evidence still matter.

| ID and scope | Requirement | Evidence/location |
|---|---|---|
| ED-ACCESS · dataset contribution | Reviewer-accessible data without a personal request to the PI | tested URL or justified established credentialization |
| ED-META · dataset contribution | Valid Croissant with core and minimal RAI content | completed metadata; validator report |
| ED-COLLECTION · dataset collection | Suitable metadata/access for each component | source and collection map |
| ED-RELEASE · accepted dataset | Public availability by camera-ready under stated provisions | final hosting/version record |

Sources: [hosting guide](https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting) and [reviewer guidelines](https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines).
The template JSON is intentionally incomplete. Platform-generated core metadata still
needs factual and RAI review. Complete the [RAI worksheet](CROISSANT_RAI_WORKSHEET.md).

For an actual NeurIPS submission, complete the [official current checklist](https://neurips.cc/public/guides/PaperChecklist)
with evidence for claims, limitations, reproduction, settings, uncertainty, compute,
asset rights and applicable human-subject issues. This repository's checklist is a teaching aid.

## Template recommendations

Use full commits and data revisions, retain allowed raw inputs, reconcile counts, document
manual steps, preserve adverse evidence and ask an unfamiliar reader to reproduce the workflow.
These are practical author tasks. Passing the software demo, parsing JSON or checking every
box does not establish measurement validity or scientific adequacy.
