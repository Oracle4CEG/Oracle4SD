# First-author workbook

**Project / first author / corresponding author:** [AUTHOR INPUT]  
**Data release / code commit / manuscript version:** [AUTHOR INPUT]  
**Target venue, year and policy-check date:** [AUTHOR INPUT]

Deliver a manuscript, data release and code tutorial that a scientist outside the team
can understand and examine. This workbook organizes the work; it supplies no missing
measurements, approvals, permissions or scientific results.

## 1. Define the resource and contribution

Answer three questions before drafting: What does one record represent? What data need
does this resource address? What evidence supports its proposed use?
Distinguish new measurements, inherited data, new annotations, transformed data and
synthetic content. Quantify them with consistent units and state overlap/dependence.
Do not treat more rows or more documentation as sufficient evidence of a scientific contribution.

For a NeurIPS E&D submission, specify a meaningful AI/ML evaluative role: task, construct,
population, reference information, assumptions and limits. A general Scientific Data resource
does not automatically fit that track. A new model or state-of-the-art score is not a
prerequisite. Consult the [2026 call](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets).

Maintain a claim register with scope, release, evidence, code, uncertainty, counterevidence
and status. Distinguish measured findings, method choices, interpretations and proposed uses.
Describe a use as demonstrated only where there is supporting evidence.

## 2. Connect the paper, release and notebook

Fill actual paths and permanent URLs. GitHub source links should identify the exact commit;
download URLs must return the intended bytes. A homepage alone does not locate code.

| Manuscript section | Colab part | First-author evidence | Reader's check |
|---|---|---|---|
| Background & Summary | I | Plain-language context, comparison, contribution and scope | Can a newcomer explain the data need and record unit? |
| Methods: inputs | II–III | Source metadata, rights, exact query or protocol | Can the same permitted inputs be obtained? |
| Methods: acquisition checks | IV | Raw inventory, anomalies, provenance and scope | Did acquisition produce the intended material? |
| Methods: processing | V | Canonical code, parameters, lineage and logs | Can every transformation and count change be explained? |
| Data Records | VI | Release manifest, relations, dictionary and citation | Can a reader locate and interpret each component? |
| Optional Data Overview | VII | Selected descriptive outputs with denominators | Does this orient the reader without becoming research analysis? |
| Technical Validation | VIII | Scientific tests, references, uncertainty, failures and rerun | What does each check actually establish? |
| Usage Notes | I, III–VIII | Access, loader, interpretation, limitations and support | Can an independent reader use the data correctly? |
| Availability statements | I, II, VI | Matching data identifier, release, code commit and access | Do all artifacts identify the same resource? |
| Declarations | II and source records | Governance, author roles, interests and funding | Are statements supported by responsible records? |

The companion notebook is a blank authoring template. Required project configuration
intentionally stops execution before acquisition. Fill its Markdown prompts and configuration,
connect the actual scripts, and document verified expected outputs.
For images, text, signals, graphs or other non-tabular data, supply the appropriate
inspection adapter. Do not force the modality into an inappropriate table.

## 3. Populate the evidence registers

CSV worksheets contain headers and, for the release checklist, unevaluated task rows.
They are not data or completed evidence. Record unknown information explicitly with a reason.

| Worksheet | Required content |
|---|---|
| source_register.csv | Versions, acquisition, rights, access, sensitivity and provenance |
| resource_comparison.csv | Cited, aligned comparisons and qualified differences |
| process_trace.csv | Stage inputs/outputs, rules, count changes and reasons |
| file_manifest.csv | Real files, sizes, formats, units, hashes and access |
| data_dictionary.csv | Definitions, types/shapes, units, missing codes, keys and derivation |
| validation_plan.csv | Claim, reference, sampling, metric, criterion, outcome and limit |
| reproduction_record.csv | Independent environment, commands, comparison and discrepancies |
| claim_evidence.csv | Claim linked to release, code, output and supported wording |
| issue_log.csv | Artifact-specific questions, revisions, owners and resolutions |
| release_checklist.csv | Applicability, evidence and status for readiness tasks |

Keep tokens, personal consent forms and confidential records outside public artifacts.
Public visibility and redistribution permission are separate facts.
Use public summaries and transparent controlled-access procedures where appropriate.

## 4. Test scientific failure modes

Ask how data could mislead a reader even if every file loads: selection bias, unstable
measurements, shared annotation errors, duplicate subjects across partitions, changed
source definitions or incorrect units. Choose references and tests for those failures.

Define the tested population and sampling design. Record examined and failing counts,
and distinguish sample evidence from full-release checks. Give criteria and their rationale,
including when they were chosen. Use uncertainty appropriate to the design, accounting
for clustering or repeated observations where relevant. Retain adverse findings.

| Evidence | What it supports | What remains to establish |
|---|---|---|
| File checksum | Identity relative to reference bytes | Correctness of the reference |
| Successful execution | A command finished in one environment | Correct records and quantities |
| Schema check | Structure satisfies specified rules | Correct meanings and measurement assumptions |
| Agreement study | Agreement under its reference and design | Reference independence and suitability |
| Reproduction | Specific outputs regenerated within defined tolerance | Validity for broader populations or uses |
| Metadata validation | The validator's checks on metadata | Truthful descriptions and scientific adequacy |

For applicable ML evaluation, document splits, baselines, tuning, metrics, seeds,
uncertainty and compute, with leakage/contamination checks and relevant error analysis.
Keep extended research experiments in an appropriate research manuscript; retain in the
Data Descriptor only checks that directly support technical data quality.
Use the [NeurIPS checklist](https://neurips.cc/public/guides/PaperChecklist) as an evidence
inventory. An actual NeurIPS submission needs its official current form, honest answers
and supporting locations. This workbook does not replace it.

## 5. Work through three iterations

Set dates for each project; no fixed student, topic or publication calendar is built in.

| Iteration | Date | Deliverables | Completion evidence |
|---|---|---|---|
| First internal draft | [AUTHOR INPUT] | All sections; source/rights register; file map; permitted sample run; validation plan | Each missing item has a specific task and owner |
| Second iteration | [AUTHOR INPUT] | Revised paper; populated metadata; actual validation; independent tutorial run | Issues resolved or limits recorded; claims traceable |
| Preprint/submission release | [AUTHOR INPUT] | Clean manuscript; matching data/code; completed notebook; declarations | Coauthor agreement; no placeholders; exact versions and access verified |

Formatting completion does not establish scientific completion.
If evidence contradicts a claim, revise the claim or collect justified additional evidence.
Do not drop failed checks or mark untested dimensions passed.

## 6. Review three artifacts independently

Ask a colleague who did not build the pipeline to review the paper, dataset and code
separately. For each, record (A) what is clear and supported, (B) what remains unclear
or unverifiable, and (C) one to three specific improvements.
This adapts the supplied educational NeurIPS-like peer-evaluation form, not an official review form.

Cite pages, fields, files, commands, outputs, commits or URLs. Test public access while
logged out. For controlled data, test the documented eligible-user route and record limitations.
Run the notebook from a fresh runtime using only published instructions.
Record sample/full scope, resources, failures and output differences.
Compare using stable keys and scientifically justified tolerances where byte equality is unsuitable.

## 7. Return a coherent handoff

Provide the paper, persistent data release, exact code, completed notebook, validation
reports and issue log together. Their counts, identifiers, definitions, licences and limits
must agree. Check related-publication and simultaneous-submission policies; disclose overlap.
Anticipated citations or acceptance elsewhere do not replace data-quality evidence.
The template organizes readiness; editors and reviewers determine scientific adequacy.
