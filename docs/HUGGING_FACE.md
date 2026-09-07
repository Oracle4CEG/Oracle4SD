# Prepare a dataset for Hugging Face

The GitHub repository keeps code and instructions. The dataset repository should contain
only permitted data, its Dataset Card, licences and metadata. Uploading all of GitHub would
mix teaching fixtures, author templates, tests and unfinished project content.

## 1. Rehearse packaging locally

~~~bash
python scripts/prepare_huggingface.py --manifest configs/huggingface.demo.json --output runs/hf-demo
~~~

This creates a small **synthetic teaching** bundle and performs no upload.
It includes only the selected processed CSV, completed teaching Dataset Card, dictionary
and MIT licence. Inspect every file and the generated checksum manifest.
Use a new output directory on each run.

## 2. Complete the real project

Copy [the card template](../templates/DATASET_CARD.md) and
[the project release manifest](../configs/huggingface.project.template.json).
Complete source/rights records, actual scientific validation, the data licence, Croissant
metadata and the actual validator report. The package must include the completed card
as README.md, data licence as LICENSE, selected data and validated metadata.
Each allowlisted entry has source, destination and a verified SHA-256.

The packaging helper checks explicit inputs, permissions confirmation, hashes and
evidence records. It does not independently certify licences or science and does not
run the external Croissant validator. See [metadata instructions](../metadata/README.md).
Keep data-version and metadata-version changes consistent; revalidate after changing metadata.

Use [Hugging Face Dataset Cards](https://huggingface.co/docs/hub/datasets-cards) for the YAML header and descriptions.
Set explicit data_files patterns so dictionaries and source CSVs are not accidentally
loaded as observations. Document split meaning: the teaching card's default train split
is a loading convention, not a scientifically designed evaluation partition.

## 3. Upload only after inspecting the real bundle

Create the intended dataset repository in your own Hugging Face account with appropriate
visibility/access. Install the current huggingface_hub client in a separate environment
and record its tested version. The commands below are a manual publication step:

~~~bash
hf auth login
hf upload YOUR_ACCOUNT/YOUR_DATASET runs/your-approved-bundle . --repo-type dataset
~~~

Replace both paths deliberately. Use interactive authentication or your platform's
secret manager; do not store a token in the notebook or repository.
See the [official upload guide](https://huggingface.co/docs/huggingface_hub/guides/upload).
No upload is performed by this template or by its tests.

## 4. Verify the hosted release

Test downloads, dataset-card rendering, actual loading, field types, units and access.
Record the resulting immutable data revision and persistent archival identifier where
appropriate. Update paper, README, source register, Colab and Croissant consistently.
Re-run the official metadata validator on the final hosted resource and retain the report.
For NeurIPS, follow the [hosting requirements](https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting); for Scientific Data, confirm the
host and any separate archival deposit meet its [data policy](https://www.nature.com/sdata/policies/data-policies).
Do not assume a platform upload alone completes either venue's requirements.
