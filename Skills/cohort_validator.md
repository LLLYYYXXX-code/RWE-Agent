---
name: cohort_validator
description: Export a MIMIC‑IV research cohort to CSV, perform data‑integrity checks, and generate a standardised funnel.json summary. Use after defining a cohort and before any statistical analysis or figure generation.
version: 1.0.0
metadata: {"display_name":"cohort_validator"}
---

---
name: cohort_validator
description: Export a MIMIC‑IV research cohort to CSV, perform data‑integrity checks, and generate a standardised funnel.json summary. Use after defining a cohort and before any statistical analysis or figure generation.
---


# Cohort Validator

## Purpose
This skill exports a defined MIMIC‑IV cohort to a CSV file, validates its structure and contents, computes descriptive statistics, and produces a `funnel.json` artefact for transparent research records.

## When to Use
- After a cohort has been built with `cohort_builder` or a custom SQL query.
- Before proceeding to statistical modelling or generating figures (e.g., with `stats_analysis`, `figure_report`).
- Whenever you need a quick, standardised quality‑check of the extracted data.

## Workflow

### 1. Cohort Export
- Execute the cohort query using the existing database connection (configured via the `MIMIC_IV_DB` environment variable).
- Write the result set to `shared/cohort.csv` with UTF‑8 encoding, no row index, and a header row.
- Ensure the CSV does not contain any SQL‑level statement leftovers (e.g., `SET` commands). If present, they will be handled in the loading step.

### 2. Data Loading & Cleaning
- Read `shared/cohort.csv` with `pandas.read_csv()`.
  - Use `comment='S'` to skip rows that might contain SQL statement fragments (e.g., starting with `SET`).
  - Set `low_memory=False` or explicitly specify `dtype` where appropriate to avoid mixed‑type warnings.
- Report the loaded dimensions (`shape`).

### 3. Column Verification
- Confirm the presence of required columns: `subject_id`, `stay_id`, `hadm_id`, `study_group`.
- Identify binary outcome columns (e.g., `mortality_28d`, `icu_mortality`, `hospital_mortality`) and any continuous covariates mentioned in the study protocol.
- If any mandatory column is missing, log the error and halt further validation.

### 4. Descriptive Statistics
Print (and optionally save to a log file) the following summary:

- **Total records** – raw count of rows.
- **Group distribution** – absolute counts and percentages for `study_group` (or equivalent arm variable).
- **Outcome distribution** – for each binary outcome: counts of `0`/`1`, incidence rate (proportion of `1`), and missing count.
- **Continuous variables** – for age, SOFA score, vital signs, lab values, etc.:
  - Median, mean, standard deviation, minimum, maximum
  - Percentage of missing values
- **Categorical variables** – category counts and missing percentage.
- **Missing‑data flag** – clearly highlight any variable with >5% missingness.

### 5. Generate `funnel.json`
Create or overwrite `shared/funnel.json` with the following keys:

- `cohort_size`: total number of records
- `group_sizes`: dictionary mapping group name → count
- `outcome_rates`: dictionary mapping outcome name → incidence proportion
- `continuous_summary`: dictionary of variable → `{median, mean, std, min, max, missing_pct}`
- `exclusions`: list (empty, or pre‑populated if earlier filtering steps were tracked)

Save the file and print a confirmation.

### 6. Report & Next Steps
- Summarise key findings: sample‑size match against the study design, group balance, and any unusual missing data patterns.
- If the cohort size deviates from the expected target, alert the user and recommend revisiting the cohort query.
- Remind that only descriptive statistics are performed — no hypothesis testing is done at this stage.

## Integration
This skill is designed to run after `cohort_builder` and before `stats_analysis` or `figure_report`, forming a reproducible pipeline:

1. `cohort_builder` → define and fetch the cohort
2. `cohort_validator` → export, validate, and document
3. `stats_analysis` / `figure_report` → analyse and visualise

## Notes
- Database connection parameters (`MIMIC_IV_DB`) are expected to be set in the environment; credentials are never stored in the skill.
- All outputs are deterministic and do not rely on random seeds.
- The `funnel.json` captures a snapshot of the cohort at validation time and should be committed alongside the results.
