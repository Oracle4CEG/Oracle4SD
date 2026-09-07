---
license: mit
language:
  - en
tags:
  - synthetic
  - educational
  - scientific-data
size_categories:
  - n<1K
configs:
  - config_name: teaching
    data_files:
      - split: train
        path: data/observations.csv
---

# Synthetic temperature teaching fixture

Six processed, invented observations demonstrate file acquisition, duplicate handling,
missingness, unit conversion, description and bounded validation. There are no real
measurements or human participants. The version is teaching-example-1.

## Source and processing

The eight-row source and executable code are in
[Oracle4SD](https://github.com/sunshineluyao/Oracle4SD).
Processing removes one exact duplicate and one value outside an arbitrary teaching range,
retains one missing value, and converts Celsius to kelvin by adding 273.15.
These rules demonstrate a workflow and are not a recommended scientific cleaning protocol.

## Structure

data/observations.csv contains stable invented IDs, invented group/time, temperature_c,
temperature_k, value_status and the synthetic_teaching origin flag.
metadata/data_dictionary.csv defines fields. Empty temperature fields represent missingness.
The train split is only a default loading convention; no evaluation split or model is provided.

## Uses and limitations

Suitable for software education and testing this template. Not suitable for scientific
inference, real population comparisons, model evaluation or measurement calibration.
Software checks do not validate measurement accuracy, population representativeness or
ML construct validity. All values and timestamps are invented; no population is represented.

## Rights and responsibility

The included MIT licence applies to this synthetic teaching fixture. No upstream research
records are redistributed. It contains no personal information. Its primary misuse risk is
misrepresenting teaching values as empirical findings; retain the synthetic labels.
Report template problems through the Oracle4SD GitHub issues page.

## Version and citation

Use the source repository's exact commit and teaching-example-1 identifier. No DOI or
scientific publication is claimed. This demo bundle is not a NeurIPS dataset submission;
real projects must supply validated Croissant/RAI metadata and domain evidence.
