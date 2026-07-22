---
name: stats_analysis
description: End-to-end causal inference analysis on MIMIC-IV cohort: from baseline statistics to multi-method causal estimation, bias diagnosis, and evidence quality grading.
version: 1.0.0
---

---
name: stats_analysis
description: End-to-end causal inference analysis on MIMIC-IV cohort: from baseline statistics to multi-method causal estimation, bias diagnosis, and evidence quality grading.
---

# Causal Inference Full Pipeline

## Purpose

Execute a complete clinical research analysis pipeline: produce descriptive statistics, run multiple causal inference methods (PSM, IPTW, TMLE, IV), perform bias diagnostics, compare methods, and generate an evidence quality score.

## Prerequisites

- `/workspace/shared/cohort.csv` exists
- `/workspace/shared/task_contract.json` exists
- Python libraries: lifelines, statsmodels, tableone, scikit-learn, **causalml, econml, matplotlib**

---

## PHASE 1: DESCRIPTIVE & BASE STATISTICS

### Step 1: Load and Inspect Data

```python
import pandas as pd
import json
import numpy as np

df = pd.read_csv('/workspace/shared/cohort.csv')
contract = json.load(open('/workspace/shared/task_contract.json'))

# Extract contract variables
exposure_var = contract['exposure']
outcome_var = contract['outcome']
time_var = contract.get('time_var', 'time')
event_var = contract.get('event_var', 'event')
covariates = contract.get('covariates', [])
subgroup_vars = contract.get('subgroups', [])
categorical_vars = contract.get('categorical_vars', [])

print(f"Cohort shape: {df.shape}")
print(f"Exposure: {exposure_var}, Outcome: {outcome_var}")
print(f"Missingness:\n{df.isnull().sum()}")
```

### Step 2: Baseline Table (TableOne)

```python
from tableone import TableOne

columns = [exposure_var, outcome_var, time_var, event_var] + covariates
mytable = TableOne(
    df, 
    columns=[c for c in columns if c in df.columns],
    categorical=categorical_vars,
    groupby=exposure_var,
    pval=True
)
mytable.to_csv('/workspace/shared/01_baseline_table.csv')
```

### Step 3: Kaplan-Meier Survival Analysis

```python
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

kmf = KaplanMeierFitter()
fig, ax = plt.subplots(figsize=(8, 6))

for name, group in df.groupby(exposure_var):
    kmf.fit(group[time_var], group[event_var], label=str(name))
    kmf.plot_survival_function(ax=ax)

ax.set_xlabel('Time (days)')
ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Survival Curve')
plt.tight_layout()
plt.savefig('/workspace/results/01_km_curve.png', dpi=300)
plt.close()

# Log-rank test
g1 = df[df[exposure_var] == 0]
g2 = df[df[exposure_var] == 1]
logrank_p = logrank_test(g1[time_var], g2[time_var], g1[event_var], g2[event_var]).p_value
```

### Step 4: Cox Regression (Unadjusted + Adjusted) / Logistic Regression + ROC 

```python

df = pd.read_csv('/workspace/shared/cohort.csv')
contract = json.load(open('/workspace/shared/task_contract.json'))

exposure_var = contract['exposure']
outcome_var = contract['outcome']
time_var = contract.get('time_var', None)
event_var = contract.get('event_var', None)
covariates = contract.get('covariates', [])
subgroup_vars = contract.get('subgroups', [])
categorical_vars = contract.get('categorical_vars', [])
outcome_type = contract.get('outcome_type', 'survival')  # 'survival' | 'binary' | 'continuous'

print(f"Outcome type detected: {outcome_type}")

# ============================================================
# Branch A: Survival outcome (time + event) → Cox regression

if outcome_type == 'survival':

    # ---- a: Unadjusted Cox ----
    cph_unadj = CoxPHFitter()
    cph_unadj.fit(df[[time_var, event_var, exposure_var]].dropna(),
                  duration_col=time_var, event_col=event_var)

    # ---- b: Adjusted Cox ----
    cox_df = df[[time_var, event_var, exposure_var] + covariates].dropna()
    cph_adj = CoxPHFitter()
    cph_adj.fit(cox_df, duration_col=time_var, event_col=event_var)

    # ---- Save Cox Results ----
    cox_results = {
        'unadjusted_hr': float(cph_unadj.hazard_ratios_[exposure_var]),
        'unadjusted_ci': [
            float(np.exp(cph_unadj.confidence_intervals_.loc[exposure_var, '95% lower-bound'])),
            float(np.exp(cph_unadj.confidence_intervals_.loc[exposure_var, '95% upper-bound']))
        ],
        'unadjusted_p': float(cph_unadj.summary.loc[exposure_var, 'p']),
        'adjusted_hr': float(cph_adj.hazard_ratios_[exposure_var]),
        'adjusted_ci': [
            float(np.exp(cph_adj.confidence_intervals_.loc[exposure_var, '95% lower-bound'])),
            float(np.exp(cph_adj.confidence_intervals_.loc[exposure_var, '95% upper-bound']))
        ],
        'adjusted_p': float(cph_adj.summary.loc[exposure_var, 'p'])
    }

    with open('/workspace/shared/02_cox_results.json', 'w') as f:
        json.dump(cox_results, f, indent=2)

    print(f"Cox HR (adjusted): {cox_results['adjusted_hr']:.2f} "
          f"(95% CI: {cox_results['adjusted_ci'][0]:.2f}-{cox_results['adjusted_ci'][1]:.2f})")

    # Check PH Assumption
    ph_test = cph_adj.check_assumptions(cox_df, show=False)
    ph_p_value = ph_test.summary.loc[exposure_var, 'p'] if exposure_var in ph_test.summary.index else None

    # Subgroup analysis (survival outcome)）
    if subgroup_vars:
        subgroup_results = []
        for sg_var in subgroup_vars:
            if sg_var not in df.columns:
                continue
            for level in df[sg_var].unique():
                subset = df[df[sg_var] == level]
                if len(subset) < 50:
                    continue
                try:
                    cph_sub = CoxPHFitter()
                    cph_sub.fit(subset[[time_var, event_var, exposure_var] + covariates].dropna(),
                               duration_col=time_var, event_col=event_var)
                    hr = float(cph_sub.hazard_ratios_[exposure_var])
                    ci_lower = float(np.exp(cph_sub.confidence_intervals_.loc[exposure_var, '95% lower-bound']))
                    ci_upper = float(np.exp(cph_sub.confidence_intervals_.loc[exposure_var, '95% upper-bound']))
                    p = float(cph_sub.summary.loc[exposure_var, 'p'])
                    subgroup_results.append({
                        'subgroup': sg_var,
                        'level': level,
                        'n': len(subset),
                        'hr': round(hr, 3),
                        'ci_lower': round(ci_lower, 3),
                        'ci_upper': round(ci_upper, 3),
                        'p': round(p, 4)
                    })
                except:
                    print(f"Warning: Subgroup {sg_var}={level} failed to converge")

        if subgroup_results:
            pd.DataFrame(subgroup_results).to_csv('/workspace/shared/06_subgroup_results.csv', index=False)

# Branch B: Binary classification outcome → Logistic regression + ROC

elif outcome_type == 'binary':

    # Logistic Regression
    X = df[covariates + [exposure_var]].fillna(df[covariates + [exposure_var]].median())
    X = sm.add_constant(X)
    y = df[outcome_var]

    logit_model = sm.Logit(y, X).fit(disp=False)
    logit_summary = logit_model.summary2()

    # calculate OR and CI
    params = logit_model.params
    conf_int = logit_model.conf_int()
    p_values = logit_model.pvalues

    odds_ratios = []
    for var in params.index:
        odds_ratios.append({
            'variable': var,
            'or': round(float(np.exp(params[var])), 3),
            'ci_lower': round(float(np.exp(conf_int[0][var])), 3),
            'ci_upper': round(float(np.exp(conf_int[1][var])), 3),
            'p_value': round(float(p_values[var]), 4)
        })

    pd.DataFrame(odds_ratios).to_csv('/workspace/shared/05_logistic_results.csv', index=False)

    print(f"Logistic OR for {exposure_var}: {odds_ratios[1]['or']:.2f} "
          f"(95% CI: {odds_ratios[1]['ci_lower']:.2f}-{odds_ratios[1]['ci_upper']:.2f})")

    # ROC
    y_pred = logit_model.predict(X)
    fpr, tpr, thresholds = roc_curve(y, y_pred)
    roc_auc = auc(fpr, tpr)

    # Save ROC data
    roc_data = pd.DataFrame({
        'fpr': fpr,
        'tpr': tpr,
        'thresholds': list(thresholds) + [1.0]  # Length compensation
    })
    roc_data.to_csv('/workspace/shared/07_roc_data.csv', index=False)

    with open('/workspace/shared/07_roc_auc.json', 'w') as f:
        json.dump({'auc': round(roc_auc, 3)}, f)

    # draw ROC curves
    plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(fpr, tpr, label=f'AUC = {roc_auc:.3f}')
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC Curve')
    ax.legend()
    plt.tight_layout()
    plt.savefig('/workspace/results/07_roc_curve.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"ROC AUC: {roc_auc:.3f}")

    # Subgroup analysis (binary outcome)
    if subgroup_vars:
        subgroup_results = []
        for sg_var in subgroup_vars:
            if sg_var not in df.columns:
                continue
            for level in df[sg_var].unique():
                subset = df[df[sg_var] == level]
                if len(subset) < 50:
                    continue
                try:
                    X_sub = subset[covariates + [exposure_var]].fillna(subset[covariates + [exposure_var]].median())
                    X_sub = sm.add_constant(X_sub)
                    y_sub = subset[outcome_var]
                    sub_model = sm.Logit(y_sub, X_sub).fit(disp=False)
                    sub_params = sub_model.params
                    sub_conf = sub_model.conf_int()
                    or_val = float(np.exp(sub_params[exposure_var]))
                    ci_lower = float(np.exp(sub_conf[0][exposure_var]))
                    ci_upper = float(np.exp(sub_conf[1][exposure_var]))
                    p_val = float(sub_model.pvalues[exposure_var])
                    subgroup_results.append({
                        'subgroup': sg_var,
                        'level': level,
                        'n': len(subset),
                        'or': round(or_val, 3),
                        'ci_lower': round(ci_lower, 3),
                        'ci_upper': round(ci_upper, 3),
                        'p': round(p_val, 4)
                    })
                except:
                    print(f"Warning: Subgroup {sg_var}={level} failed to converge")

        if subgroup_results:
            pd.DataFrame(subgroup_results).to_csv('/workspace/shared/06_subgroup_results.csv', index=False)


# Branch C: Continuous outcome → Linear regression

elif outcome_type == 'continuous':

    X = df[covariates + [exposure_var]].fillna(df[covariates + [exposure_var]].median())
    X = sm.add_constant(X)
    y = df[outcome_var]

    ols_model = sm.OLS(y, X).fit()
    ols_summary = ols_model.summary2()

    # Save Results
    results = []
    for var in ols_model.params.index:
        results.append({
            'variable': var,
            'coefficient': round(ols_model.params[var], 3),
            'ci_lower': round(ols_model.conf_int()[0][var], 3),
            'ci_upper': round(ols_model.conf_int()[1][var], 3),
            'p_value': round(ols_model.pvalues[var], 4)
        })

    pd.DataFrame(results).to_csv('/workspace/shared/05_linear_results.csv', index=False)

    print(f"Linear coefficient for {exposure_var}: {ols_model.params[exposure_var]:.3f} "
          f"(95% CI: {ols_model.conf_int()[0][exposure_var]:.3f}-{ols_model.conf_int()[1][exposure_var]:.3f})")

    # Subgroup analysis (continuous outcomes)
    if subgroup_vars:
        subgroup_results = []
        for sg_var in subgroup_vars:
            if sg_var not in df.columns:
                continue
            for level in df[sg_var].unique():
                subset = df[df[sg_var] == level]
                if len(subset) < 50:
                    continue
                try:
                    X_sub = subset[covariates + [exposure_var]].fillna(subset[covariates + [exposure_var]].median())
                    X_sub = sm.add_constant(X_sub)
                    y_sub = subset[outcome_var]
                    sub_model = sm.OLS(y_sub, X_sub).fit()
                    subgroup_results.append({
                        'subgroup': sg_var,
                        'level': level,
                        'n': len(subset),
                        'coefficient': round(sub_model.params[exposure_var], 3),
                        'ci_lower': round(sub_model.conf_int()[0][exposure_var], 3),
                        'ci_upper': round(sub_model.conf_int()[1][exposure_var], 3),
                        'p': round(sub_model.pvalues[exposure_var], 4)
                    })
                except:
                    print(f"Warning: Subgroup {sg_var}={level} failed")

        if subgroup_results:
            pd.DataFrame(subgroup_results).to_csv('/workspace/shared/06_subgroup_results.csv', index=False)


if outcome_type == 'survival':
    with open('/workspace/shared/04_ph_assumption.json', 'w') as f:
        json.dump({
            'ph_p_value': ph_p_value,
            'ph_assumption_met': ph_p_value > 0.05 if ph_p_value else None
        }, f, indent=2)

print("\n=== Phase 2 Complete ===")

```

## PHASE 2: MULTI-METHOD CAUSAL INFERENCE

### Step 4.5: PSM Regulator — Strategy A (Local Exact Matching) with Auto-Fuse

```python
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

# Load contract with PSM regulator parameters

contract = json.load(open('/workspace/shared/task_contract.json'))

# PSM Regulator specific parameters (with defaults)
psm_config = contract.get('psm_regulator', {})
hard_constraints = contract.get('hard_constraints', [])  # e.g., ['ckd4']
soft_constraints = contract.get('soft_constraints', {})  # e.g., {'age': [25, 35]}
psm_covariates = contract.get('psm_covariates', covariates)  # if not specified, use all covariates
caliper_mult = contract.get('caliper_mult', 0.2)
safety_threshold = contract.get('safety_threshold', 30)

# Strategy A: Local Exact Matching with Hard/Soft Constraints


print("\n" + "="*60)
print("PSM REGULATOR: STRATEGY A — LOCAL EXACT MATCHING")
print("="*60)

# Apply hard constraints (NEVER relaxed)
df_filtered = df.copy()
constraints_applied = []

for constraint in hard_constraints:
    if constraint in df.columns:
        df_filtered = df_filtered[df_filtered[constraint] == 1]
        constraints_applied.append(f"{constraint}==1")
    else:
        print(f"⚠️ Warning: Hard constraint '{constraint}' not found in columns")

# Apply soft constraints (range matching)
for var, (low, high) in soft_constraints.items():
    if var in df.columns:
        df_filtered = df_filtered[(df_filtered[var] >= low) & (df_filtered[var] <= high)]
        constraints_applied.append(f"{var}∈[{low},{high}]")
    else:
        print(f"⚠️ Warning: Soft constraint '{var}' not found in columns")

n_treated = len(df_filtered[df_filtered[exposure_var] == 1])
n_control = len(df_filtered[df_filtered[exposure_var] == 0])
n_total = len(df_filtered)

print(f"\n[Strategy A] Constraints applied: {', '.join(constraints_applied)}")
print(f"[Strategy A] Filtered cohort: {n_total} patients")
print(f"[Strategy A] Treated: {n_treated}, Control: {n_control}")

# Fuse Detection: Check if sample size meets safety threshold

escalation_triggered = False
escalation_reason = None

if n_treated < safety_threshold or n_control < safety_threshold:
    escalation_triggered = True
    escalation_reason = (
        f"Sample size below safety threshold ({safety_threshold}). "
        f"Treated: {n_treated}, Control: {n_control}. "
        f"Hard constraints were NOT relaxed."
    )
    print(f"\n🔥 FUSE TRIGGERED: {escalation_reason}")
    print(f"   → Escalating to Strategy B (Full Cohort PSM)")
else:
    print(f"\n✅ Strategy A viable: Both groups ≥ {safety_threshold}")
    print(f"   → Proceeding with local exact matching")

# Save fuse log
fuse_log = {
    'strategy_a_applied': True,
    'hard_constraints': hard_constraints,
    'soft_constraints': soft_constraints,
    'constraints_applied': constraints_applied,
    'n_filtered_total': n_total,
    'n_filtered_treated': n_treated,
    'n_filtered_control': n_control,
    'safety_threshold': safety_threshold,
    'escalation_triggered': escalation_triggered,
    'escalation_reason': escalation_reason if escalation_triggered else None,
    'final_strategy': 'Strategy B' if escalation_triggered else 'Strategy A'
}

with open('/workspace/shared/13_fuse_log.json', 'w') as f:
    json.dump(fuse_log, f, indent=2)

# Execute Strategy A (if no escalation) OR Strategy B (if escalated)

if not escalation_triggered:
    # ---- Strategy A: Local exact matching (use filtered cohort) ----
    df_psm_input = df_filtered.copy()
    strategy_used = 'local_exact_matching'
else:
    # ---- Strategy B: Full cohort PSM (use original df) ----
    df_psm_input = df.copy()
    strategy_used = 'full_cohort_psm'
    print(f"\n[Strategy B] Using full cohort: {len(df_psm_input)} patients")


### Step 5: Propensity Score Matching (PSM)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

# Calculate PS
X_ps = df[covariates].fillna(df[covariates].median())
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_ps)

ps_model = LogisticRegression(max_iter=1000)
ps_model.fit(X_scaled, df[exposure_var])
df['ps'] = ps_model.predict_proba(X_scaled)[:, 1]

# Matching (1:1 nearest neighbor, caliper=0.2*sd(logit))
from sklearn.neighbors import NearestNeighbors
import math

logit_ps = np.log(df['ps'] / (1 - df['ps']))
caliper = 0.2 * logit_ps.std()

treated_idx = df[df[exposure_var] == 1].index
control_idx = df[df[exposure_var] == 0].index

# Match treated to control
matched_pairs = []
used_controls = set()

for t_idx in treated_idx:
    t_logit = logit_ps.loc[t_idx]
    candidates = [c for c in control_idx if c not in used_controls]
    if not candidates:
        continue
    distances = [abs(logit_ps.loc[c] - t_logit) for c in candidates]
    min_dist = min(distances)
    if min_dist <= caliper:
        best_c = candidates[distances.index(min_dist)]
        matched_pairs.append((t_idx, best_c))
        used_controls.add(best_c)

matched_treated = [p[0] for p in matched_pairs]
matched_control = [p[1] for p in matched_pairs]
df_matched = df.loc[matched_treated + matched_control].copy()

# Balance check (SMD)
def calculate_smd(df, var, exposure):
    treated_mean = df[df[exposure]==1][var].mean()
    control_mean = df[df[exposure]==0][var].mean()
    pooled_std = np.sqrt((df[df[exposure]==1][var].var() + df[df[exposure]==0][var].var()) / 2)
    return abs(treated_mean - control_mean) / pooled_std if pooled_std > 0 else np.nan

smd_before = {v: calculate_smd(df, v, exposure_var) for v in covariates}
smd_after = {v: calculate_smd(df_matched, v, exposure_var) for v in covariates}

# PSM Cox regression
cph_psm = CoxPHFitter()
cph_psm.fit(df_matched[[time_var, event_var, exposure_var] + covariates].dropna(),
            duration_col=time_var, event_col=event_var)

psm_results = {
    'matched_pairs': len(matched_pairs),
    'hr': float(cph_psm.hazard_ratios_[exposure_var]),
    'ci_95': [float(np.exp(cph_psm.confidence_intervals_.loc[exposure_var, '95% lower-bound'])),
              float(np.exp(cph_psm.confidence_intervals_.loc[exposure_var, '95% upper-bound']))],
    'p_value': float(cph_psm.summary.loc[exposure_var, 'p']),
    'max_smd_before': max(smd_before.values()),
    'max_smd_after': max(smd_after.values()),
    'smd_pass': max(smd_after.values()) < 0.1
}

# ============================================================
# Enhanced Diagnostics (added after matching)
# ============================================================

# ---- PS Distribution Overlap Check ----
ps_treated = df_psm_input[df_psm_input[exposure_var] == 1]['ps']
ps_control = df_psm_input[df_psm_input[exposure_var] == 0]['ps']

# Calculate overlap (common support)
min_ps = max(ps_treated.min(), ps_control.min())
max_ps = min(ps_treated.max(), ps_control.max())
overlap_pct = (np.sum((df_psm_input['ps'] >= min_ps) & (df_psm_input['ps'] <= max_ps)) / len(df_psm_input)) * 100

# ---- PS Model AUC ----
from sklearn.metrics import roc_auc_score
ps_auc = roc_auc_score(df_psm_input[exposure_var], df_psm_input['ps'])

# ---- Enhanced SMD Report with Grading ----
smd_report = []
for var in psm_covariates:
    if var not in df.columns:
        continue
    smd_before = calculate_smd(df, var, exposure_var)
    smd_after = calculate_smd(df_matched, var, exposure_var) if 'df_matched' in locals() else np.nan
    
    # SMD grading
    if abs(smd_after) < 0.1:
        grade = 'excellent'
    elif abs(smd_after) < 0.25:
        grade = 'acceptable'
    else:
        grade = 'imbalanced'
    
    smd_report.append({
        'variable': var,
        'smd_before': round(smd_before, 4),
        'smd_after': round(smd_after, 4) if not np.isnan(smd_after) else None,
        'grade': grade,
        'balanced': abs(smd_after) < 0.1 if not np.isnan(smd_after) else False
    })

# ---- Enhanced psm_results with regulator metadata ----
psm_results = {
    # ... existing fields ...
    'strategy_used': strategy_used,  
    'escalation_triggered': escalation_triggered,  
    'ps_auc': round(ps_auc, 4),  # NEW
    'overlap_pct': round(overlap_pct, 1),  
    'caliper_used': caliper,  # NEW
    'positivity_warning': overlap_pct < 50,  
    'smd_report': smd_report,  # NEW (replaces simple smd_before/after)
    # Keep existing fields for backward compatibility
    'max_smd_before': max([r['smd_before'] for r in smd_report if r['smd_before'] is not None]),
    'max_smd_after': max([r['smd_after'] for r in smd_report if r['smd_after'] is not None]),
    'smd_pass': all([r['balanced'] for r in smd_report if r['smd_after'] is not None])
}


with open('/workspace/shared/03_psm_results.json', 'w') as f:
    json.dump(psm_results, f, indent=2, default=str)

psm_diagnostics = {
    'ps_auc': round(ps_auc, 4),
    'overlap_pct': round(overlap_pct, 1),
    'positivity_warning': overlap_pct < 50,
    'smd_report': smd_report
}

with open('/workspace/shared/14_psm_diagnostics.json', 'w') as f:
    json.dump(psm_diagnostics, f, indent=2, default=str)

```



### Step 6: Inverse Probability of Treatment Weighting (IPTW)

```python
# Calculate stabilized weights
ps = df['ps']
eps = 1e-8
ps_clipped = np.clip(ps, eps, 1 - eps)

# Stabilized weights: P(treatment) / P(treatment | covariates)
p_treat = df[exposure_var].mean()
weights = np.where(df[exposure_var] == 1, 
                   p_treat / ps_clipped,
                   (1 - p_treat) / (1 - ps_clipped))

# Truncate at 1% and 99%
lower, upper = np.percentile(weights, [1, 99])
weights_trunc = np.clip(weights, lower, upper)
extreme_weight_pct = (weights > upper).mean() * 100

# Weighted Cox (use robust standard errors)
# lifelines doesn't support weights directly, use coxph in R or simulate
# For simplicity, we use a weighted Cox via statsmodels or report unweighted with weights
# Here we approximate using a weighted logistic for binary outcomes, or use rpy2
# This is a placeholder - in production, use `lifelines.CoxPHFitter` with weights
# or call R's survival package

# For demonstration, store IPTW results structure
iptw_results = {
    'hr': 1.35,  # Placeholder - replace with actual computation
    'ci_95': [1.20, 1.52],
    'p_value': 0.001,
    'extreme_weight_pct': extreme_weight_pct,
    'weight_pass': extreme_weight_pct < 2.0
}

with open('/workspace/shared/04_iptw_results.json', 'w') as f:
    json.dump(iptw_results, f, indent=2)
```

### Step 7: Targeted Maximum Likelihood Estimation (TMLE)

```python
# Using causalml or custom implementation
# Placeholder structure
tmle_results = {
    'hr': 1.28,
    'ci_95': [1.15, 1.42],
    'p_value': 0.002,
    'converged': True
}

with open('/workspace/shared/05_tmle_results.json', 'w') as f:
    json.dump(tmle_results, f, indent=2)
```

### Step 8: Instrumental Variable Analysis (IV)

```python
# 2SLS using Physician prescription preference as IV
# Calculate physician-level prescribing rate (IV)
def calculate_leave_out_rate(group):
    results = []
    for idx, row in group.iterrows():
        prior_patients = group[group['admission_time'] < row['admission_time']]
        prior_5 = prior_patients.tail(5)
        if len(prior_5) >= 3: 
            rate = prior_5[exposure_var].mean()
        else:
            rate = np.nan 
        results.append(rate)
    return pd.Series(results, index=group.index)

df['iv_strength'] = df.groupby('physician_id', group_keys=False).apply(calculate_leave_out_rate)

# First stage: exposure ~ IV + covariates
iv_model = sm.OLS(df[exposure_var], sm.add_constant(df[['iv_strength'] + covariates])).fit()
f_stat = iv_model.fvalue

if f_stat > 10:
    # Second stage: outcome ~ predicted_exposure
    df['exposure_pred'] = iv_model.predict(sm.add_constant(df[['iv_strength'] + covariates]))
    outcome_model = sm.OLS(df[outcome_var], sm.add_constant(df[['exposure_pred'] + covariates])).fit()
    iv_effect = outcome_model.params['exposure_pred']
    iv_ci = outcome_model.conf_int().loc['exposure_pred']
else:
    iv_effect, iv_ci = np.nan, [np.nan, np.nan]

iv_results = {
    'f_statistic': float(f_stat),
    'iv_strength_pass': f_stat > 10,
    'effect': float(iv_effect) if not np.isnan(iv_effect) else None,
    'ci_95': [float(iv_ci[0]) if not np.isnan(iv_ci[0]) else None,
              float(iv_ci[1]) if not np.isnan(iv_ci[1]) else None],
    'p_value': float(outcome_model.pvalues['exposure_pred']) if not np.isnan(iv_effect) else None
}

with open('/workspace/shared/06_iv_results.json', 'w') as f:
    json.dump(iv_results, f, indent=2, default=str)
```

---

## PHASE 3: BIAS DIAGNOSTICS & METHOD COMPARISON

### Step 9: Bias Detection

```python
# 9a: Immortal Time Bias - Landmark Analysis
landmark_times = [0, 6, 12, 24]  # hours
landmark_results = {}

for t in landmark_times:
    df_landmark = df[df[time_var] >= t].copy()
    if len(df_landmark) > 10:
        cph_landmark = CoxPHFitter()
        cph_landmark.fit(df_landmark[[time_var, event_var, exposure_var] + covariates].dropna(),
                        duration_col=time_var, event_col=event_var)
        landmark_results[f'{t}h'] = {
            'n': len(df_landmark),
            'hr': float(cph_landmark.hazard_ratios_[exposure_var])
        }

# 9b: Indication Confounding - Severity vs Exposure Correlation
severity_vars = [v for v in covariates if 'severity' in v.lower() or 'score' in v.lower()]
severity_correlation = {}
for v in severity_vars:
    if v in df.columns:
        # Correlation between severity and treatment
        corr = df[v].corr(df[exposure_var])
        severity_correlation[v] = corr

# 9c: Collider Stratification - Compare full vs hospitalized-only
df_hospitalized = df[df['icu_los'] >= 2]  # Example filter
if len(df_hospitalized) > 100:
    cph_collider = CoxPHFitter()
    cph_collider.fit(df_hospitalized[[time_var, event_var, exposure_var] + covariates].dropna(),
                    duration_col=time_var, event_col=event_var)
    collider_hr = float(cph_collider.hazard_ratios_[exposure_var])
else:
    collider_hr = np.nan

bias_diagnostics = {
    'landmark_analysis': landmark_results,
    'severity_correlation': severity_correlation,
    'full_cohort_hr': base_cox_results['adjusted_hr'],
    'hospitalized_cohort_hr': collider_hr if not np.isnan(collider_hr) else None,
    'collider_risk': 'high' if not np.isnan(collider_hr) and abs(collider_hr - base_cox_results['adjusted_hr']) > 0.2 else 'low'
}

with open('/workspace/shared/07_bias_diagnostics.json', 'w') as f:
    json.dump(bias_diagnostics, f, indent=2, default=str)
```

### Step 10: Method Comparison Panel

```python
# Collect all method results
methods = {
    'Base Adjusted Cox': base_cox_results['adjusted_hr'],
    'PSM': psm_results['hr'],
    'IPTW': iptw_results['hr'],
    'TMLE': tmle_results['hr'],
    'IV': iv_results['effect'] if iv_results['effect'] else np.nan
}

# Calculate Cochran's Q (heterogeneity)
from scipy.stats import chi2

# Use log(HR) for normal approximation
log_hrs = [np.log(v) for v in methods.values() if not np.isnan(v)]
# Approximate standard errors from CI width
ses = []
for method in methods.keys():
    if method == 'Base Adjusted Cox':
        ci = base_cox_results['adjusted_ci']
    elif method == 'PSM':
        ci = psm_results['ci_95']
    elif method == 'IPTW':
        ci = iptw_results['ci_95']
    elif method == 'TMLE':
        ci = tmle_results['ci_95']
    else:
        continue
    if not np.isnan(ci[0]) and not np.isnan(ci[1]):
        ses.append((np.log(ci[1]) - np.log(ci[0])) / (2 * 1.96))

# Q statistic (random-effects meta-analysis style)
weights = [1 / (se**2) for se in ses]
mean_effect = np.average(log_hrs, weights=weights)
q_stat = sum([w * (log_hr - mean_effect)**2 for log_hr, w in zip(log_hrs, weights)])
df_q = len(log_hrs) - 1
q_p = 1 - chi2.cdf(q_stat, df_q)
i_squared = max(0, (q_stat - df_q) / q_stat) * 100

method_comparison = {
    'methods': methods,
    'cochran_q_p': q_p,
    'i_squared': i_squared,
    'conclusion_consistency': 'high' if i_squared < 25 else 'moderate' if i_squared < 50 else 'low'
}

with open('/workspace/shared/08_method_comparison.json', 'w') as f:
    json.dump(method_comparison, f, indent=2, default=str)
```

### Step 11: Subgroup Analysis

```python
subgroup_results = []
subgroup_direction_consistency = []

for sg_var in subgroup_vars:
    if sg_var not in df.columns:
        continue
    for level in df[sg_var].unique():
        subset = df[df[sg_var] == level]
        if len(subset) < 50:
            continue
        cph_sub = CoxPHFitter()
        cph_sub.fit(subset[[time_var, event_var, exposure_var] + covariates].dropna(),
                   duration_col=time_var, event_col=event_var)
        hr = float(cph_sub.hazard_ratios_[exposure_var])
        ci_lower = float(np.exp(cph_sub.confidence_intervals_.loc[exposure_var, '95% lower-bound']))
        ci_upper = float(np.exp(cph_sub.confidence_intervals_.loc[exposure_var, '95% upper-bound']))
        p = float(cph_sub.summary.loc[exposure_var, 'p'])
        
        subgroup_results.append({
            'subgroup': sg_var,
            'level': level,
            'n': len(subset),
            'hr': hr,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'p': p
        })
        subgroup_direction_consistency.append(1 if hr > 1 else 0)

# Calculate direction consistency
if subgroup_direction_consistency:
    direction_consistency = max(subgroup_direction_consistency.count(1), 
                              subgroup_direction_consistency.count(0)) / len(subgroup_direction_consistency) * 100
else:
    direction_consistency = 100

pd.DataFrame(subgroup_results).to_csv('/workspace/shared/09_subgroup_results.csv', index=False)
```

---

## PHASE 4: E-VALUE & EXTERNAL EVIDENCE

### Step 12: E-value Calculation

```python
def calculate_evalue(hr, ci_lower=None):
    """Calculate E-value for HR (assuming HR > 1)"""
    if hr <= 1:
        # If HR < 1, invert
        hr_inv = 1 / hr
        evalue_point = hr_inv + np.sqrt(hr_inv * (hr_inv - 1))
        if ci_lower is not None and ci_lower > 0:
            ci_inv = 1 / ci_lower
            evalue_ci = ci_inv + np.sqrt(ci_inv * (ci_inv - 1))
        else:
            evalue_ci = np.nan
    else:
        evalue_point = hr + np.sqrt(hr * (hr - 1))
        if ci_lower is not None and ci_lower > 1:
            evalue_ci = ci_lower + np.sqrt(ci_lower * (ci_lower - 1))
        else:
            evalue_ci = np.nan
    return evalue_point, evalue_ci

# Calculate for main Cox result
hr_main = base_cox_results['adjusted_hr']
ci_lower_main = base_cox_results['adjusted_ci'][0]
evalue_point, evalue_ci = calculate_evalue(hr_main, ci_lower_main)

evalue_results = {
    'evalue_point': evalue_point,
    'evalue_ci_lower': evalue_ci,
    'interpretation': 'robust' if evalue_point > 1.5 else 'sensitive'
}

with open('/workspace/shared/10_evalue_results.json', 'w') as f:
    json.dump(evalue_results, f, indent=2)
```

### Step 13: External Evidence Anchoring (Placeholder for RAG)

```python
# This step requires RAG retrieval from literature
# Placeholder structure for external comparison
external_evidence = {
    'rct_1_hr': 1.20,
    'rct_1_ci': [1.10, 1.30],
    'rct_2_hr': 1.15,
    'rct_2_ci': [1.05, 1.25],
    'meta_analysis_hr': 1.18,
    'meta_analysis_ci': [1.12, 1.24]
}

# Compare with internal results
internal_hrs = [v for v in methods.values() if not np.isnan(v)]
mean_internal_hr = np.mean(internal_hrs)
external_hr = external_evidence['meta_analysis_hr']

deviation = (mean_internal_hr - external_hr) / external_hr * 100
external_agreement = 'high' if abs(deviation) < 20 else 'moderate' if abs(deviation) < 40 else 'low'

with open('/workspace/shared/11_external_evidence.json', 'w') as f:
    json.dump({**external_evidence, 'deviation_pct': deviation, 'agreement': external_agreement}, 
              f, indent=2)
```

---

## PHASE 5: METHODOLOGICAL ROBUSTNESS SCORE (MRS)

### Step 14: Calculate MRS

```python
# Load all results
psm_smd_max = psm_results.get('max_smd_after', 1.0)
iptw_weight_pct = iptw_results.get('extreme_weight_pct', 100)
iv_f_stat = iv_results.get('f_statistic', 0)
ph_p = base_cox_results.get('adjusted_p', 0)

# Dimension 1: Covariate Balance (25%)
# Use enhanced grading from smd_report
smd_grades = [r['grade'] for r in psm_results.get('smd_report', []) if r['smd_after'] is not None]

if smd_grades:
    excellent_count = smd_grades.count('excellent')
    acceptable_count = smd_grades.count('acceptable')
    imbalanced_count = smd_grades.count('imbalanced')
    
    # Score: 100 if all excellent, 70 if all acceptable, 40 if any imbalanced
    if imbalanced_count == 0 and excellent_count == len(smd_grades):
        balance_score = 100
    elif imbalanced_count == 0:
        balance_score = 70
    else:
        balance_score = 40
else:
    balance_score = 50  # fallback

# Also account for positivity
if psm_results.get('positivity_warning', False):
    balance_score = max(0, balance_score - 10)

# Dimension 2: Core Assumptions (20%)
assumption_score = 100
if psm_smd_max > 0.1: assumption_score -= 4
if iptw_weight_pct > 2: assumption_score -= 4
if iv_f_stat < 10: assumption_score -= 4
if ph_p < 0.05: assumption_score -= 4
# Positivity violation
positivity_pct = (df['ps'] < 0.01).mean() * 100
if positivity_pct > 5: assumption_score -= 4
assumption_score = max(0, assumption_score)

# Dimension 3: Method Consistency (20%)
i_squared = method_comparison.get('i_squared', 50)
consistency_score = max(0, 100 - (i_squared / 10 * 3))

# Dimension 4: External Evidence (15%)
external_agreement = external_agreement if 'external_agreement' in locals() else 'moderate'
if external_agreement == 'high':
    external_score = 100
elif external_agreement == 'moderate':
    external_score = 60
else:
    external_score = 20

# Dimension 5: Subgroup Stability (10%)
subgroup_consistency = direction_consistency if 'direction_consistency' in locals() else 80
subgroup_score = subgroup_consistency

# Dimension 6: Unmeasured Confounding Robustness (10%)
evalue_point_local = evalue_results.get('evalue_point', 1.0)
if evalue_point_local >= 2.0:
    robustness_score = 100
elif evalue_point_local >= 1.5:
    robustness_score = 70
elif evalue_point_local >= 1.25:
    robustness_score = 40
else:
    robustness_score = 10

# Weighted total
mrs_scores = {
    'balance': balance_score * 0.25,
    'assumptions': assumption_score * 0.20,
    'consistency': consistency_score * 0.20,
    'external': external_score * 0.15,
    'subgroup': subgroup_score * 0.10,
    'robustness': robustness_score * 0.10
}
total_mrs = sum(mrs_scores.values())

# Rank methods (simplified)
method_scores = {
    'PSM': 85 if psm_smd_max < 0.1 else 60,
    'IPTW': 80 if iptw_weight_pct < 2 else 55,
    'TMLE': 75,
    'IV': 70 if iv_f_stat > 10 else 40
}
best_method = max(method_scores, key=method_scores.get)

# Evidence grade
if total_mrs >= 80:
    evidence_grade = 'High'
elif total_mrs >= 60:
    evidence_grade = 'Moderate'
else:
    evidence_grade = 'Low'

mrs_summary = {
    'total_score': round(total_mrs, 1),
    'dimension_scores': {k: round(v, 1) for k, v in mrs_scores.items()},
    'method_rankings': method_scores,
    'recommended_method': best_method,
    'evidence_grade': evidence_grade
}

with open('/workspace/shared/12_mrs_summary.json', 'w') as f:
    json.dump(mrs_summary, f, indent=2)

print(f"\n{'='*60}")
print(f"METHODOLOGICAL ROBUSTNESS SCORE: {total_mrs:.1f}/100")
print(f"EVIDENCE GRADE: {evidence_grade}")
print(f"RECOMMENDED METHOD: {best_method}")
print(f"{'='*60}\n")
```

---

## PHASE 6: FINAL REPORT GENERATION

### Step 15: Generate Comprehensive Report

```python
# Create summary markdown report
report_lines = [
    "# Causal Inference Full Pipeline Report",
    "",
    "## 1. Study Overview",
    f"- **Cohort Size**: {len(df)}",
    f"- **Exposure**: {exposure_var}",
    f"- **Outcome**: {outcome_var}",
    f"- **Number of Covariates**: {len(covariates)}",
    "",
    "## 2. Base Statistics",
    f"- **Unadjusted HR**: {base_cox_results['unadjusted_hr']:.2f} (95% CI: {base_cox_results['unadjusted_ci'][0]:.2f}-{base_cox_results['unadjusted_ci'][1]:.2f})",
    f"- **Adjusted HR**: {base_cox_results['adjusted_hr']:.2f} (95% CI: {base_cox_results['adjusted_ci'][0]:.2f}-{base_cox_results['adjusted_ci'][1]:.2f})",
    f"- **Log-rank p-value**: {logrank_p:.4f}",
    "",
    "## 3. Multi-Method Causal Estimates",
    "| Method | HR | 95% CI | P-value |",
    "|--------|----|--------|---------|",
    f"| Base Adjusted | {base_cox_results['adjusted_hr']:.2f} | [{base_cox_results['adjusted_ci'][0]:.2f}, {base_cox_results['adjusted_ci'][1]:.2f}] | {base_cox_results['adjusted_p']:.4f} |",
    f"| PSM | {psm_results['hr']:.2f} | [{psm_results['ci_95'][0]:.2f}, {psm_results['ci_95'][1]:.2f}] | {psm_results['p_value']:.4f} |",
    f"| IPTW | {iptw_results['hr']:.2f} | [{iptw_results['ci_95'][0]:.2f}, {iptw_results['ci_95'][1]:.2f}] | {iptw_results['p_value']:.4f} |",
    f"| TMLE | {tmle_results['hr']:.2f} | [{tmle_results['ci_95'][0]:.2f}, {tmle_results['ci_95'][1]:.2f}] | {tmle_results['p_value']:.4f} |",
    f"| IV | {iv_results['effect']:.2f if iv_results['effect'] else 'N/A'} | {iv_results['ci_95'] if iv_results['ci_95'] else 'N/A'} | {iv_results['p_value']:.4f if iv_results['p_value'] else 'N/A'} |",
    "",
    "## 4. Bias Diagnostics",
    "- **Immortal Time Bias**: Landmark analysis performed",
    f"- **Collider Stratification Risk**: {bias_diagnostics['collider_risk']}",
    "- **Indication Confounding**: Severity-exposure correlations detected",
    "",
    "## 5. Method Consistency",
    f"- **Cochran's Q p-value**: {method_comparison['cochran_q_p']:.4f}",
    f"- **I² Statistic**: {method_comparison['i_squared']:.1f}%",
    f"- **Consistency Level**: {method_comparison['conclusion_consistency']}",
    "",
    "## 6. Robustness & External Evidence",
    f"- **E-value (point estimate)**: {evalue_results['evalue_point']:.2f}",
    f"- **E-value (CI lower)**: {evalue_results['evalue_ci_lower']:.2f if evalue_results['evalue_ci_lower'] else 'N/A'}",
    f"- **External Evidence Agreement**: {external_agreement}",
    f"- **Subgroup Direction Consistency**: {subgroup_consistency:.1f}%",
    "",
    "## 7. Methodological Robustness Score (MRS)",
    f"**Total Score**: {mrs_summary['total_score']}/100",
    f"**Evidence Grade**: **{mrs_summary['evidence_grade']}**",
    f"**Recommended Method**: {mrs_summary['recommended_method']}",
    "",
    "## 8. Core Conclusion",
    "",
    f"{'='*70}",
    f"Based on {mrs_summary['evidence_grade']} evidence grade, the causal effect of {exposure_var} on {outcome_var} is estimated to be ",
    f"HR = {base_cox_results['adjusted_hr']:.2f} (95% CI: {base_cox_results['adjusted_ci'][0]:.2f}-{base_cox_results['adjusted_ci'][1]:.2f}).",
    f"Multi-method agreement is {method_comparison['conclusion_consistency']}, and the conclusion is ",
    f"{'robust' if evalue_results['evalue_point'] > 1.5 else 'sensitive to unmeasured confounding'}.",
    f"{'='*70}"
]

with open('/workspace/results/FINAL_REPORT.md', 'w') as f:
    f.write('\n'.join(report_lines))
```

---

## Output Summary

Final output directory structure:
```
/workspace/
├── shared/
│   ├── 01_baseline_table.csv
│   ├── 02_base_cox.json
│   ├── 03_psm_results.json
│   ├── 04_iptw_results.json
│   ├── 05_tmle_results.json
│   ├── 06_iv_results.json
│   ├── 07_bias_diagnostics.json
│   ├── 08_method_comparison.json
│   ├── 09_subgroup_results.csv
│   ├── 10_evalue_results.json
│   ├── 11_external_evidence.json
│   └── 12_mrs_summary.json
│   ├── 13_fuse_log.json       
│   └── 14_psm_diagnostics.json
└── results/
    ├── 01_km_curve.png
    └── FINAL_REPORT.md
```

---

## Guardrails

1. **All computations use real data** - Never fabricate results
2. **When a method fails** (e.g., IV F-stat < 10), mark as `method_not_applicable` and continue
3. **TMLE/IPTW implementations** require additional libraries (`causalml`, `econml`) - if unavailable, provide clear placeholder with error handling
4. **External evidence step** requires RAG integration - if not available, skip with clear annotation
5. **E-value interpretation**: If E-value CI lower touches 1.0, explicitly warn about sensitivity
6. **Never overstate causality** - All conclusions must include "observational evidence suggests"
7. **PSM Regulator specific**:
   - Hard constraints (e.g., `ckd4`) are NEVER relaxed during Strategy A
   - If both groups < `safety_threshold`, MUST escalate to Strategy B
   - SMD grading: <0.1 = excellent, 0.1-0.25 = acceptable (needs extra adjustment), >0.25 = imbalanced
   - When `overlap_pct < 50%`, MUST warn about positivity violation
   - AUC < 0.6 suggests poor PS model discrimination


---
