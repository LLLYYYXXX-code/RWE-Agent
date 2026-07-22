---
name: question_analyzer
description: Transforming users' vague research ideas into clearly structured and executable research task definitions. It is suitable for preliminary structuring of clinical comparative studies (TTE protocol identification) and general research problems, and serves as the starting point of the research process.
version: 1.2.0
---

---
name: question_analyzer
description: Transforming users' vague research ideas into clearly structured and executable research task definitions. It is suitable for preliminary structuring of clinical comparative studies (TTE protocol identification) and general research problems, and serves as the starting point of the research process.
---


# Question Analyzer

Transform a user's vague research question into a well-defined, actionable research task. This skill serves as the starting point of the research workflow, responsible for understanding context, refining the question, and generating a preliminary research plan.

This skill supports two working modes, automatically switching based on user input:

- **Clinical Comparative Research Mode**: When the user poses a clinical comparative research question involving interventions such as drugs or procedures, execute a rigorous TTE (Target Trial Emulation) protocol identification, extract PICO elements, and output a structured protocol in JSON format.
- **General Research Analysis Mode**: When the user poses other types of research ideas (e.g., materials, proteins, biology, plasma, patents, etc.), execute a general question refinement and research plan generation process.

## Trigger Conditions

This skill should be activated when the user expresses any of the following intents:
- Proposes a research topic or idea
- Is triggered as the first step after `rwd_to_rwe_statistical_workflow` is activated
- Poses a clinical comparative research question requiring TTE protocol structuring

## Input Specification

| Input Item | Type | Required | Description |
|------------|------|----------|-------------|
| `research_idea` | string | Yes | The user's initial research idea, can be described in natural language |
| `uploaded_files` | string[] | No | List of file paths uploaded or referenced by the user |
| `domain_hint` | string | No | Research domain mentioned by the user (e.g., materials, proteins, biology, plasma, patents, clinical medicine, etc.) |

## Output Specification

### Clinical Comparative Research Mode (TTE Protocol Identification)

When identified as a clinical comparative study, output in strict JSON format:

```json
{
  "study_type": "comparative_effectiveness",
  "population": {
    "description": "Target population description",
    "inclusion_criteria": ["Inclusion criterion 1", "Inclusion criterion 2"],
    "age_range": "Age range",
    "disease": "Disease name",
    "setting": "ICU/inpatient/outpatient",
    "time_window": "Enrollment time window"
  },
  "intervention": {
    "description": "Intervention description",
    "drug_or_procedure": "Specific drug/procedure",
    "route": "Route of administration",
    "timing": "Timing of administration"
  },
  "comparator": {
    "description": "Comparator description",
    "drug_or_procedure": "Specific drug/procedure",
    "route": "Route of administration",
    "timing": "Timing of administration"
  },
  "outcome": {
    "description": "Outcome description",
    "type": "Outcome type (e.g., all-cause mortality, adverse event rate)",
    "time_window": "Outcome assessment time window (e.g., 28 days, 90 days)"
  },
  "time_zero": {
    "description": "Time zero description",
    "event": "Starting event (e.g., first dose, admission date)"
  },
  "missing_elements": ["List of missing elements, empty if complete"]
}
```

### General Research Analysis Mode

When identified as a non-clinical comparative study, output a structured text plan:

| Output Item | Type | Description |
|-------------|------|-------------|
| `refined_question` | string | Refined core research question, summarized in one sentence |
| `research_plan` | object[] | Step-by-step execution plan, each step containing: step number, description, tools/actions, whether user input is required |
| `expected_outputs` | string[] | List of expected output files |
| `suggested_agent` | string | Recommended specialized agent name |

## Workflow

### Step 1: Mode Identification and Context Collection

1. **Determine research type**: Analyze user input to determine whether it is a clinical interventional comparative study.
   - If clinical comparative study, proceed to TTE protocol identification workflow (Step 2A).
   - If other types of research, proceed to general research analysis workflow (Step 2B).
2. **Read reference files**: If the user has uploaded files or referenced files in the conversation, use file reading tools to retrieve content.
3. **Identify domain**: If the user mentions a specific domain (materials, proteins, biology, plasma, patents, etc.), record the best-matching specialized agent.
4. **Check workspace**: Examine the `/workspace` directory for leftover files from previous runs to avoid redundant work.
5. **Basic search (on demand)**: Use `web_search` only when the user's topic is completely unfamiliar and basic orientation is needed; do not explore deeply at this stage.

### Step 2A: TTE Protocol Identification (Clinical Comparative Research Mode)

Extract PICO-T elements from the user's question to construct a structured protocol:

1. **Extract target population (Population)**: Include inclusion criteria (age, disease, ICU/inpatient, time window).
2. **Extract intervention (Intervention)**: Specific drug/procedure, route/timing of administration.
3. **Extract comparator (Comparator)**: Must be explicit; vague comparators such as "no treatment" or "standard of care" are not accepted.
4. **Extract outcome (Outcome)**: Must explicitly specify "outcome type + time window" (e.g., "28-day all-cause mortality").
5. **Extract time zero (Time Zero)**: Clearly identify the starting event from which timing begins.

**Critical Rules**:
- If any of the above elements are missing from the user's question, they must be listed in `missing_elements` with proactive follow-up questions until complete.
- If the user's question is not an interventional comparative study, clearly inform the user that the current system only supports TTE protocol identification for clinical comparative studies, and suggest using the general research analysis mode.

### Step 2B: General Research Question Refinement (General Research Analysis Mode)

Based on collected context, engage in interactive clarification with the user:

1. Summarize the user's vague idea into 2-3 possible research directions.
2. For each direction, explain its strengths, limitations, and required resources.
3. Ask the user to select or merge directions to form the final core research question.
4. Refine the final question into one sentence, ensuring it is actionable.

### Step 3: Generate Research Plan (General Research Analysis Mode)

After the user confirms the research direction, generate a step-by-step execution plan:

1. Number each step.
2. Specify the tools or actions to be used at each step.
3. Anticipate which steps will require user input during execution.
4. List expected output files.

**Plan Example:**

> **Core Research Question:** [Refined question]
>
> **Research Plan:**
> 1. Search web and academic databases for recent papers on [topic] (web_search)
> 2. Download and extract key sections from the top 20 results (sandbox shell + files)
> 3. Synthesize findings into a structured report (file creation)
> 4. Generate comparison tables and charts (Python in sandbox)
> 5. Save all outputs to `/workspace/output/`
>
> **Expected Outputs:** `report.md`, `references.bib`, `figures/comparison.png`
> **Steps Requiring User Input:** Step 2 (confirm paper selection)
> **Recommended Agent:** `literature_reviewer`

## Error Handling

| Scenario | Handling Approach |
|----------|-------------------|
| User input too vague to extract directions | Respond with guiding questions, request more details (e.g., domain, objective, scope) |
| Uploaded files cannot be read or format is unsupported | Prompt user to check file path and format, list supported formats |
| Web search returns no results | Suggest adjusting search keywords or providing more background information |
| User rejects all research directions | Re-initiate requirements discovery, propose new directions from different angles |
| `/workspace` directory does not exist or is inaccessible | Prompt user to check environment configuration, attempt to create directory |
| TTE protocol missing required elements | List missing items in `missing_elements` in JSON, generate follow-up questions |
| User question is not a clinical comparative study but expects TTE output | Clearly inform that current TTE mode only supports interventional comparative studies; suggest switching to general mode or supplementing information |

## Usage Examples

**Example 1: Clinical Comparative Research Mode**
```
User: I want to study the effects of SGLT2 inhibitors on cardiovascular outcomes in diabetic patients
Agent: [Activate question_analyzer, identified as clinical comparative study]
Agent: Identified as a clinical comparative study, extracting TTE protocol elements...
Output JSON:
{
  "study_type": "comparative_effectiveness",
  "population": {
    "description": "Patients with type 2 diabetes",
    "inclusion_criteria": ["Confirmed diagnosis of type 2 diabetes", "Age ≥18 years"],
    "age_range": "≥18 years",
    "disease": "Type 2 diabetes",
    "setting": "Outpatient/inpatient",
    "time_window": "To be confirmed"
  },
  "intervention": {
    "description": "SGLT2 inhibitors",
    "drug_or_procedure": "SGLT2 inhibitors (e.g., dapagliflozin, empagliflozin)",
    "route": "Oral",
    "timing": "To be confirmed"
  },
  "comparator": {
    "description": "To be confirmed",
    "drug_or_procedure": "",
    "route": "",
    "timing": ""
  },
  "outcome": {
    "description": "Cardiovascular outcomes",
    "type": "To be confirmed (e.g., MACE, cardiovascular death)",
    "time_window": "To be confirmed"
  },
  "time_zero": {
    "description": "To be confirmed",
    "event": ""
  },
  "missing_elements": ["comparator", "outcome.type", "outcome.time_window", "time_zero"]
}
Agent: Your protocol is missing the following key information. Please provide:
- What is the comparator? (e.g., metformin, other oral antidiabetic agents, etc.)
- What is the specific cardiovascular outcome measure? (e.g., MACE, cardiovascular death, etc.)
- What is the outcome assessment time window? (e.g., 1 year, 5 years)
- From which event should time zero be calculated? (e.g., date of first prescription, date of diagnosis)
```

**Example 2: General Research Analysis Mode**
```
User: I want to study the cardiovascular effects of diabetes medications
Agent: [Activate question_analyzer, identified as non-clinical comparative study]
Agent: I understand you want to explore the relationship between diabetes medications and cardiovascular health. Based on your idea, I have refined the following directions:
1. Compare cardiovascular outcomes across different classes of diabetes medications (e.g., SGLT2 inhibitors vs. GLP-1 receptor agonists)
2. Analyze the cardiovascular safety of diabetes medications in specific populations (e.g., elderly patients)
3. Investigate the effects of combination diabetes therapies on cardiovascular risk factors
Which direction would you prefer?
```

**Example 3: With File Input (General Mode)**
```
User: Here are some papers I've collected. Help me design a study on material fatigue life prediction.
    [Upload: literature_collection.zip]
Agent: [Read files, identify domain as "materials"]
Agent: Based on your uploaded literature and the topic of "material fatigue life prediction," I suggest focusing on...
```
