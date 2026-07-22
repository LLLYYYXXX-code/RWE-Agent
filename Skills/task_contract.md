---
name: task_contract
description: Convert the user's research intent or the PICO corresponding to the protocol into a structured task_contract.json, locking in the PICOS, variables, and statistical methods to provide a single source of truth for subsequent cohort query and stats analysis. This is used during the research initiation phase.
version: 1.0.0
metadata: {"display_name":"task_contract"}
---

---
name: task_contract

description: Convert the user's research intent or the PICO corresponding to the protocol into a structured task_contract.json, locking in the PICOS, variables, and statistical methods to provide a single source of truth for subsequent cohort query and stats analysis. This is used during the research initiation phase.
---


# Task Contract Generation

## Purpose

Generate a standardized `task_contract.json` file from research proposals, paper reproduction requests, or question_analyzer session outputs, serving as the contract and input specification for the entire analysis workflow.

## When to Use

- After completing question_analyzer and receiving user confirmation
- Before starting any cohort query or data analysis
- When research details (PICOS, variables, methods, subgroups) need to be locked in to prevent scope creep

## Prerequisites

- question_analyzer has been completed or a clear research protocol is available
- Target population, exposure/intervention, comparator, outcomes, covariates, and statistical methods are known
- Familiarity with MIMIC-IV available table structures (can invoke `cohort_builder` for assistance)

## Workflow

### 1. Collect Research Elements

Extract from the user-confirmed protocol:
- **Population (P)**: Inclusion/exclusion criteria, time range, age, etc.
- **Intervention / Exposure (I)**: Primary exposure or treatment variable
- **Comparison (C)**: Control group definition
- **Outcomes (O)**: Primary and secondary outcome measures
- **Time frame**: Follow-up time window
- **Covariates**: List of confounding variables for adjustment
- **Methods**: Propensity score (PSM/IPTW), multivariable regression, Cox models, subgroup analyses, RCS, etc.
- **Sensitivity analyses**: Planned sensitivity tests

### 2. Build the Contract JSON

Write the following JSON structure to `/workspace/shared/task_contract.json` in English:

```json
{
  "study_id": "unique_short_snake_case_id",
  "title": "Human-readable study title",
  "population": {
    "description": "...",
    "inclusion_criteria": ["criterion1", "criterion2"],
    "exclusion_criteria": ["..."],
    "time_window": "e.g., first ICU stay between 2008-2019"
  },
  "exposure": {
    "variable": "...",
    "type": "binary/categorical/continuous",
    "definition": "..."
  },
  "comparator": {
    "variable": "...",
    "definition": "..."
  },
  "outcomes": {
    "primary": {
      "variable": "...",
      "type": "binary/time-to-event/continuous",
      "definition": "..."
    },
    "secondary": [
      {"variable": "...", "type": "...", "definition": "..."}
    ]
  },
  "covariates": [
    {"variable": "age", "type": "continuous", "source_table": "patients"},
    {"variable": "gender", "type": "binary", "source_table": "patients"}
  ],
  "methods": {
    "primary_analysis": "Cox proportional hazards / logistic regression / ...",
    "propensity_score": {
      "method": "PSM / IPTW / matching",
      "caliper": null,
      "matching_ratio": 1
    },
    "subgroup_analyses": ["by sex", "by age group"],
    "sensitivity_analyses": ["E-value", "additional adjustment"]
  },
  "outputs": {
    "tables": ["Table1 baseline", "Table2 primary results", "..."],
    "figures": ["Kaplan-Meier curve", "Forest plot", "RCS plot"]
  }
}
```

Adjust fields according to the specific research content, ensuring every variable can be found or derived in MIMIC-IV. If uncertain, mark as pending and confirm later with `cohort_builder`.

### 3. Validate the Contract

- Check that all variables are realizable in the database (pre‑query schemas such as `mimiciv_hosp`, `mimiciv_icu` as needed)
- Confirm there are no logical flaws in the study design
- Save the final contract as `/workspace/shared/task_contract.json`

### 4. Hand Off to Downstream

After saving, notify the user: "TaskContract is ready. It will be validated by `feasibility_check`, then `cohort_builder` will execute cohort extraction."

## Important Notes

- Once the contract file is created, subsequent stages will treat it as read‑only; if adjustments are needed, re-run this skill and update the version number.
- All variable definitions must use official MIMIC-IV table and column names (e.g., `patients.subject_id`, `admissions.hadm_id`) to avoid ambiguity.
- For complex study designs, multiple analysis plan objects may be included.
