---
name: feasibility_check
description: Quickly assess the existence and scale of specific concepts, variables, or patient populations in the database to confirm data feasibility before formulating research questions. Applicable scenarios: After researchers raise clinical questions, they need to understand the number of target populations and whether key variables have been collected.
version: 1.0.0
---

---
name: feasibility_check 
description: Quickly assess the existence and scale of specific concepts, variables, or patient populations in the database to confirm data feasibility before formulating research questions. Applicable scenarios: After researchers raise clinical questions, they need to understand the number of target populations and whether key variables have been collected.
---



# Feasibility Check

A skill dedicated to conducting data feasibility exploration. Before generating a formal research plan or writing complex extraction logic, you will write and execute lightweight exploratory SQL queries based on the researcher's proposed concept to verify the existence of required data, approximate sample size, and potential limitations.

## Trigger Conditions
- The researcher proposes a new clinical question and needs to assess whether MIMIC-IV can effectively support the study.
- The researcher asks questions such as: "Does the database contain data on X?", "How many patients meet criteria Y?", "What is the coverage of a certain variable in the ICU?", etc.

## Execution Workflow

### Part One:

## Steps (executed synchronously, no sub‑agents)

1. **Retrieve credentials from Memory**  
   Call `search_memory` with query:  
   `"MIMIC database connection parameters PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD"`  
   Also fetch `"research context mimics version schema"` if relevant.

2. **Fallback if Memory is empty**  
   If no credentials found, ask the user once for HOST, PORT, DATABASE, USER, PASSWORD.  
   Save into Memory immediately via `save_memory` to prevent repeat requests.

3. **Generate env.sh**  
   Write a script at `scripts/env.sh` that exports `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`.  
   Make it executable (`chmod +x`).

4. **Load environment**  
   Source the script: `source scripts/env.sh`

5. **Verify connectivity**  
   Run a lightweight query (e.g., `SELECT COUNT(*) FROM patients;`) using `tmux_execute` or direct command.  
   If it fails, report error and re‑check credentials.

6. **Confirm research context**  
   Print database name and patient count, then load the necessary research skill.

7. **Proceed with study**  
   Only after successful verification, start cohort extraction or analysis.

---

### Part Two:

1. **Clarify query objectives**: Confirm key concepts (e.g., exposure, outcome, population characteristics) with the researcher, and translate them into one or more specific SQL checkpoints.
2. **Connect to database**: Load host, port, database, user, and password variables from Memory to ensure executable queries.
3. **Write exploratory SQL**:
   - Use `COUNT(DISTINCT subject_id/hadm_id/icustay_id)` to estimate target population size.
   - Check variable existence using tables such as `d_items`, `labevents`, `chartevents`, `diagnoses_icd`, `prescriptions`, e.g., `WHERE LOWER(label) LIKE '%keyword%'`.
   - Avoid full table scans or long-running queries; only retrieve summary metrics.
4. **Interpret results**: Summarize query results in concise language, including:
   - Approximate magnitude of the target population.
   - Whether key variables have sufficient records, and which tables and modules they reside in.
   - Obvious limitations (e.g., only available in ICU, high missing rates, complex coding schemes, etc.).
5. **Provide recommendations**: Based on feasibility results, advise whether the research question is suitable for pursuit in MIMIC-IV, or whether inclusion criteria, alternative variables, etc., need adjustment.

## Important Notes
- All queries are read‑only; data is never modified.
- Returned results are for data feasibility assessment only and do not replace formal cohort construction or fine‑grained statistical analysis.
- Strictly protect patient privacy: do not output any personal identifiers or specific values for very small groups (n < 10).
- The current database is MIMIC.

```sql
-- Verify SOFA table
SELECT column_name FROM information_schema.columns 
WHERE table_schema='mimiciv_derived' AND table_name='sofa';

-- Verify derived vitals table (note: it is 'vitalsign', not 'first_day_vitals')
SELECT column_name FROM information_schema.columns 
WHERE table_schema='mimiciv_derived' AND table_name='vitalsign';

-- Verify laboratory value sources: lactate in first_day_bg, routine labs in first_day_lab
SELECT table_name FROM information_schema.tables 
WHERE table_schema='mimiciv_derived' AND table_name LIKE '%bg%';
```

## Example Interaction
Researcher: "Compare outcomes between ARNI and ACEi in heart failure patients. First, let's see how many heart failure patients are in the database and whether ARNI prescription records exist."
Agent: Connect to database, execute queries to count heart failure hospitalizations, search for drug names containing "sacubitril" or "valsartan", then return patient counts and a brief report on drug availability.
