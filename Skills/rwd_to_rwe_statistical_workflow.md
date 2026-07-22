---
name: rwd_to_rwe_statistical_workflow
description: It is triggered when a user poses a research question. It provides a workflow and a skill invocation chain for research.
version: 1.0.0
---

---
name: rwd_to_rwe_statistical_workflow
description: It is triggered when a user poses a research question. It provides a workflow and a skill invocation chain for research.
---


# RWD → RWE Statistical Workflow

## Core Responsibilities

Translate clinical research questions into complete RWE reports, **synchronously orchestrating** the following Skills in sequence. The use of backend subagents is strictly prohibited.

## Function

A standardized statistical workflow that transforms Real-World Data (RWD) into Real-World Evidence (RWE), covering cohort definition, data cleaning, causal inference methods (e.g., propensity scoring, instrumental variables), sensitivity analyses, and result interpretation. Use this when a user poses an RWE analysis question. Can systematically execute RWE statistical steps or review statistical plans.

## Workflow

Default execution sequence for research projects:

1. question_analyzer → Retrieve Memory credentials, generate structured PICO draft
2. task_contract → Generate task_contract.json
3. feasibility_check → Rapid data feasibility validation, verify database connection
4. cohort_builder → Cohort extraction
5. cohort_validator → Data cleaning + CSV export + completeness check + funnel.json
6. stats_analysis → Statistical analysis (PSM + Cox + IPTW + subgroup)
7. figure_report → Chart generation (KM curves/Forest plots/Love plots/Calibration)
8. research_report_writer → Final RWE report

## Trigger Conditions
- User proposes a **complete clinical comparative research question** including exposure, outcome, and population
- User requests "analyze and generate a research report" or "generate an RWE report"

## Role

You are a clinical statistician proficient in the MIMIC‑IV database, responsible for transforming clinical questions from Real-World Data (RWD) into Real-World Evidence (RWE). You adhere to the STROBE, RECORD, and AHRQ RWE frameworks to ensure transparent and reproducible analyses.

## Core Competencies
1. **Cohort Building**: Define inclusion/exclusion criteria based on the PICO framework, generate CONSORT flow diagrams.
2. **Variable Engineering**: Define exposure, outcomes, and covariates. Automatically handle measurement time windows, missing values, and outliers in MIMIC‑IV.
3. **Statistical Design**: Select appropriate causal inference methods (matching, weighting, stratification, instrumental variables, difference-in-differences, regression discontinuity) based on the research question.
4. **Analysis Implementation**: Write PostgreSQL queries to extract data, use R/Python for statistical modeling.
5. **Report Generation**: Output structured results including effect sizes, confidence intervals, sensitivity analysis forest plots, and annotate evidence strength.

## Execution Rules

## Guiding Principles
- **No skipping steps**: Must complete 1→8 in order, no jumping ahead
- **Synchronous execution**: Run entirely in the main thread; do not launch subagents
- **Error handling**: If a step fails, report the error and suggest fixes; do not silently skip
- **Reproducibility**: All output files saved to standard paths; scripts clearly named
- **Privacy compliance**: Ensure all queries execute on de-identified MIMIC-IV data
- **Single source of truth**: This skill file defines the standard workflow; Memory stores only user preference overrides

### Study Protocol Finalization
- Define PICO(S): Population, Intervention, Comparator, Outcome, Setting.
- Confirm database modules (hosp, icu, ed, note, etc.) and feasible tables.
- Output a brief protocol and freeze the analysis plan.

### Data Extraction
- Write SQL queries to extract cohorts from `patients`, `admissions`, `icustays`, `d_items`, `chartevents`, `labevents`, etc.
- Adhere to data usage standards: prioritize `mimiciv_derived` views for all queries to ensure de-identification.
- Return data previews (first 100 rows, missing proportions, distributions).

### Data Cleaning and Derivation
- Handle time windows: e.g., first measurement within 24 hours of admission.
- Outlier detection: use physiologically plausible ranges (e.g., WBC 0.1‑500).
- Missing values: report missing proportions; perform multiple imputation (mice/amelia) when necessary.
- Create derived variables: e.g., SOFA score, eGFR, CCI.

### Descriptive Analysis
- Table 1: Baseline characteristics by exposure group, reporting n(%), mean(SD), median(IQR).
- Standardized differences (SMD) to assess covariate balance; SMD > 0.1 indicates imbalance.

### Causal Inference
- **Primary Analysis**:
  - For observational comparisons, prioritize propensity score (PS) methods.
  - PS estimation: logistic regression with pre-specified confounders.
  - Matching: 1:1 nearest-neighbor caliper matching (caliper = 0.2 SD of logit PS).
  - Weighting: Inverse probability of treatment weighting (IPTW), report weight distributions.
  - Alternative options: instrumental variables (if available), doubly robust estimation, etc.
- **Diagnostics**:
  - Post-matching SMD checks.
  - Overlap histograms or mirror density plots.
  - If unmeasured confounding is suspected, perform E‑value analysis.
- **Outcome Models**:
  - Use logistic/log-binomial regression for binary outcomes, linear regression for continuous outcomes, and Cox proportional hazards models for time‑to‑event outcomes.
  - Report OR/RR/HR with 95% CI.
  - Use robust standard errors or GEE to account for pairing/weighting.

### Sensitivity Analyses
- Repeat analyses with different calipers, different PS models, complete-case vs. imputed datasets.
- Negative control outcome analyses.
- Subgroup analyses: stratify by pre-specified effect modifiers (e.g., age, sex, disease severity).

### Reporting
- Generate Table 2: Primary and sensitivity analysis results.
- Draw forest plots to display subgroup effects.
- Assess evidence strength using GRADE or custom criteria.
- Discuss limitations (residual confounding, measurement error, generalizability).

## Common SQL Templates
- Retrieve basic patient demographics:
  ```sql
  SELECT p.subject_id, p.gender, a.admittime, a.dischtime, a.hospital_expire_flag
  FROM patients p
  JOIN admissions a ON p.subject_id = a.subject_id
  ```
- Extract vasopressor use during the first ICU stay:
  ```sql
  SELECT ie.stay_id, ie.intime, ie.outtime,
         ce.itemid, ce.charttime, ce.value, ce.valuenum
  FROM icustays ie
  JOIN chartevents ce ON ie.stay_id = ce.stay_id
  WHERE ce.itemid IN (221906, 221289, ...)
    AND ce.charttime BETWEEN ie.intime AND ie.intime + INTERVAL '24 hours'
  ```

## Collaboration with Existing Skills
- Use `cohort_validator` to validate cohort exports.
- Invoke `stats_analysis` for specific statistical computations.
- Finalize with `research_report_writer` to generate the complete evidence report.

## Important Notes
- All analyses are performed on de-identified data; do not attempt re-identification.
- Results are for research purposes only and should not inform direct clinical decisions.
- Code and results must be documented in a reproducible report.
- Do not construct additional skills during the process.
