---
name: cohort_builder
description: An end-to-end PICO-driven clinical data extraction and cleaning pipeline. It is triggered when users provide structured PICO elements (population/exposure/control/outcome) and need to generate an analysis-ready dataset. It covers PICO coding specifications, coding verification, cohort SQL generation, feature extraction, data cleaning, and quality reporting. It enhances diagnostic logs and is fully self-contained, without external module dependencies.
version: 1.0.0
metadata: {"display_name":"cohort_builder"}
---

---
name: cohort_builder 
description: An end-to-end PICO-driven clinical data extraction and cleaning pipeline. It is triggered when users provide structured PICO elements (population/exposure/control/outcome) and need to generate an analysis-ready dataset. It covers PICO coding specifications, coding verification, cohort SQL generation, feature extraction, data cleaning, and quality reporting. It enhances diagnostic logs and is fully self-contained, without external module dependencies.
---


# cohort_builder — End-to-End PICO-Driven Clinical Data Extraction and Cleaning

## Trigger Scenarios

Trigger when a user provides a study protocol JSON file containing structured PICO elements as the research plan, and requests extraction of an analysis-ready dataset from MIMIC-IV.

**Example trigger statements:**
- "Extract data according to the following PICO: P=adult sepsis patients, I=norepinephrine, C=dopamine, O=28-day mortality"
- "Convert PICO into an analyzable dataset"
- "Extract PICO cohort and clean the data"
- "Help me build a cohort comparing XXX vs YYY"

---

## Core Pipeline (5 Stages)

```
Stage 1: PICO Standardized Encoding + Code Validation
    ↓
Stage 2: Cohort Extraction SQL Generation and Execution
    ↓
Stage 3: Feature Extraction SQL Generation and Execution
    ↓
Stage 4: Data Cleaning and Quality Report
    ↓
Stage 5: Assemble Analysis-Ready Dataset
```

> **Self-Contained Principle**: All SQL/Python templates in this skill are inline code. Does not rely on external modules such as `db_connector` or `feature_extractor`.
> Use HOST, PORT, DB, USER, PASSWORD variables from Memory to connect to the internal MIMIC-IV database.

---

## Stage 1: PICO Standardized Encoding + Code Validation

### 1.1 Encoding Specification

Strictly map the user's natural language PICO elements into a structured definition. Each element must include:

| Field | Description | Example |
|-------|-------------|---------|
| `concept_name` | Standardized concept name | `sepsis` |
| `domain` | Data domain | `condition` / `drug` / `measurement` / `procedure` / `observation` |
| `vocabulary` | Terminology system | `ICD-10-CM` / `ICD-9-CM` / `LOINC` / `RxNorm` / `MIMIC-itemid` / `MIMIC-label` |
| `codes` | Specific code list | `['A41.9', 'R65.20']` |
| `time_window` | Time window constraint (relative to index_time) | `[-6h, +24h]` |
| `aggregation` | Aggregation method | `first` / `max` / `min` / `mean` / `any` / `count` |

### 1.2 MIMIC-IV Special Handling Guidelines

#### ICD Code Version Determination
MIMIC-IV contains both ICD-9-CM and ICD-10-CM codes. Operation steps:

```sql
-- First check version distribution in diagnoses_icd
SELECT icd_version, COUNT(*) AS n
FROM mimic_hosp.diagnoses_icd
GROUP BY icd_version;

-- Also check procedures_icd
SELECT icd_version, COUNT(*) AS n
FROM mimic_hosp.procedures_icd
GROUP BY icd_version;
```

**Rule**: If `icd_version=10` count far exceeds `icd_version=9`, prioritize ICD-10 codes; otherwise provide both code sets.

**Format**: In MIMIC, `icd_code` is stored as a string, typically without decimal points. ICD-10-CM e.g., `'A419'` (actually A41.9), ICD-9-CM e.g., `'99592'` (actually 995.92).

#### Drug Mapping Pathways
Three mutually backup pathways, in priority order:
1. **ICU Medications**: `mimic_icu.inputevents` → `itemid` (fastest, but limited to ICU medications)
2. **Inpatient Pharmacy**: `mimic_hosp.pharmacy` → `gsn` / `ndc` → needs mapping to drug names
3. **Prescription Records**: `mimic_hosp.prescriptions` → `drug` field (non-standardized)

```sql
-- Method to find drug itemid
SELECT DISTINCT itemid, label
FROM mimic_icu.d_items
WHERE label ILIKE '%norepinephrine%'
   OR label ILIKE '%levophed%';
```

#### Laboratory Value Lookup
```sql
-- Find lab itemid
SELECT itemid, label, fluid, category
FROM mimic_hosp.d_labitems
WHERE label ILIKE '%creatinine%'
  AND fluid = 'Blood';
```

#### Time Anchor Selection
| Scenario | Recommended Anchor | MIMIC Column |
|----------|--------------------|--------------|
| ICU intervention study | ICU admission time | `mimic_icu.icustays.intime` |
| Inpatient exposure study | Hospital admission time | `mimic_hosp.admissions.admittime` |
| Surgery study | Surgery start time | `mimic_hosp.poe.ordertime` or `procedures_icd` association |

### 1.3 Code Validation

**Must validate in Stage 1 that user-provided codes actually exist in the MIMIC database.** Use the following validation chain:

```sql
-- Validate diagnosis codes exist
SELECT icd_code, icd_version, COUNT(*) AS freq
FROM mimic_hosp.diagnoses_icd
WHERE icd_code IN ('A419', 'R6520', '99592')  -- replace with user-provided code list
GROUP BY icd_code, icd_version
ORDER BY freq DESC;

-- Validate procedure codes exist
SELECT icd_code, icd_version, COUNT(*) AS freq
FROM mimic_hosp.procedures_icd
WHERE icd_code IN ('3612', '02100Z3')  -- replace with user-provided code list
GROUP BY icd_code, icd_version
ORDER BY freq DESC;

-- Validate drug itemid exists
SELECT itemid, label, COUNT(*) AS freq
FROM mimic_icu.inputevents
WHERE itemid IN (221906, 221289)  -- replace with itemid list
GROUP BY itemid, label;
```

**Validation Failure Handling:**
- If code is completely non-existent → Use `LIKE 'prefix%'` fuzzy search to suggest alternative codes, present to user for confirmation
- If code partially exists → Remove invalid codes, log warnings
- If code frequency is 0 but exists in dictionary → Mark as low-priority warning (rare codes, possibly from different institutions)

**Hint**: If ICD code queries return empty results, invoke `mimic-icd-format-check` skill to troubleshoot format issues.

### 1.4 Output Artifact

```json
{
  "pico_id": "PICO-2025-001",
  "population": {
    "name": "adult_sepsis_patients",
    "criteria": {
      "age_min": 18,
      "conditions": [
        {"concept_name": "sepsis", "vocabulary": "ICD-10-CM", "codes": ["A41.9", "R65.20"], "verified": true, "freq_in_db": 12345}
      ]
    }
  },
  "intervention": {
    "name": "norepinephrine",
    "domain": "drug",
    "vocabulary": "MIMIC-itemid",
    "codes": [221906],
    "verified": true,
    "route": "intravenous"
  },
  "comparator": {
    "name": "dopamine",
    "domain": "drug",
    "vocabulary": "MIMIC-itemid",
    "codes": [221662],
    "verified": true,
    "route": "intravenous"
  },
  "outcome": {
    "primary": {"name": "28_day_mortality", "type": "binary", "time_horizon": "28d", "source": "mimic_hosp.admissions.deathtime + mimic_derived.dod"},
    "secondary": []
  },
  "index_time": "icu_intime",
  "observation_window": ["index - 6h", "index + 28d"],
  "validation_log": [
    {"code": "A41.9", "status": "verified", "freq": 12345},
    {"code": "R65.20", "status": "verified", "freq": 8765}
  ]
}
```

---

## Stage 2: Cohort Extraction (Inline SQL Generation)

### 2.1 SQL Generation Principles

No external modules. Generate self-contained SQL directly following these templates:

- **Build CTEs progressively**: `WITH pop_base AS (...), pop_filtered AS (...), exposed AS (...), control AS (...), cohort_final AS (...)`
- **All time filters use `INTERVAL`**: Explicitly specify direction, e.g., `index_time - INTERVAL '6 hours'`, `index_time + INTERVAL '28 days'`
- **Exclusion criteria use `NOT EXISTS`**: Maintain readability and determinism
- **Add diagnostic comments after each CTE**: `-- CTE: after_xxx_filter | expected N ≈ XXXX | actual: <to be filled>`

### 2.2 Standard Cohort Building Template

```sql
-- ============================================================
-- PICO Cohort Extraction: [pico_id]
-- Generated: [timestamp]
-- ============================================================

DROP TABLE IF EXISTS [cohort_table_name] CASCADE;

CREATE TEMP TABLE [cohort_table_name] AS
WITH 
-- Step 0: Anchor base population
pop_base AS (
    SELECT 
        p.subject_id,
        a.hadm_id,
        i.stay_id,
        i.intime AS index_time,
        p.anchor_age + (EXTRACT(YEAR FROM i.intime) - p.anchor_year) AS age_at_index,
        p.gender,
        a.admittime,
        a.dischtime,
        a.deathtime,
        a.race
    FROM mimic_hosp.patients p
    INNER JOIN mimic_hosp.admissions a 
        ON p.subject_id = a.subject_id
    INNER JOIN mimic_icu.icustays i 
        ON a.hadm_id = i.hadm_id
    WHERE p.anchor_age >= 18  -- age filter: use anchor_age for approximation
      AND i.intime IS NOT NULL
),
-- Step 1: Inclusion criteria
pop_included AS (
    SELECT DISTINCT pb.*
    FROM pop_base pb
    INNER JOIN mimic_hosp.diagnoses_icd di
        ON pb.hadm_id = di.hadm_id
    WHERE di.icd_code IN ('A419', 'R6520')  -- sepsis codes (verified in Stage 1)
      -- AND di.icd_version = 10  -- optionally restrict version
),
-- Step 2: Exclusion criteria
pop_filtered AS (
    SELECT pi.*
    FROM pop_included pi
    WHERE NOT EXISTS (
        SELECT 1 FROM mimic_hosp.diagnoses_icd di2
        WHERE pi.hadm_id = di2.hadm_id
          AND di2.icd_code IN ('XXX', 'YYY')  -- exclusion codes
    )
    -- AND age_at_index <= 89  -- optional extra filter
),
-- Step 3: Exposure grouping
exposed AS (
    SELECT DISTINCT pf.hadm_id, 1 AS exposure_group
    FROM pop_filtered pf
    INNER JOIN mimic_icu.inputevents ie
        ON pf.stay_id = ie.stay_id
    WHERE ie.itemid = 221906  -- norepinephrine (verified in Stage 1)
      AND ie.starttime BETWEEN pf.index_time - INTERVAL '6 hours' 
                           AND pf.index_time + INTERVAL '24 hours'
),
control AS (
    SELECT DISTINCT pf.hadm_id, 0 AS exposure_group
    FROM pop_filtered pf
    INNER JOIN mimic_icu.inputevents ie
        ON pf.stay_id = ie.stay_id
    WHERE ie.itemid = 221662  -- dopamine (verified in Stage 1)
      AND ie.starttime BETWEEN pf.index_time - INTERVAL '6 hours' 
                           AND pf.index_time + INTERVAL '24 hours'
      AND NOT EXISTS (SELECT 1 FROM exposed e WHERE e.hadm_id = pf.hadm_id)
),
-- Step 4: Assemble final cohort
cohort_final AS (
    SELECT 
        pf.*,
        COALESCE(exp.exposure_group, ctrl.exposure_group) AS exposure_group
    FROM pop_filtered pf
    LEFT JOIN exposed exp ON pf.hadm_id = exp.hadm_id
    LEFT JOIN control ctrl ON pf.hadm_id = ctrl.hadm_id
    WHERE exp.exposure_group IS NOT NULL OR ctrl.exposure_group IS NOT NULL
)
SELECT * FROM cohort_final;
```

### 2.3 Common Variant Templates

#### Variant A: Hospital tables only (no ICU)
```sql
pop_base AS (
    SELECT 
        p.subject_id, a.hadm_id,
        a.admittime AS index_time,
        ...
    FROM mimic_hosp.patients p
    INNER JOIN mimic_hosp.admissions a ON p.subject_id = a.subject_id
    WHERE p.anchor_age >= 18
)
```

#### Variant B: Pharmacy table for drug exposure
```sql
exposed AS (
    SELECT DISTINCT pf.hadm_id, 1 AS exposure_group
    FROM pop_filtered pf
    INNER JOIN mimic_hosp.prescriptions rx
        ON pf.hadm_id = rx.hadm_id
    WHERE LOWER(rx.drug) LIKE '%norepinephrine%'
      AND rx.starttime BETWEEN pf.index_time - INTERVAL '6 hours' 
                           AND pf.index_time + INTERVAL '24 hours'
)
```

#### Variant C: Exposure threshold (multiple administrations/dose)
```sql
exposed AS (
    SELECT pf.hadm_id, 1 AS exposure_group
    FROM pop_filtered pf
    INNER JOIN mimic_icu.inputevents ie
        ON pf.stay_id = ie.stay_id
    WHERE ie.itemid = 221906
      AND ie.starttime BETWEEN pf.index_time - INTERVAL '6 hours' 
                           AND pf.index_time + INTERVAL '24 hours'
    GROUP BY pf.hadm_id
    HAVING COUNT(*) >= 2  -- at least 2 administrations
)
```

### 2.4 Diagnostic Log

**Must output counts after each CTE. If any CTE is empty or significantly abnormal, ABORT and report:**

```
📊 Cohort Build Diagnostics:
   pop_base:               N = 53,210
   pop_included (after inclusion):  N = 12,450  (↓ 76.6%)
   pop_filtered (after exclusion):  N = 11,890  (↓ 4.5%)
   exposed (exposure group):        N = 4,230
   control (control group):         N = 3,810
   cohort_final (final):            N = 8,040
   ⚠️ Exposure/Control ratio = 1.11:1 (acceptable range 0.5~2.0)
```

**Anomaly Thresholds and Handling:**
| Signal | Threshold | Handling |
|--------|-----------|----------|
| Final N < 30 | N_final < 30 | Suggest relaxing inclusion criteria, print stepwise counts |
| Step filters >90% | N_after / N_before < 0.1 | Check if this step's criteria are too strict |
| Extreme exposure/control ratio | ratio < 0.1 or ratio > 10 | Alert group imbalance, consider IPTW |
| Exposed or control group = 0 | N_exposed=0 or N_control=0 | Check if itemid/code is correct, use `mimic-icd-format-check` to investigate |

### 2.5 SQL Execution Error Handling

**When SQL execution fails, automatically follow this investigation flow:**

1. **Syntax error**: Print error location → check bracket matching, quotes, commas
2. **Column does not exist**: Invoke `mimic-schema-fix` skill to query actual table structure and fix
3. **Type mismatch**: Check if DATE/TIMESTAMP operations need explicit conversion `::date` / `::timestamp`
4. **Zero rows returned**: Check JOIN keys (stay_id ↔ hadm_id ↔ subject_id), check if time windows are reasonable

```
>>> ERROR in Stage 2 | SQL: INSERT INTO cohort_final
    PostgreSQL Error: column "dob" does not exist
    🔧 Auto-fix: patients table has no dob column, use anchor_age + anchor_year instead
    📝 Correction: p.anchor_age + (EXTRACT(YEAR FROM a.admittime) - p.anchor_year) AS age
```

---

## Stage 3: Feature Extraction (Inline SQL/Python)

### 3.1 Feature Classification and Extraction Templates

No external `feature_extractor` module. Extract by category:

| Feature Type | MIMIC Source Table | Extraction Strategy | Time Window |
|-------------|-------------------|---------------------|-------------|
| Demographics | `patients` | Direct extraction | None |
| Admission info | `admissions` | Direct extraction | None |
| Vital signs | `chartevents` | Aggregate by itemid, flag outliers | ±24h around index |
| Laboratory | `labevents` | Aggregate by itemid, flag abnormal values | ±24h around index |
| Comorbidities | `diagnoses_icd` | Charlson / Elixhauser calculation | All records before index |
| Severity scores | Derived from `chartevents` | SOFA / APS III / GCS | Within 24h before index |
| Drug exposure details | `inputevents` / `pharmacy` | Dose, frequency, duration | Around index |
| Outcomes | `admissions` / `patients` | Death time derivation | Various windows after index |

### 3.2 Key Feature Extraction SQL Templates

#### Vital Signs
```sql
-- Extract min/max/mean of vital signs within 24h before index
DROP TABLE IF EXISTS vitals_features;
CREATE TEMP TABLE vitals_features AS
SELECT 
    c.stay_id,
    -- Heart rate
    MIN(CASE WHEN c.itemid IN (220045, 211) THEN c.valuenum END) AS hr_min,
    MAX(CASE WHEN c.itemid IN (220045, 211) THEN c.valuenum END) AS hr_max,
    AVG(CASE WHEN c.itemid IN (220045, 211) THEN c.valuenum END) AS hr_mean,
    -- Mean arterial pressure (MAP)
    MIN(CASE WHEN c.itemid IN (220052, 456) THEN c.valuenum END) AS map_min,
    AVG(CASE WHEN c.itemid IN (220052, 456) THEN c.valuenum END) AS map_mean,
    -- Respiratory rate
    AVG(CASE WHEN c.itemid IN (220210, 618) THEN c.valuenum END) AS rr_mean,
    -- Temperature
    AVG(CASE WHEN c.itemid IN (223762, 676) THEN c.valuenum END) AS temp_mean,
    -- SpO2
    AVG(CASE WHEN c.itemid IN (220277, 646) THEN c.valuenum END) AS spo2_mean
FROM mimic_icu.chartevents c
INNER JOIN [cohort_table_name] co ON c.stay_id = co.stay_id
WHERE c.itemid IN (220045, 211, 220052, 456, 220210, 618, 223762, 676, 220277, 646)
  AND c.charttime BETWEEN co.index_time - INTERVAL '24 hours' AND co.index_time
  AND c.valuenum IS NOT NULL
  AND c.valuenum > 0  -- filter implausible values
GROUP BY c.stay_id;
```

#### Laboratory Values
```sql
-- Extract lab values within ±24h of index
DROP TABLE IF EXISTS lab_features;
CREATE TEMP TABLE lab_features AS
SELECT 
    co.hadm_id,
    co.stay_id,
    -- Creatinine
    MAX(CASE WHEN le.itemid = 50912 AND le.valuenum IS NOT NULL THEN le.valuenum END) AS creatinine_max,
    MIN(CASE WHEN le.itemid = 50912 AND le.valuenum IS NOT NULL THEN le.valuenum END) AS creatinine_min,
    -- Lactate
    MAX(CASE WHEN le.itemid = 50813 AND le.valuenum IS NOT NULL THEN le.valuenum END) AS lactate_max,
    -- WBC
    MAX(CASE WHEN le.itemid IN (51301, 51300) AND le.valuenum IS NOT NULL THEN le.valuenum END) AS wbc_max,
    -- Platelets
    MIN(CASE WHEN le.itemid = 51265 AND le.valuenum IS NOT NULL THEN le.valuenum END) AS platelet_min,
    -- BUN
    MAX(CASE WHEN le.itemid IN (51006, 52647) AND le.valuenum IS NOT NULL THEN le.valuenum END) AS bun_max
FROM [cohort_table_name] co
LEFT JOIN mimic_hosp.labevents le 
    ON co.hadm_id = le.hadm_id
    AND le.charttime BETWEEN co.index_time - INTERVAL '24 hours' 
                         AND co.index_time + INTERVAL '24 hours'
GROUP BY co.hadm_id, co.stay_id;
```

#### Comorbidities (Charlson example)
```sql
-- Use mimiciv_derived.charlson (if available)
DROP TABLE IF EXISTS comorbidity_features;
CREATE TEMP TABLE comorbidity_features AS
SELECT 
    co.hadm_id,
    COALESCE(ch.myocardial_infarct, 0) AS cm_mi,
    COALESCE(ch.congestive_heart_failure, 0) AS cm_chf,
    COALESCE(ch.peripheral_vascular_disease, 0) AS cm_pvd,
    COALESCE(ch.cerebrovascular_disease, 0) AS cm_cvd,
    COALESCE(ch.dementia, 0) AS cm_dementia,
    COALESCE(ch.chronic_pulmonary_disease, 0) AS cm_copd,
    COALESCE(ch.rheumatic_disease, 0) AS cm_rheumatic,
    COALESCE(ch.peptic_ulcer_disease, 0) AS cm_pud,
    COALESCE(ch.mild_liver_disease, 0) AS cm_liver_mild,
    COALESCE(ch.diabetes_without_cc, 0) AS cm_dm,
    COALESCE(ch.diabetes_with_cc, 0) AS cm_dm_comp,
    COALESCE(ch.hemiplegia_or_paraplegia, 0) AS cm_hemiplegia,
    COALESCE(ch.renal_disease, 0) AS cm_renal,
    COALESCE(ch.malignancy, 0) AS cm_cancer,
    COALESCE(ch.severe_liver_disease, 0) AS cm_liver_severe,
    COALESCE(ch.metastatic_solid_tumor, 0) AS cm_mets,
    COALESCE(ch.aids, 0) AS cm_aids
FROM [cohort_table_name] co
LEFT JOIN mimic_derived.charlson ch ON co.hadm_id = ch.hadm_id;
```

#### Outcomes (28-day mortality example)
```sql
-- Outcome derivation: 28-day mortality
DROP TABLE IF EXISTS outcome_primary;
CREATE TEMP TABLE outcome_primary AS
SELECT 
    co.hadm_id,
    co.stay_id,
    CASE 
        WHEN co.deathtime IS NOT NULL 
         AND co.deathtime <= co.index_time + INTERVAL '28 days' 
        THEN 1 ELSE 0 
    END AS death_28d,
    CASE 
        WHEN co.deathtime IS NOT NULL 
         AND co.deathtime <= co.index_time + INTERVAL '90 days' 
        THEN 1 ELSE 0 
    END AS death_90d,
    -- In-hospital mortality
    CASE WHEN co.deathtime IS NOT NULL 
         AND co.deathtime <= co.dischtime 
        THEN 1 ELSE 0 
    END AS hospital_mortality,
    -- ICU mortality
    CASE WHEN co.deathtime IS NOT NULL 
         AND co.deathtime <= (SELECT outtime FROM mimic_icu.icustays icu WHERE icu.stay_id = co.stay_id)
        THEN 1 ELSE 0
    END AS icu_mortality
FROM [cohort_table_name] co;
```

### 3.3 Missing Value Marking Specification

- **Explicit missing**: Patient should have this data but not recorded → `NULL`
- **Implicit missing**: Logically impossible → special marker `-999` with explanation in quality report
- **Time window missing**: No record within window → `NULL` + log note

### 3.4 Feature Extraction Diagnostics

```
📊 Feature Extraction Diagnostics:
   vitals_features:  7,890 / 8,040 rows (missing rate 1.9%)
   lab_features:     7,560 / 8,040 rows (missing rate 6.0%)
   comorbidity_features: 8,040 / 8,040 rows ✅
   outcome_primary:  8,040 / 8,040 rows ✅
   ⚠️ lab_troponin missing rate 67.3% (>50%), recommend excluding or imputing in subsequent analysis
```

---

## Stage 4: Data Cleaning and Quality Report

### 4.1 Automated Cleaning Pipeline (Strictly Sequential)

#### Step 1: Type Coercion
```python
# Coerce all columns to correct types
df['age_at_index'] = pd.to_numeric(df['age_at_index'], errors='coerce')
df['gender'] = df['gender'].astype('category')
for col in df.filter(like='lab_').columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
for col in df.filter(like='cm_').columns:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
```

#### Step 2: Range Validation
Define `valid_range` for each continuous variable; values outside → `NaN`. Record affected row counts:

| Variable | Valid Range | Rationale |
|----------|-------------|-----------|
| hr_min, hr_max | 10–350 bpm | Physiological limits |
| map_min, map_mean | 10–250 mmHg | Physiological limits |
| temp_mean | 25–45 °C | Thermometer range + extreme hypothermia |
| spo2_mean | 30–100 % | Sensor range |
| creatinine_max | 0.1–50 mg/dL | Clinical extremes |
| wbc_max | 0.1–500 K/μL | Clinical extremes |
| platelet_min | 1–5000 K/μL | Clinical extremes |
| age_at_index | 18–120 years | Adult ICU reasonable range |

```python
RANGE_CHECKS = {
    'hr_min': (10, 350), 'hr_max': (10, 350),
    'map_min': (10, 250), 'map_mean': (10, 250),
    'temp_mean': (25, 45), 'spo2_mean': (30, 100),
    'creatinine_max': (0.1, 50), 'wbc_max': (0.1, 500),
    'platelet_min': (1, 5000), 'age_at_index': (18, 120),
}
for col, (lo, hi) in RANGE_CHECKS.items():
    if col in df.columns:
        mask = (df[col] < lo) | (df[col] > hi)
        if mask.sum() > 0:
            print(f"  [RANGE] {col}: {mask.sum()} values outside [{lo}, {hi}] → NaN")
            df.loc[mask, col] = np.nan
```

#### Step 3: Logical Consistency Checks
```python
# Discharge time >= admission time
invalid = df[df['dischtime'] < df['admittime']]
if len(invalid) > 0:
    print(f"  [LOGIC] {len(invalid)} rows with dischtime < admittime → flagged")
    df['logic_flag_discharge'] = (df['dischtime'] < df['admittime']).astype(int)
```

#### Step 4: Zero/Near-Zero Variance Filtering
```python
# Columns with single value >99% flagged and removed
constant_cols = []
for col in df.columns:
    if df[col].nunique() <= 1 or df[col].value_counts(normalize=True).iloc[0] > 0.99:
        constant_cols.append(col)
        print(f"  [CONSTANT] {col}: >99% single value → removed")
df.drop(columns=constant_cols, errors='ignore', inplace=True)
```

#### Step 5: Outlier Winsorization
```python
# Default 1st & 99th percentile
WINSORIZE_COLS = [c for c in df.columns if c.startswith(('hr_','map_','creatinine_','wbc_','bun_','lactate_'))]
for col in WINSORIZE_COLS:
    if col in df.columns and df[col].notna().sum() > 10:
        lo, hi = df[col].quantile(0.01), df[col].quantile(0.99)
        n_lo = (df[col] < lo).sum()
        n_hi = (df[col] > hi).sum()
        df[col] = df[col].clip(lo, hi)
        if n_lo + n_hi > 0:
            print(f"  [WINSORIZE] {col}: {n_lo} low + {n_hi} high → clipped to [{lo:.2f}, {hi:.2f}]")
```

#### Step 6: High Missing Rate Row Filtering
```python
# Default threshold: rows with >50% missing flagged but NOT removed by default (requires user confirmation)
row_missing_pct = df.isnull().mean(axis=1)
hi_miss_rows = row_missing_pct > 0.5
if hi_miss_rows.sum() > 0:
    print(f"  [HIGH_MISS] {hi_miss_rows.sum()} rows with >50% missing values → flagged (not removed)")
    df['flag_high_missing'] = hi_miss_rows.astype(int)
```

#### Step 7: Missing Value Encoding Standardization
```python
# All NaN / None / '' → np.nan (unified representation)
df = df.replace(['', 'NA', 'N/A', 'null', 'NULL', 'None', 'NaN'], np.nan)
```

### 4.2 Quality Report

**Must generate a structured cleaning summary containing:**

```
╔══════════════════════════════════════════════╗
║         DATA QUALITY REPORT                  ║
╠══════════════════════════════════════════════╣
║ Row count:    Initial 8,040 → Cleaned 7,980  ║
║               (removed 60, 0.75%)             ║
║ Column count: Initial 86 → Cleaned 83        ║
║               (removed constant columns: 3)   ║
╠══════════════════════════════════════════════╣
║ Overall missing rate: 3.8%                   ║
║ TOP 5 missing columns:                       ║
║   lab_troponin   67.3% ⚠️                    ║
║   lab_bnp        52.1% ⚠️                    ║
║   lab_lactate    18.4%                       ║
║   vitals_rr      12.1%                       ║
║   vitals_temp    8.9%                        ║
╠══════════════════════════════════════════════╣
║ Cleaning operation statistics:                ║
║   [RANGE] creatinine_max: 12 vals → NaN      ║
║   [RANGE] hr_max: 8 vals → NaN               ║
║   [WINSORIZE] wbc_max: 23 + 45 clipped       ║
║   [CONSTANT] cm_aids, cm_liver_severe, ...   ║
╠══════════════════════════════════════════════╣
║ ⚠️ Warnings:                                 ║
║   1. lab_troponin missing >50%, recommend imputation or exclusion
║   2. Exposure/control ratio 1.11, balance acceptable
║   3. cm_aids constant (99.8% 0), removed
╚══════════════════════════════════════════════╝
```

### 4.3 Cleaning Failure Handling

| Signal | Handling |
|--------|----------|
| Row reduction >20% | ⚠️ Cleaning rules may be too strict, show per-rule impact, ask user if relaxation is acceptable |
| All rows removed | 🛑 ABORT, print affected rows per cleaning rule, suggest turning off rules one by one |
| Exposure group labels lost | 🛑 Check merge/join logic, ensure `exposure_group` column was not accidentally dropped |

---

## Stage 5: Assemble Analysis-Ready Dataset

### 5.1 Final Merge

```python
# Merge all feature tables
import pandas as pd

# Load each feature table and merge into main cohort
cohort = pd.read_sql("SELECT * FROM [cohort_table_name]", con=engine)
vitals = pd.read_sql("SELECT * FROM vitals_features", con=engine)
lab = pd.read_sql("SELECT * FROM lab_features", con=engine)
comorb = pd.read_sql("SELECT * FROM comorbidity_features", con=engine)
outcome = pd.read_sql("SELECT * FROM outcome_primary", con=engine)

# Merge by stay_id
df_final = (cohort
    .merge(vitals, on='stay_id', how='left')
    .merge(lab, on=['hadm_id', 'stay_id'], how='left')
    .merge(comorb, on='hadm_id', how='left')
    .merge(outcome, on=['hadm_id', 'stay_id'], how='left')
)
```

### 5.2 Output Format

Must provide all of the following:

1. **Analysis File**: `[pico_id]_dataset.parquet`
   - Contains identifier columns (`subject_id`, `hadm_id`, `stay_id`)
   - Exposure flag `exposure_group` (1=Intervention, 0=Control)
   - Outcome `outcome_primary`
   - All cleaned feature columns

2. **Data Dictionary**: `[pico_id]_data_dictionary.csv`
   ```csv
   column_name,source_table,domain,type,unit,missingness_pct,distribution_summary
   age_at_index,patients,demographics,numeric,years,0.0,mean=65.2 sd=14.3 median=67 IQR=56-76
   hr_mean,chartevents,vitals,numeric,bpm,1.9,mean=88.5 sd=18.2
   exposure_group,derived,exposure,binary,,0.0,0=3810 1=4230
   death_28d,admissions,outcome,binary,,0.0,0=6320 1=1720
   ...
   ```

3. **Metadata File**: `[pico_id]_metadata.json`
   ```json
   {
     "dataset_version": "v1.0",
     "pico_id": "PICO-2025-001",
     "mimic_version": "v2.2",
     "generated_at": "2025-01-01T00:00:00Z",
     "n_rows": 7980,
     "n_cols": 83,
     "exposure_distribution": {"control": 3810, "intervention": 4230},
     "cleaning_log": "see quality report",
     "pipeline_script": "pipeline_pico_001.sql"
   }
   ```

### 5.3 Final Confirmation

**Print output manifest after Stage 5 completes:**
```
✅ PICO Extraction Complete
📁 Output files:
   /data/PICO-2025-001_dataset.parquet (7,980 rows × 83 cols)
   /data/PICO-2025-001_data_dictionary.csv
   /data/PICO-2025-001_metadata.json
   /sql/cohort_extraction_PICO-2025-001.sql
   /sql/feature_extraction_PICO-2025-001.sql
📊 Dataset ready for statistical analysis (mimic_stats_analysis / mimic-statistical-analysis-pipeline)
```

---

## Integration with Existing Skills

| Skill | Integration Point | Trigger Timing |
|-------|-------------------|----------------|
| `mimic-icd-format-check` | Stage 1 code validation | Auto-invoked when ICD code queries return empty |
| `mimic-schema-fix` | Stage 2 SQL error | Auto-invoked on column does not exist / type mismatch |
| `mimic-cohort-iteration` | Stage 2 modification iteration | Invoked when user requests grouping adjustments |
| `mimic-statistical-analysis-pipeline` | After Stage 5 | Links to statistical analysis once dataset is ready |
| `mimic-connection-check` | Before pipeline starts | Confirms environment availability on first run |

---

## Comprehensive Diagnostics and Error Handling

### Core Principles

**No stage failure may silently pass.** Must:
1. Print stage name and step number
2. Describe error context (table name, row count, operation)
3. Provide 2–3 possible root causes and inspection suggestions
4. Write error to `pipeline_errors.log`

### Stage-Specific Checkpoints

| Stage | Checkpoint | Error Type | Auto-Fix Strategy |
|-------|------------|------------|-------------------|
| Stage 1 | PICO missing key fields | Incomplete input | List missing fields, wait for user to supplement |
| Stage 1 | ICD codes not found in DB | Invalid codes | Auto `LIKE` fuzzy search for alternative codes, present to user |
| Stage 2 | SQL syntax error | PostgreSQL Error | Print error location, check quotes/commas |
| Stage 2 | SQL column does not exist | Schema Error | Invoke `mimic-schema-fix` to query actual column names |
| Stage 2 | Cohort empty (N < 10) | Criteria too strict | Print each CTE count, suggest which step to relax |
| Stage 3 | Feature table empty | Itemid error | Self-check with `SELECT DISTINCT itemid, label FROM d_items WHERE label ILIKE '%keyword%'` |
| Stage 3 | Row count explodes after merge | JOIN key error | Check 1:1 / 1:N relationship, consider `DISTINCT` |
| Stage 4 | Row reduction >20% | Cleaning too strict | Show per-rule impact, ask user |
| Stage 4 | All rows dropped | Rule conflict | ABORT, print each rule's impact |
| Stage 5 | Parquet write failed | IO Error | Check disk space, path permissions |

### Error Format Template

```
╔══════════════════════════════════════════════╗
║  ERROR in Stage [X] | Step: [step_name]      ║
╠══════════════════════════════════════════════╣
║  Table: [table_name]                         ║
║  Rows: [before] → [after]                    ║
║  Error: [PostgreSQL message or Python trace] ║
╠══════════════════════════════════════════════╣
║  🔍 Possible causes:                         ║
║    1. [hypothesis 1]                         ║
║    2. [hypothesis 2]                         ║
║  🔧 Suggested fix: [action]                  ║
╚══════════════════════════════════════════════╝
```

---

## User Interaction Protocol

- **After Stage 2**: Print waterfall diagram showing N decrement at each step / text-based Sankey
- **After Stage 4**: Print cleaning summary: dropped rows/columns, TOP 5 missing columns, Warnings
- **After completion**: Output final paths and file list

## Anti-Patterns (Strictly Prohibited)

<NEVER>
- Never skip Stage 1 code validation before executing SQL, because ICD code formats in MIMIC vary widely (with/without decimals, version differences); unvalidated codes may result in empty cohorts or incorrect inclusion
- Never enter Stage 2 without user confirmation of PICO codes, as code selection directly affects research reproducibility
- Never silently drop data rows without logging cleaning operations, as data loss cannot be traced
- Never use `SELECT *` as final output — always explicitly list column names to ensure reproducibility
- Never assume `patients.dob` exists — MIMIC-IV uses `anchor_age` + `anchor_year` instead of date of birth
- Never use ICD-9 and ICD-10 codes together without checking `icd_version`, as they represent different patient eras and coding systems are incompatible
- Never directly JOIN `icustays` and `diagnoses_icd` using `stay_id` — `diagnoses_icd` uses `hadm_id` as key, must bridge through `icustays.hadm_id`
</NEVER>
