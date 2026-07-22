# MIMIC-IV 核心表结构

**数据库**: mimiciv_31  |  **Schema数**: 5  |  **表总数**: 106


## mimiciv_derived (65 张表)


### mimiciv_derived.acei — 约 135,153 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | acei | character varying | YES |
| 4 | starttime | timestamp without time zone | YES |
| 5 | stoptime | timestamp without time zone | YES |

### mimiciv_derived.age — 约 546,028 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | admittime | timestamp without time zone | YES |
| 4 | anchor_age | smallint | YES |
| 5 | anchor_year | smallint | YES |
| 6 | age | numeric | YES |

### mimiciv_derived.antibiotic — 约 949,901 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | antibiotic | character varying | YES |
| 5 | route | character varying | YES |
| 6 | starttime | timestamp without time zone | YES |
| 7 | stoptime | timestamp without time zone | YES |

### mimiciv_derived.apsiii — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | apsiii | integer | YES |
| 5 | apsiii_prob | double precision | YES |
| 6 | hr_score | integer | YES |
| 7 | mbp_score | integer | YES |
| 8 | temp_score | integer | YES |
| 9 | resp_rate_score | integer | YES |
| 10 | pao2_aado2_score | integer | YES |
| 11 | hematocrit_score | integer | YES |
| 12 | wbc_score | integer | YES |
| 13 | creatinine_score | integer | YES |
| 14 | uo_score | integer | YES |
| 15 | bun_score | integer | YES |
| 16 | sodium_score | integer | YES |
| 17 | albumin_score | integer | YES |
| 18 | bilirubin_score | integer | YES |
| 19 | glucose_score | integer | YES |
| 20 | acidbase_score | integer | YES |
| 21 | gcs_score | integer | YES |

### mimiciv_derived.bg — 约 697,418 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | specimen | text | YES |
| 5 | so2 | double precision | YES |
| 6 | po2 | double precision | YES |
| 7 | pco2 | double precision | YES |
| 8 | fio2_chartevents | double precision | YES |
| 9 | fio2 | double precision | YES |
| 10 | aado2 | double precision | YES |
| 11 | aado2_calc | double precision | YES |
| 12 | pao2fio2ratio | double precision | YES |
| 13 | ph | double precision | YES |
| 14 | baseexcess | double precision | YES |
| 15 | bicarbonate | double precision | YES |
| 16 | totalco2 | double precision | YES |
| 17 | hematocrit | double precision | YES |
| 18 | hemoglobin | double precision | YES |
| 19 | carboxyhemoglobin | double precision | YES |
| 20 | methemoglobin | double precision | YES |
| 21 | chloride | double precision | YES |
| 22 | calcium | double precision | YES |
| 23 | temperature | double precision | YES |
| 24 | potassium | double precision | YES |
| 25 | sodium | double precision | YES |
| 26 | lactate | double precision | YES |
| 27 | glucose | double precision | YES |

### mimiciv_derived.blood_differential — 约 4,155,124 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | specimen_id | integer | YES |
| 5 | wbc | double precision | YES |
| 6 | basophils_abs | numeric | YES |
| 7 | eosinophils_abs | numeric | YES |
| 8 | lymphocytes_abs | numeric | YES |
| 9 | monocytes_abs | numeric | YES |
| 10 | neutrophils_abs | numeric | YES |
| 11 | basophils | double precision | YES |
| 12 | eosinophils | double precision | YES |
| 13 | lymphocytes | double precision | YES |
| 14 | monocytes | double precision | YES |
| 15 | neutrophils | double precision | YES |
| 16 | atypical_lymphocytes | double precision | YES |
| 17 | bands | double precision | YES |
| 18 | immature_granulocytes | double precision | YES |
| 19 | metamyelocytes | double precision | YES |
| 20 | nrbc | double precision | YES |

### mimiciv_derived.cardiac_marker — 约 380,131 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | specimen_id | integer | YES |
| 5 | troponin_t | double precision | YES |
| 6 | ck_mb | double precision | YES |
| 7 | ntprobnp | double precision | YES |

### mimiciv_derived.charlson — 约 546,028 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | age_score | integer | YES |
| 4 | myocardial_infarct | integer | YES |
| 5 | congestive_heart_failure | integer | YES |
| 6 | peripheral_vascular_disease | integer | YES |
| 7 | cerebrovascular_disease | integer | YES |
| 8 | dementia | integer | YES |
| 9 | chronic_pulmonary_disease | integer | YES |
| 10 | rheumatic_disease | integer | YES |
| 11 | peptic_ulcer_disease | integer | YES |
| 12 | mild_liver_disease | integer | YES |
| 13 | diabetes_without_cc | integer | YES |
| 14 | diabetes_with_cc | integer | YES |
| 15 | paraplegia | integer | YES |
| 16 | renal_disease | integer | YES |
| 17 | malignant_cancer | integer | YES |
| 18 | severe_liver_disease | integer | YES |
| 19 | metastatic_solid_tumor | integer | YES |
| 20 | aids | integer | YES |
| 21 | charlson_comorbidity_index | integer | YES |

### mimiciv_derived.chemistry — 约 4,976,888 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | specimen_id | integer | YES |
| 5 | albumin | double precision | YES |
| 6 | globulin | double precision | YES |
| 7 | total_protein | double precision | YES |
| 8 | aniongap | double precision | YES |
| 9 | bicarbonate | double precision | YES |
| 10 | bun | double precision | YES |
| 11 | calcium | double precision | YES |
| 12 | chloride | double precision | YES |
| 13 | creatinine | double precision | YES |
| 14 | glucose | double precision | YES |
| 15 | sodium | double precision | YES |
| 16 | potassium | double precision | YES |

### mimiciv_derived.coagulation — 约 1,991,167 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | specimen_id | integer | YES |
| 5 | d_dimer | double precision | YES |
| 6 | fibrinogen | double precision | YES |
| 7 | thrombin | double precision | YES |
| 8 | inr | double precision | YES |
| 9 | pt | double precision | YES |
| 10 | ptt | double precision | YES |

### mimiciv_derived.complete_blood_count — 约 4,378,276 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | specimen_id | integer | YES |
| 5 | hematocrit | double precision | YES |
| 6 | hemoglobin | double precision | YES |
| 7 | mch | double precision | YES |
| 8 | mchc | double precision | YES |
| 9 | mcv | double precision | YES |
| 10 | platelet | double precision | YES |
| 11 | rbc | double precision | YES |
| 12 | rdw | double precision | YES |
| 13 | rdwsd | double precision | YES |
| 14 | wbc | double precision | YES |

### mimiciv_derived.creatinine_baseline — 约 546,028 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | hadm_id | integer | YES |
| 2 | gender | character | YES |
| 3 | age | numeric | YES |
| 4 | scr_min | double precision | YES |
| 5 | ckd | integer | YES |
| 6 | mdrd_est | double precision | YES |
| 7 | scr_baseline | double precision | YES |

### mimiciv_derived.crrt — 约 475,214 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | charttime | timestamp without time zone | YES |
| 3 | crrt_mode | text | YES |
| 4 | access_pressure | double precision | YES |
| 5 | blood_flow | double precision | YES |
| 6 | citrate | double precision | YES |
| 7 | current_goal | double precision | YES |
| 8 | dialysate_fluid | text | YES |
| 9 | dialysate_rate | double precision | YES |
| 10 | effluent_pressure | double precision | YES |
| 11 | filter_pressure | double precision | YES |
| 12 | heparin_concentration | text | YES |
| 13 | heparin_dose | double precision | YES |
| 14 | hourly_patient_fluid_removal | double precision | YES |
| 15 | prefilter_replacement_rate | double precision | YES |
| 16 | postfilter_replacement_rate | double precision | YES |
| 17 | replacement_fluid | text | YES |
| 18 | replacement_rate | double precision | YES |
| 19 | return_pressure | double precision | YES |
| 20 | ultrafiltrate_output | double precision | YES |
| 21 | system_active | integer | YES |
| 22 | clots | integer | YES |
| 23 | clots_increasing | integer | YES |
| 24 | clotted | integer | YES |

### mimiciv_derived.dobutamine — 约 10,264 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | linkorderid | integer | YES |
| 3 | vaso_rate | double precision | YES |
| 4 | vaso_amount | double precision | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | endtime | timestamp without time zone | YES |

### mimiciv_derived.dopamine — 约 18,085 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | linkorderid | integer | YES |
| 3 | vaso_rate | double precision | YES |
| 4 | vaso_amount | double precision | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | endtime | timestamp without time zone | YES |

### mimiciv_derived.enzyme — 约 2,187,060 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | specimen_id | integer | YES |
| 5 | alt | double precision | YES |
| 6 | alp | double precision | YES |
| 7 | ast | double precision | YES |
| 8 | amylase | double precision | YES |
| 9 | bilirubin_total | double precision | YES |
| 10 | bilirubin_direct | double precision | YES |
| 11 | bilirubin_indirect | double precision | YES |
| 12 | ck_cpk | double precision | YES |
| 13 | ck_mb | double precision | YES |
| 14 | ggt | double precision | YES |
| 15 | ld_ldh | double precision | YES |

### mimiciv_derived.epinephrine — 约 31,495 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | linkorderid | integer | YES |
| 3 | vaso_rate | double precision | YES |
| 4 | vaso_amount | double precision | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | endtime | timestamp without time zone | YES |

### mimiciv_derived.first_day_bg — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | lactate_min | double precision | YES |
| 4 | lactate_max | double precision | YES |
| 5 | ph_min | double precision | YES |
| 6 | ph_max | double precision | YES |
| 7 | so2_min | double precision | YES |
| 8 | so2_max | double precision | YES |
| 9 | po2_min | double precision | YES |
| 10 | po2_max | double precision | YES |
| 11 | pco2_min | double precision | YES |
| 12 | pco2_max | double precision | YES |
| 13 | aado2_min | double precision | YES |
| 14 | aado2_max | double precision | YES |
| 15 | aado2_calc_min | double precision | YES |
| 16 | aado2_calc_max | double precision | YES |
| 17 | pao2fio2ratio_min | double precision | YES |
| 18 | pao2fio2ratio_max | double precision | YES |
| 19 | baseexcess_min | double precision | YES |
| 20 | baseexcess_max | double precision | YES |
| 21 | bicarbonate_min | double precision | YES |
| 22 | bicarbonate_max | double precision | YES |
| 23 | totalco2_min | double precision | YES |
| 24 | totalco2_max | double precision | YES |
| 25 | hematocrit_min | double precision | YES |
| 26 | hematocrit_max | double precision | YES |
| 27 | hemoglobin_min | double precision | YES |
| 28 | hemoglobin_max | double precision | YES |
| 29 | carboxyhemoglobin_min | double precision | YES |
| 30 | carboxyhemoglobin_max | double precision | YES |
| 31 | methemoglobin_min | double precision | YES |
| 32 | methemoglobin_max | double precision | YES |
| 33 | temperature_min | double precision | YES |
| 34 | temperature_max | double precision | YES |
| 35 | chloride_min | double precision | YES |
| 36 | chloride_max | double precision | YES |
| 37 | calcium_min | double precision | YES |
| 38 | calcium_max | double precision | YES |
| 39 | glucose_min | double precision | YES |
| 40 | glucose_max | double precision | YES |
| 41 | potassium_min | double precision | YES |
| 42 | potassium_max | double precision | YES |
| 43 | sodium_min | double precision | YES |
| 44 | sodium_max | double precision | YES |

### mimiciv_derived.first_day_bg_art — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | lactate_min | double precision | YES |
| 4 | lactate_max | double precision | YES |
| 5 | ph_min | double precision | YES |
| 6 | ph_max | double precision | YES |
| 7 | so2_min | double precision | YES |
| 8 | so2_max | double precision | YES |
| 9 | po2_min | double precision | YES |
| 10 | po2_max | double precision | YES |
| 11 | pco2_min | double precision | YES |
| 12 | pco2_max | double precision | YES |
| 13 | aado2_min | double precision | YES |
| 14 | aado2_max | double precision | YES |
| 15 | aado2_calc_min | double precision | YES |
| 16 | aado2_calc_max | double precision | YES |
| 17 | pao2fio2ratio_min | double precision | YES |
| 18 | pao2fio2ratio_max | double precision | YES |
| 19 | baseexcess_min | double precision | YES |
| 20 | baseexcess_max | double precision | YES |
| 21 | bicarbonate_min | double precision | YES |
| 22 | bicarbonate_max | double precision | YES |
| 23 | totalco2_min | double precision | YES |
| 24 | totalco2_max | double precision | YES |
| 25 | hematocrit_min | double precision | YES |
| 26 | hematocrit_max | double precision | YES |
| 27 | hemoglobin_min | double precision | YES |
| 28 | hemoglobin_max | double precision | YES |
| 29 | carboxyhemoglobin_min | double precision | YES |
| 30 | carboxyhemoglobin_max | double precision | YES |
| 31 | methemoglobin_min | double precision | YES |
| 32 | methemoglobin_max | double precision | YES |
| 33 | temperature_min | double precision | YES |
| 34 | temperature_max | double precision | YES |
| 35 | chloride_min | double precision | YES |
| 36 | chloride_max | double precision | YES |
| 37 | calcium_min | double precision | YES |
| 38 | calcium_max | double precision | YES |
| 39 | glucose_min | double precision | YES |
| 40 | glucose_max | double precision | YES |
| 41 | potassium_min | double precision | YES |
| 42 | potassium_max | double precision | YES |
| 43 | sodium_min | double precision | YES |
| 44 | sodium_max | double precision | YES |

### mimiciv_derived.first_day_gcs — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | gcs_min | double precision | YES |
| 4 | gcs_motor | double precision | YES |
| 5 | gcs_verbal | double precision | YES |
| 6 | gcs_eyes | double precision | YES |
| 7 | gcs_unable | integer | YES |

### mimiciv_derived.first_day_height — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | height | numeric | YES |

### mimiciv_derived.first_day_lab — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | hematocrit_min | double precision | YES |
| 4 | hematocrit_max | double precision | YES |
| 5 | hemoglobin_min | double precision | YES |
| 6 | hemoglobin_max | double precision | YES |
| 7 | platelets_min | double precision | YES |
| 8 | platelets_max | double precision | YES |
| 9 | wbc_min | double precision | YES |
| 10 | wbc_max | double precision | YES |
| 11 | albumin_min | double precision | YES |
| 12 | albumin_max | double precision | YES |
| 13 | globulin_min | double precision | YES |
| 14 | globulin_max | double precision | YES |
| 15 | total_protein_min | double precision | YES |
| 16 | total_protein_max | double precision | YES |
| 17 | aniongap_min | double precision | YES |
| 18 | aniongap_max | double precision | YES |
| 19 | bicarbonate_min | double precision | YES |
| 20 | bicarbonate_max | double precision | YES |
| 21 | bun_min | double precision | YES |
| 22 | bun_max | double precision | YES |
| 23 | calcium_min | double precision | YES |
| 24 | calcium_max | double precision | YES |
| 25 | chloride_min | double precision | YES |
| 26 | chloride_max | double precision | YES |
| 27 | creatinine_min | double precision | YES |
| 28 | creatinine_max | double precision | YES |
| 29 | glucose_min | double precision | YES |
| 30 | glucose_max | double precision | YES |
| 31 | sodium_min | double precision | YES |
| 32 | sodium_max | double precision | YES |
| 33 | potassium_min | double precision | YES |
| 34 | potassium_max | double precision | YES |
| 35 | abs_basophils_min | numeric | YES |
| 36 | abs_basophils_max | numeric | YES |
| 37 | abs_eosinophils_min | numeric | YES |
| 38 | abs_eosinophils_max | numeric | YES |
| 39 | abs_lymphocytes_min | numeric | YES |
| 40 | abs_lymphocytes_max | numeric | YES |
| 41 | abs_monocytes_min | numeric | YES |
| 42 | abs_monocytes_max | numeric | YES |
| 43 | abs_neutrophils_min | numeric | YES |
| 44 | abs_neutrophils_max | numeric | YES |
| 45 | atyps_min | double precision | YES |
| 46 | atyps_max | double precision | YES |
| 47 | bands_min | double precision | YES |
| 48 | bands_max | double precision | YES |
| 49 | imm_granulocytes_min | double precision | YES |
| 50 | imm_granulocytes_max | double precision | YES |
| 51 | metas_min | double precision | YES |
| 52 | metas_max | double precision | YES |
| 53 | nrbc_min | double precision | YES |
| 54 | nrbc_max | double precision | YES |
| 55 | d_dimer_min | double precision | YES |
| 56 | d_dimer_max | double precision | YES |
| 57 | fibrinogen_min | double precision | YES |
| 58 | fibrinogen_max | double precision | YES |
| 59 | thrombin_min | double precision | YES |
| 60 | thrombin_max | double precision | YES |
| 61 | inr_min | double precision | YES |
| 62 | inr_max | double precision | YES |
| 63 | pt_min | double precision | YES |
| 64 | pt_max | double precision | YES |
| 65 | ptt_min | double precision | YES |
| 66 | ptt_max | double precision | YES |
| 67 | alt_min | double precision | YES |
| 68 | alt_max | double precision | YES |
| 69 | alp_min | double precision | YES |
| 70 | alp_max | double precision | YES |
| 71 | ast_min | double precision | YES |
| 72 | ast_max | double precision | YES |
| 73 | amylase_min | double precision | YES |
| 74 | amylase_max | double precision | YES |
| 75 | bilirubin_total_min | double precision | YES |
| 76 | bilirubin_total_max | double precision | YES |
| 77 | bilirubin_direct_min | double precision | YES |
| 78 | bilirubin_direct_max | double precision | YES |
| 79 | bilirubin_indirect_min | double precision | YES |
| 80 | bilirubin_indirect_max | double precision | YES |
| 81 | ck_cpk_min | double precision | YES |
| 82 | ck_cpk_max | double precision | YES |
| 83 | ck_mb_min | double precision | YES |
| 84 | ck_mb_max | double precision | YES |
| 85 | ggt_min | double precision | YES |
| 86 | ggt_max | double precision | YES |
| 87 | ld_ldh_min | double precision | YES |
| 88 | ld_ldh_max | double precision | YES |

### mimiciv_derived.first_day_rrt — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | dialysis_present | integer | YES |
| 4 | dialysis_active | integer | YES |
| 5 | dialysis_type | text | YES |

### mimiciv_derived.first_day_sofa — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | sofa | integer | YES |
| 5 | respiration | integer | YES |
| 6 | coagulation | integer | YES |
| 7 | liver | integer | YES |
| 8 | cardiovascular | integer | YES |
| 9 | cns | integer | YES |
| 10 | renal | integer | YES |

### mimiciv_derived.first_day_urine_output — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | urineoutput | double precision | YES |

### mimiciv_derived.first_day_vitalsign — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | heart_rate_min | double precision | YES |
| 4 | heart_rate_max | double precision | YES |
| 5 | heart_rate_mean | double precision | YES |
| 6 | sbp_min | double precision | YES |
| 7 | sbp_max | double precision | YES |
| 8 | sbp_mean | double precision | YES |
| 9 | dbp_min | double precision | YES |
| 10 | dbp_max | double precision | YES |
| 11 | dbp_mean | double precision | YES |
| 12 | mbp_min | double precision | YES |
| 13 | mbp_max | double precision | YES |
| 14 | mbp_mean | double precision | YES |
| 15 | resp_rate_min | double precision | YES |
| 16 | resp_rate_max | double precision | YES |
| 17 | resp_rate_mean | double precision | YES |
| 18 | temperature_min | numeric | YES |
| 19 | temperature_max | numeric | YES |
| 20 | temperature_mean | numeric | YES |
| 21 | spo2_min | double precision | YES |
| 22 | spo2_max | double precision | YES |
| 23 | spo2_mean | double precision | YES |
| 24 | glucose_min | double precision | YES |
| 25 | glucose_max | double precision | YES |
| 26 | glucose_mean | double precision | YES |

### mimiciv_derived.first_day_weight — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | weight_admit | double precision | YES |
| 4 | weight | double precision | YES |
| 5 | weight_min | double precision | YES |
| 6 | weight_max | double precision | YES |

### mimiciv_derived.gcs — 约 2,217,787 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | gcs | double precision | YES |
| 5 | gcs_motor | double precision | YES |
| 6 | gcs_verbal | double precision | YES |
| 7 | gcs_eyes | double precision | YES |
| 8 | gcs_unable | integer | YES |

### mimiciv_derived.height — 约 43,342 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | height | numeric | YES |

### mimiciv_derived.icp — 约 243,283 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | icp | double precision | YES |

### mimiciv_derived.icustay_detail — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | gender | character | YES |
| 5 | dod | date | YES |
| 6 | admittime | timestamp without time zone | YES |
| 7 | dischtime | timestamp without time zone | YES |
| 8 | los_hospital | numeric | YES |
| 9 | admission_age | numeric | YES |
| 10 | race | character varying | YES |
| 11 | hospital_expire_flag | smallint | YES |
| 12 | hospstay_seq | bigint | YES |
| 13 | first_hosp_stay | boolean | YES |
| 14 | icu_intime | timestamp without time zone | YES |
| 15 | icu_outtime | timestamp without time zone | YES |
| 16 | los_icu | numeric | YES |
| 17 | icustay_seq | bigint | YES |
| 18 | first_icu_stay | boolean | YES |

### mimiciv_derived.icustay_hourly — 约 10,486,965 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | hr | bigint | YES |
| 3 | endtime | timestamp without time zone | YES |

### mimiciv_derived.icustay_times — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | intime_hr | timestamp without time zone | YES |
| 5 | outtime_hr | timestamp without time zone | YES |

### mimiciv_derived.inflammation — 约 174,269 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | specimen_id | integer | YES |
| 5 | crp | double precision | YES |

### mimiciv_derived.invasive_line — 约 108,165 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | line_type | character varying | YES |
| 3 | line_site | character varying | YES |
| 4 | starttime | timestamp without time zone | YES |
| 5 | endtime | timestamp without time zone | YES |

### mimiciv_derived.kdigo_creatinine — 约 811,585 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | hadm_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | creat | double precision | YES |
| 5 | creat_low_past_48hr | double precision | YES |
| 6 | creat_low_past_7day | double precision | YES |

### mimiciv_derived.kdigo_stages — 约 5,101,336 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | charttime | timestamp without time zone | YES |
| 5 | creat_low_past_7day | double precision | YES |
| 6 | creat_low_past_48hr | double precision | YES |
| 7 | creat | double precision | YES |
| 8 | aki_stage_creat | integer | YES |
| 9 | uo_rt_6hr | numeric | YES |
| 10 | uo_rt_12hr | numeric | YES |
| 11 | uo_rt_24hr | numeric | YES |
| 12 | aki_stage_uo | integer | YES |
| 13 | aki_stage_crrt | integer | YES |
| 14 | aki_stage | integer | YES |
| 15 | aki_stage_smoothed | integer | YES |

### mimiciv_derived.kdigo_uo — 约 4,127,646 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | charttime | timestamp without time zone | YES |
| 3 | weight | double precision | YES |
| 4 | urineoutput_6hr | double precision | YES |
| 5 | urineoutput_12hr | double precision | YES |
| 6 | urineoutput_24hr | double precision | YES |
| 7 | uo_rt_6hr | numeric | YES |
| 8 | uo_rt_12hr | numeric | YES |
| 9 | uo_rt_24hr | numeric | YES |
| 10 | uo_tm_6hr | double precision | YES |
| 11 | uo_tm_12hr | double precision | YES |
| 12 | uo_tm_24hr | double precision | YES |

### mimiciv_derived.lods — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | lods | integer | YES |
| 5 | neurologic | integer | YES |
| 6 | cardiovascular | integer | YES |
| 7 | renal | integer | YES |
| 8 | pulmonary | integer | YES |
| 9 | hematologic | integer | YES |
| 10 | hepatic | integer | YES |

### mimiciv_derived.meld — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | meld_initial | numeric | YES |
| 5 | meld | double precision | YES |
| 6 | rrt | integer | YES |
| 7 | creatinine_max | double precision | YES |
| 8 | bilirubin_total_max | double precision | YES |
| 9 | inr_max | double precision | YES |
| 10 | sodium_min | double precision | YES |

### mimiciv_derived.milrinone — 约 10,668 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | linkorderid | integer | YES |
| 3 | vaso_rate | double precision | YES |
| 4 | vaso_amount | double precision | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | endtime | timestamp without time zone | YES |

### mimiciv_derived.neuroblock — 约 19,430 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | orderid | integer | YES |
| 3 | drug_rate | double precision | YES |
| 4 | drug_amount | double precision | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | endtime | timestamp without time zone | YES |

### mimiciv_derived.norepinephrine — 约 459,800 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | linkorderid | integer | YES |
| 3 | vaso_rate | double precision | YES |
| 4 | vaso_amount | double precision | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | endtime | timestamp without time zone | YES |

### mimiciv_derived.norepinephrine_equivalent_dose — 约 783,613 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | starttime | timestamp without time zone | YES |
| 3 | endtime | timestamp without time zone | YES |
| 4 | norepinephrine_equivalent_dose | numeric | YES |

### mimiciv_derived.nsaid — 约 293,253 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | nsaid | character varying | YES |
| 4 | starttime | timestamp without time zone | YES |
| 5 | stoptime | timestamp without time zone | YES |

### mimiciv_derived.oasis — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | oasis | integer | YES |
| 5 | oasis_prob | double precision | YES |
| 6 | age | numeric | YES |
| 7 | age_score | integer | YES |
| 8 | preiculos | numeric | YES |
| 9 | preiculos_score | integer | YES |
| 10 | gcs | double precision | YES |
| 11 | gcs_score | integer | YES |
| 12 | heartrate | double precision | YES |
| 13 | heart_rate_score | integer | YES |
| 14 | meanbp | double precision | YES |
| 15 | mbp_score | integer | YES |
| 16 | resprate | double precision | YES |
| 17 | resp_rate_score | integer | YES |
| 18 | temp | double precision | YES |
| 19 | temp_score | integer | YES |
| 20 | urineoutput | double precision | YES |
| 21 | urineoutput_score | integer | YES |
| 22 | mechvent | integer | YES |
| 23 | mechvent_score | integer | YES |
| 24 | electivesurgery | integer | YES |
| 25 | electivesurgery_score | integer | YES |

### mimiciv_derived.oxygen_delivery — 约 794,232 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | o2_flow | double precision | YES |
| 5 | o2_flow_additional | double precision | YES |
| 6 | o2_delivery_device_1 | text | YES |
| 7 | o2_delivery_device_2 | text | YES |
| 8 | o2_delivery_device_3 | text | YES |
| 9 | o2_delivery_device_4 | text | YES |

### mimiciv_derived.phenylephrine — 约 209,376 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | linkorderid | integer | YES |
| 3 | vaso_rate | double precision | YES |
| 4 | vaso_amount | double precision | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | endtime | timestamp without time zone | YES |

### mimiciv_derived.rhythm — 约 7,886,194 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | charttime | timestamp without time zone | YES |
| 3 | heart_rhythm | text | YES |
| 4 | ectopy_type | text | YES |
| 5 | ectopy_frequency | text | YES |
| 6 | ectopy_type_secondary | text | YES |
| 7 | ectopy_frequency_secondary | text | YES |

### mimiciv_derived.rrt — 约 4,098,630 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | charttime | timestamp without time zone | YES |
| 3 | dialysis_present | integer | YES |
| 4 | dialysis_active | integer | YES |
| 5 | dialysis_type | text | YES |

### mimiciv_derived.sapsii — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | starttime | timestamp without time zone | YES |
| 5 | endtime | timestamp without time zone | YES |
| 6 | sapsii | integer | YES |
| 7 | sapsii_prob | double precision | YES |
| 8 | age_score | integer | YES |
| 9 | hr_score | integer | YES |
| 10 | sysbp_score | integer | YES |
| 11 | temp_score | integer | YES |
| 12 | pao2fio2_score | integer | YES |
| 13 | uo_score | integer | YES |
| 14 | bun_score | integer | YES |
| 15 | wbc_score | integer | YES |
| 16 | potassium_score | integer | YES |
| 17 | sodium_score | integer | YES |
| 18 | bicarbonate_score | integer | YES |
| 19 | bilirubin_score | integer | YES |
| 20 | gcs_score | integer | YES |
| 21 | comorbidity_score | integer | YES |
| 22 | admissiontype_score | integer | YES |

### mimiciv_derived.sepsis3 — 约 41,295 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | antibiotic_time | timestamp without time zone | YES |
| 4 | culture_time | timestamp without time zone | YES |
| 5 | suspected_infection_time | timestamp without time zone | YES |
| 6 | sofa_time | timestamp without time zone | YES |
| 7 | sofa_score | integer | YES |
| 8 | respiration | integer | YES |
| 9 | coagulation | integer | YES |
| 10 | liver | integer | YES |
| 11 | cardiovascular | integer | YES |
| 12 | cns | integer | YES |
| 13 | renal | integer | YES |
| 14 | sepsis3 | boolean | YES |

### mimiciv_derived.sepsis_vaso_analysis — 约 8,075 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | exposure_group | integer | YES |
| 5 | vaso_group | text | YES |
| 6 | vaso_starttime | timestamp without time zone | YES |
| 7 | icu_intime | timestamp without time zone | YES |
| 8 | icu_outtime | timestamp without time zone | YES |
| 9 | admittime | timestamp without time zone | YES |
| 10 | dischtime | timestamp without time zone | YES |
| 11 | deathtime | timestamp without time zone | YES |
| 12 | age | numeric | YES |
| 13 | gender | character | YES |
| 14 | race | character varying | YES |
| 15 | hours_to_vaso | numeric | YES |
| 16 | icu_los_hours | numeric | YES |
| 17 | death_28d | integer | YES |
| 18 | death_90d | integer | YES |
| 19 | hospital_mortality | integer | YES |
| 20 | survival_time_28d | numeric | YES |
| 21 | survival_time_90d | numeric | YES |
| 22 | sofa_baseline | integer | YES |
| 23 | sofa_resp | integer | YES |
| 24 | sofa_coag | integer | YES |
| 25 | sofa_liver | integer | YES |
| 26 | sofa_cv | integer | YES |
| 27 | sofa_cns | integer | YES |
| 28 | sofa_renal | integer | YES |
| 29 | lactate_max | double precision | YES |
| 30 | lactate_min | double precision | YES |
| 31 | lactate_mean | double precision | YES |
| 32 | map_min | double precision | YES |
| 33 | map_mean | double precision | YES |
| 34 | hr_min | double precision | YES |
| 35 | hr_mean | double precision | YES |
| 36 | hr_max | double precision | YES |
| 37 | rr_mean | double precision | YES |
| 38 | temp_mean | numeric | YES |
| 39 | spo2_mean | double precision | YES |
| 40 | gcs_min | double precision | YES |
| 41 | urine_output_24h | double precision | YES |
| 42 | mech_vent | integer | YES |
| 43 | rrt_flag | integer | YES |
| 44 | weight_kg | double precision | YES |
| 45 | creatinine_max | double precision | YES |
| 46 | wbc_max | double precision | YES |
| 47 | platelets_min | double precision | YES |
| 48 | bun_max | double precision | YES |
| 49 | bilirubin_max | double precision | YES |
| 50 | inr_max | double precision | YES |
| 51 | pt_max | double precision | YES |
| 52 | ptt_max | double precision | YES |
| 53 | myocardial_infarct | integer | YES |
| 54 | congestive_heart_failure | integer | YES |
| 55 | peripheral_vascular_disease | integer | YES |
| 56 | cerebrovascular_disease | integer | YES |
| 57 | dementia | integer | YES |
| 58 | chronic_pulmonary_disease | integer | YES |
| 59 | rheumatic_disease | integer | YES |
| 60 | peptic_ulcer_disease | integer | YES |
| 61 | mild_liver_disease | integer | YES |
| 62 | diabetes_without_cc | integer | YES |
| 63 | diabetes_with_cc | integer | YES |
| 64 | hemiplegia_or_paraplegia | integer | YES |
| 65 | renal_disease | integer | YES |
| 66 | malignancy | integer | YES |
| 67 | severe_liver_disease | integer | YES |
| 68 | metastatic_solid_tumor | integer | YES |
| 69 | aids | integer | YES |
| 70 | charlson_comorbidity_index | integer | YES |

### mimiciv_derived.sepsis_vaso_cohort — 约 8,075 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | icu_intime | timestamp without time zone | YES |
| 5 | icu_outtime | timestamp without time zone | YES |
| 6 | age_at_icu | numeric | YES |
| 7 | gender | character | YES |
| 8 | admittime | timestamp without time zone | YES |
| 9 | dischtime | timestamp without time zone | YES |
| 10 | deathtime | timestamp without time zone | YES |
| 11 | race | character varying | YES |
| 12 | insurance | character varying | YES |
| 13 | marital_status | character varying | YES |
| 14 | icu_los_hours | numeric | YES |
| 15 | vaso_starttime | timestamp without time zone | YES |
| 16 | vaso_group | text | YES |
| 17 | vaso_itemid | integer | YES |
| 18 | vaso_label | character varying | YES |
| 19 | hours_to_vaso | numeric | YES |
| 20 | exposure_group | integer | YES |
| 21 | death_28d | integer | YES |
| 22 | death_90d | integer | YES |
| 23 | hospital_mortality | integer | YES |
| 24 | survival_time_28d | numeric | YES |
| 25 | survival_time_90d | numeric | YES |

### mimiciv_derived.sirs — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | YES |
| 4 | sirs | integer | YES |
| 5 | temp_score | integer | YES |
| 6 | heart_rate_score | integer | YES |
| 7 | resp_score | integer | YES |
| 8 | wbc_score | integer | YES |

### mimiciv_derived.sofa — 约 8,218,391 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | hr | bigint | YES |
| 3 | starttime | timestamp without time zone | YES |
| 4 | endtime | timestamp without time zone | YES |
| 5 | pao2fio2ratio_novent | double precision | YES |
| 6 | pao2fio2ratio_vent | double precision | YES |
| 7 | rate_epinephrine | double precision | YES |
| 8 | rate_norepinephrine | double precision | YES |
| 9 | rate_dopamine | double precision | YES |
| 10 | rate_dobutamine | double precision | YES |
| 11 | meanbp_min | double precision | YES |
| 12 | gcs_min | double precision | YES |
| 13 | uo_24hr | double precision | YES |
| 14 | bilirubin_max | double precision | YES |
| 15 | creatinine_max | double precision | YES |
| 16 | platelet_min | double precision | YES |
| 17 | respiration | integer | YES |
| 18 | coagulation | integer | YES |
| 19 | liver | integer | YES |
| 20 | cardiovascular | integer | YES |
| 21 | cns | integer | YES |
| 22 | renal | integer | YES |
| 23 | respiration_24hours | integer | YES |
| 24 | coagulation_24hours | integer | YES |
| 25 | liver_24hours | integer | YES |
| 26 | cardiovascular_24hours | integer | YES |
| 27 | cns_24hours | integer | YES |
| 28 | renal_24hours | integer | YES |
| 29 | sofa_24hours | integer | YES |

### mimiciv_derived.suspicion_of_infection — 约 949,901 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | hadm_id | integer | YES |
| 4 | ab_id | bigint | YES |
| 5 | antibiotic | character varying | YES |
| 6 | antibiotic_time | timestamp without time zone | YES |
| 7 | suspected_infection | integer | YES |
| 8 | suspected_infection_time | timestamp without time zone | YES |
| 9 | culture_time | timestamp without time zone | YES |
| 10 | specimen | text | YES |
| 11 | positive_culture | integer | YES |

### mimiciv_derived.urine_output — 约 4,127,634 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | charttime | timestamp without time zone | YES |
| 3 | urineoutput | double precision | YES |

### mimiciv_derived.urine_output_rate — 约 4,127,424 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | charttime | timestamp without time zone | YES |
| 3 | weight | double precision | YES |
| 4 | uo | double precision | YES |
| 5 | urineoutput_6hr | double precision | YES |
| 6 | urineoutput_12hr | double precision | YES |
| 7 | urineoutput_24hr | double precision | YES |
| 8 | uo_mlkghr_6hr | numeric | YES |
| 9 | uo_mlkghr_12hr | numeric | YES |
| 10 | uo_mlkghr_24hr | numeric | YES |
| 11 | uo_tm_6hr | numeric | YES |
| 12 | uo_tm_12hr | numeric | YES |
| 13 | uo_tm_24hr | numeric | YES |

### mimiciv_derived.vasoactive_agent — 约 839,543 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | starttime | timestamp without time zone | YES |
| 3 | endtime | timestamp without time zone | YES |
| 4 | dopamine | double precision | YES |
| 5 | epinephrine | double precision | YES |
| 6 | norepinephrine | double precision | YES |
| 7 | phenylephrine | double precision | YES |
| 8 | vasopressin | double precision | YES |
| 9 | dobutamine | double precision | YES |
| 10 | milrinone | double precision | YES |

### mimiciv_derived.vasopressin — 约 37,163 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | linkorderid | integer | YES |
| 3 | vaso_rate | double precision | YES |
| 4 | vaso_amount | double precision | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | endtime | timestamp without time zone | YES |

### mimiciv_derived.ventilation — 约 144,812 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | starttime | timestamp without time zone | YES |
| 3 | endtime | timestamp without time zone | YES |
| 4 | ventilation_status | text | YES |

### mimiciv_derived.ventilator_setting — 约 1,377,514 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | respiratory_rate_set | double precision | YES |
| 5 | respiratory_rate_total | double precision | YES |
| 6 | respiratory_rate_spontaneous | double precision | YES |
| 7 | minute_volume | double precision | YES |
| 8 | tidal_volume_set | double precision | YES |
| 9 | tidal_volume_observed | double precision | YES |
| 10 | tidal_volume_spontaneous | double precision | YES |
| 11 | plateau_pressure | double precision | YES |
| 12 | peep | double precision | YES |
| 13 | fio2 | double precision | YES |
| 14 | flow_rate | double precision | YES |
| 15 | ventilator_mode | text | YES |
| 16 | ventilator_mode_hamilton | text | YES |
| 17 | ventilator_type | text | YES |

### mimiciv_derived.vitalsign — 约 13,509,794 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | YES |
| 2 | stay_id | integer | YES |
| 3 | charttime | timestamp without time zone | YES |
| 4 | heart_rate | double precision | YES |
| 5 | sbp | double precision | YES |
| 6 | dbp | double precision | YES |
| 7 | mbp | double precision | YES |
| 8 | sbp_ni | double precision | YES |
| 9 | dbp_ni | double precision | YES |
| 10 | mbp_ni | double precision | YES |
| 11 | resp_rate | double precision | YES |
| 12 | temperature | numeric | YES |
| 13 | temperature_site | text | YES |
| 14 | spo2 | double precision | YES |
| 15 | glucose | double precision | YES |

### mimiciv_derived.weight_durations — 约 401,850 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | stay_id | integer | YES |
| 2 | starttime | timestamp without time zone | YES |
| 3 | endtime | timestamp without time zone | YES |
| 4 | weight | double precision | YES |
| 5 | weight_type | text | YES |

## mimiciv_ed (6 张表)


### mimiciv_ed.diagnosis — 约 899,050 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | stay_id | integer | NO |
| 3 | seq_num | integer | NO |
| 4 | icd_code | character varying | NO |
| 5 | icd_version | smallint | NO |
| 6 | icd_title | text | NO |

**外键关系**:
- stay_id → mimiciv_ed.edstays.stay_id

### mimiciv_ed.edstays — 约 425,087 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | YES |
| 3 | stay_id | integer | NO |
| 4 | intime | timestamp without time zone | NO |
| 5 | outtime | timestamp without time zone | NO |
| 6 | gender | character varying | NO |
| 7 | race | character varying | YES |
| 8 | arrival_transport | character varying | NO |
| 9 | disposition | character varying | YES |

### mimiciv_ed.medrecon — 约 2,987,562 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | stay_id | integer | NO |
| 3 | charttime | timestamp without time zone | YES |
| 4 | name | character varying | YES |
| 5 | gsn | character varying | YES |
| 6 | ndc | character varying | YES |
| 7 | etc_rn | smallint | YES |
| 8 | etccode | character varying | YES |
| 9 | etcdescription | character varying | YES |

**外键关系**:
- stay_id → mimiciv_ed.edstays.stay_id

### mimiciv_ed.pyxis — 约 1,586,053 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | stay_id | integer | NO |
| 3 | charttime | timestamp without time zone | YES |
| 4 | med_rn | smallint | NO |
| 5 | name | character varying | YES |
| 6 | gsn_rn | smallint | NO |
| 7 | gsn | character varying | YES |

**外键关系**:
- stay_id → mimiciv_ed.edstays.stay_id

### mimiciv_ed.triage — 约 425,087 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | stay_id | integer | NO |
| 3 | temperature | numeric | YES |
| 4 | heartrate | numeric | YES |
| 5 | resprate | numeric | YES |
| 6 | o2sat | numeric | YES |
| 7 | sbp | numeric | YES |
| 8 | dbp | numeric | YES |
| 9 | pain | text | YES |
| 10 | acuity | numeric | YES |
| 11 | chiefcomplaint | character varying | YES |

**外键关系**:
- stay_id → mimiciv_ed.edstays.stay_id

### mimiciv_ed.vitalsign — 约 1,564,610 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | stay_id | integer | NO |
| 3 | charttime | timestamp without time zone | NO |
| 4 | temperature | numeric | YES |
| 5 | heartrate | numeric | YES |
| 6 | resprate | numeric | YES |
| 7 | o2sat | numeric | YES |
| 8 | sbp | integer | YES |
| 9 | dbp | integer | YES |
| 10 | rhythm | text | YES |
| 11 | pain | text | YES |

**外键关系**:
- stay_id → mimiciv_ed.edstays.stay_id

## mimiciv_hosp (22 张表)


### mimiciv_hosp.admissions — 约 546,028 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | admittime | timestamp without time zone | NO |
| 4 | dischtime | timestamp without time zone | YES |
| 5 | deathtime | timestamp without time zone | YES |
| 6 | admission_type | character varying | NO |
| 7 | admit_provider_id | character varying | YES |
| 8 | admission_location | character varying | YES |
| 9 | discharge_location | character varying | YES |
| 10 | insurance | character varying | YES |
| 11 | language | character varying | YES |
| 12 | marital_status | character varying | YES |
| 13 | race | character varying | YES |
| 14 | edregtime | timestamp without time zone | YES |
| 15 | edouttime | timestamp without time zone | YES |
| 16 | hospital_expire_flag | smallint | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id

### mimiciv_hosp.d_hcpcs — 约 89,208 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | code | character | NO |
| 2 | category | smallint | YES |
| 3 | long_description | text | YES |
| 4 | short_description | character varying | YES |

### mimiciv_hosp.d_icd_diagnoses — 约 112,107 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | icd_code | character | NO |
| 2 | icd_version | smallint | NO |
| 3 | long_title | character varying | YES |

### mimiciv_hosp.d_icd_procedures — 约 86,423 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | icd_code | character | NO |
| 2 | icd_version | smallint | NO |
| 3 | long_title | character varying | YES |

### mimiciv_hosp.d_labitems — 约 1,650 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | itemid | integer | NO |
| 2 | label | character varying | YES |
| 3 | fluid | character varying | YES |
| 4 | category | character varying | YES |

### mimiciv_hosp.diagnoses_icd — 约 6,364,129 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | seq_num | integer | NO |
| 4 | icd_code | character | NO |
| 5 | icd_version | smallint | NO |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.drgcodes — 约 761,856 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | drg_type | character varying | YES |
| 4 | drg_code | character varying | NO |
| 5 | description | character varying | YES |
| 6 | drg_severity | smallint | YES |
| 7 | drg_mortality | smallint | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.emar — 约 42,802,641 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | YES |
| 3 | emar_id | character varying | NO |
| 4 | emar_seq | integer | NO |
| 5 | poe_id | character varying | NO |
| 6 | pharmacy_id | integer | YES |
| 7 | enter_provider_id | character varying | YES |
| 8 | charttime | timestamp without time zone | NO |
| 9 | medication | text | YES |
| 10 | event_txt | character varying | YES |
| 11 | scheduletime | timestamp without time zone | YES |
| 12 | storetime | timestamp without time zone | NO |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.emar_detail — 约 87,384,338 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | emar_id | character varying | NO |
| 3 | emar_seq | integer | NO |
| 4 | parent_field_ordinal | character varying | YES |
| 5 | administration_type | character varying | YES |
| 6 | pharmacy_id | integer | YES |
| 7 | barcode_type | character varying | YES |
| 8 | reason_for_no_barcode | text | YES |
| 9 | complete_dose_not_given | character varying | YES |
| 10 | dose_due | character varying | YES |
| 11 | dose_due_unit | character varying | YES |
| 12 | dose_given | character varying | YES |
| 13 | dose_given_unit | character varying | YES |
| 14 | will_remainder_of_dose_be_given | character varying | YES |
| 15 | product_amount_given | character varying | YES |
| 16 | product_unit | character varying | YES |
| 17 | product_code | character varying | YES |
| 18 | product_description | character varying | YES |
| 19 | product_description_other | character varying | YES |
| 20 | prior_infusion_rate | character varying | YES |
| 21 | infusion_rate | character varying | YES |
| 22 | infusion_rate_adjustment | character varying | YES |
| 23 | infusion_rate_adjustment_amount | character varying | YES |
| 24 | infusion_rate_unit | character varying | YES |
| 25 | route | character varying | YES |
| 26 | infusion_complete | character varying | YES |
| 27 | completion_interval | character varying | YES |
| 28 | new_iv_bag_hung | character varying | YES |
| 29 | continued_infusion_in_other_location | character varying | YES |
| 30 | restart_interval | character varying | YES |
| 31 | side | character varying | YES |
| 32 | site | character varying | YES |
| 33 | non_formulary_visual_verification | character varying | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- emar_id → mimiciv_hosp.emar.emar_id

### mimiciv_hosp.hcpcsevents — 约 186,074 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | chartdate | date | YES |
| 4 | hcpcs_cd | character | NO |
| 5 | seq_num | integer | NO |
| 6 | short_description | character varying | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id
- hcpcs_cd → mimiciv_hosp.d_hcpcs.code

### mimiciv_hosp.labevents — 约 158,280,921 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | labevent_id | integer | NO |
| 2 | subject_id | integer | NO |
| 3 | hadm_id | integer | YES |
| 4 | specimen_id | integer | NO |
| 5 | itemid | integer | NO |
| 6 | order_provider_id | character varying | YES |
| 7 | charttime | timestamp without time zone | YES |
| 8 | storetime | timestamp without time zone | YES |
| 9 | value | character varying | YES |
| 10 | valuenum | double precision | YES |
| 11 | valueuom | character varying | YES |
| 12 | ref_range_lower | double precision | YES |
| 13 | ref_range_upper | double precision | YES |
| 14 | flag | character varying | YES |
| 15 | priority | character varying | YES |
| 16 | comments | text | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- itemid → mimiciv_hosp.d_labitems.itemid

### mimiciv_hosp.microbiologyevents — 约 3,987,197 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | microevent_id | integer | NO |
| 2 | subject_id | integer | NO |
| 3 | hadm_id | integer | YES |
| 4 | micro_specimen_id | integer | NO |
| 5 | order_provider_id | character varying | YES |
| 6 | chartdate | timestamp without time zone | NO |
| 7 | charttime | timestamp without time zone | YES |
| 8 | spec_itemid | integer | NO |
| 9 | spec_type_desc | character varying | NO |
| 10 | test_seq | integer | NO |
| 11 | storedate | timestamp without time zone | YES |
| 12 | storetime | timestamp without time zone | YES |
| 13 | test_itemid | integer | YES |
| 14 | test_name | character varying | YES |
| 15 | org_itemid | integer | YES |
| 16 | org_name | character varying | YES |
| 17 | isolate_num | smallint | YES |
| 18 | quantity | character varying | YES |
| 19 | ab_itemid | integer | YES |
| 20 | ab_name | character varying | YES |
| 21 | dilution_text | character varying | YES |
| 22 | dilution_comparison | character varying | YES |
| 23 | dilution_value | double precision | YES |
| 24 | interpretation | character varying | YES |
| 25 | comments | text | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.omr — 约 7,752,854 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | chartdate | date | NO |
| 3 | seq_num | integer | NO |
| 4 | result_name | character varying | NO |
| 5 | result_value | text | NO |

### mimiciv_hosp.patients — 约 364,627 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | gender | character | NO |
| 3 | anchor_age | smallint | YES |
| 4 | anchor_year | smallint | NO |
| 5 | anchor_year_group | character varying | NO |
| 6 | dod | date | YES |

### mimiciv_hosp.pharmacy — 约 17,842,631 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | pharmacy_id | integer | NO |
| 4 | poe_id | character varying | YES |
| 5 | starttime | timestamp without time zone | YES |
| 6 | stoptime | timestamp without time zone | YES |
| 7 | medication | text | YES |
| 8 | proc_type | character varying | NO |
| 9 | status | character varying | YES |
| 10 | entertime | timestamp without time zone | NO |
| 11 | verifiedtime | timestamp without time zone | YES |
| 12 | route | character varying | YES |
| 13 | frequency | character varying | YES |
| 14 | disp_sched | character varying | YES |
| 15 | infusion_type | character varying | YES |
| 16 | sliding_scale | character varying | YES |
| 17 | lockout_interval | character varying | YES |
| 18 | basal_rate | real | YES |
| 19 | one_hr_max | character varying | YES |
| 20 | doses_per_24_hrs | real | YES |
| 21 | duration | real | YES |
| 22 | duration_interval | character varying | YES |
| 23 | expiration_value | integer | YES |
| 24 | expiration_unit | character varying | YES |
| 25 | expirationdate | timestamp without time zone | YES |
| 26 | dispensation | character varying | YES |
| 27 | fill_quantity | character varying | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.poe — 约 52,217,621 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | poe_id | character varying | NO |
| 2 | poe_seq | integer | NO |
| 3 | subject_id | integer | NO |
| 4 | hadm_id | integer | YES |
| 5 | ordertime | timestamp without time zone | NO |
| 6 | order_type | character varying | NO |
| 7 | order_subtype | character varying | YES |
| 8 | transaction_type | character varying | YES |
| 9 | discontinue_of_poe_id | character varying | YES |
| 10 | discontinued_by_poe_id | character varying | YES |
| 11 | order_provider_id | character varying | YES |
| 12 | order_status | character varying | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.poe_detail — 约 8,504,141 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | poe_id | character varying | NO |
| 2 | poe_seq | integer | NO |
| 3 | subject_id | integer | NO |
| 4 | field_name | character varying | NO |
| 5 | field_value | text | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- poe_id → mimiciv_hosp.poe.poe_id

### mimiciv_hosp.prescriptions — 约 20,295,526 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | pharmacy_id | integer | NO |
| 4 | poe_id | character varying | YES |
| 5 | poe_seq | integer | YES |
| 6 | order_provider_id | character varying | YES |
| 7 | starttime | timestamp without time zone | YES |
| 8 | stoptime | timestamp without time zone | YES |
| 9 | drug_type | character varying | NO |
| 10 | drug | character varying | NO |
| 11 | formulary_drug_cd | character varying | YES |
| 12 | gsn | character varying | YES |
| 13 | ndc | character varying | YES |
| 14 | prod_strength | character varying | YES |
| 15 | form_rx | character varying | YES |
| 16 | dose_val_rx | character varying | YES |
| 17 | dose_unit_rx | character varying | YES |
| 18 | form_val_disp | character varying | YES |
| 19 | form_unit_disp | character varying | YES |
| 20 | doses_per_24_hrs | real | YES |
| 21 | route | character varying | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.procedures_icd — 约 859,655 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | seq_num | integer | NO |
| 4 | chartdate | date | NO |
| 5 | icd_code | character varying | NO |
| 6 | icd_version | smallint | NO |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.provider — 约 42,244 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | provider_id | character varying | NO |

### mimiciv_hosp.services — 约 593,071 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | transfertime | timestamp without time zone | NO |
| 4 | prev_service | character varying | YES |
| 5 | curr_service | character varying | NO |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_hosp.transfers — 约 2,413,581 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | YES |
| 3 | transfer_id | integer | NO |
| 4 | eventtype | character varying | YES |
| 5 | careunit | character varying | YES |
| 6 | intime | timestamp without time zone | YES |
| 7 | outtime | timestamp without time zone | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id

## mimiciv_icu (9 张表)


### mimiciv_icu.caregiver — 约 17,984 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | caregiver_id | integer | NO |

### mimiciv_icu.chartevents — 约 432,999,623 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | stay_id | integer | NO |
| 4 | caregiver_id | integer | YES |
| 5 | charttime | timestamp without time zone | NO |
| 6 | storetime | timestamp without time zone | YES |
| 7 | itemid | integer | NO |
| 8 | value | character varying | YES |
| 9 | valuenum | double precision | YES |
| 10 | valueuom | character varying | YES |
| 11 | warning | smallint | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id
- stay_id → mimiciv_icu.icustays.stay_id
- itemid → mimiciv_icu.d_items.itemid

### mimiciv_icu.d_items — 约 4,095 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | itemid | integer | NO |
| 2 | label | character varying | NO |
| 3 | abbreviation | character varying | NO |
| 4 | linksto | character varying | NO |
| 5 | category | character varying | NO |
| 6 | unitname | character varying | YES |
| 7 | param_type | character varying | NO |
| 8 | lownormalvalue | double precision | YES |
| 9 | highnormalvalue | double precision | YES |

### mimiciv_icu.datetimeevents — 约 9,980,313 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | stay_id | integer | NO |
| 4 | caregiver_id | integer | YES |
| 5 | charttime | timestamp without time zone | NO |
| 6 | storetime | timestamp without time zone | YES |
| 7 | itemid | integer | NO |
| 8 | value | timestamp without time zone | NO |
| 9 | valueuom | character varying | YES |
| 10 | warning | smallint | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id
- stay_id → mimiciv_icu.icustays.stay_id
- itemid → mimiciv_icu.d_items.itemid

### mimiciv_icu.icustays — 约 94,458 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | stay_id | integer | NO |
| 4 | first_careunit | character varying | YES |
| 5 | last_careunit | character varying | YES |
| 6 | intime | timestamp without time zone | YES |
| 7 | outtime | timestamp without time zone | YES |
| 8 | los | double precision | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id

### mimiciv_icu.ingredientevents — 约 14,255,297 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | stay_id | integer | YES |
| 4 | caregiver_id | integer | YES |
| 5 | starttime | timestamp without time zone | NO |
| 6 | endtime | timestamp without time zone | NO |
| 7 | storetime | timestamp without time zone | YES |
| 8 | itemid | integer | NO |
| 9 | amount | double precision | YES |
| 10 | amountuom | character varying | YES |
| 11 | rate | double precision | YES |
| 12 | rateuom | character varying | YES |
| 13 | orderid | integer | NO |
| 14 | linkorderid | integer | YES |
| 15 | statusdescription | character varying | YES |
| 16 | originalamount | double precision | YES |
| 17 | originalrate | double precision | YES |

### mimiciv_icu.inputevents — 约 10,952,711 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | stay_id | integer | YES |
| 4 | caregiver_id | integer | YES |
| 5 | starttime | timestamp without time zone | NO |
| 6 | endtime | timestamp without time zone | NO |
| 7 | storetime | timestamp without time zone | YES |
| 8 | itemid | integer | NO |
| 9 | amount | double precision | YES |
| 10 | amountuom | character varying | YES |
| 11 | rate | double precision | YES |
| 12 | rateuom | character varying | YES |
| 13 | orderid | integer | NO |
| 14 | linkorderid | integer | YES |
| 15 | ordercategoryname | character varying | YES |
| 16 | secondaryordercategoryname | character varying | YES |
| 17 | ordercomponenttypedescription | character varying | YES |
| 18 | ordercategorydescription | character varying | YES |
| 19 | patientweight | double precision | YES |
| 20 | totalamount | double precision | YES |
| 21 | totalamountuom | character varying | YES |
| 22 | isopenbag | smallint | YES |
| 23 | continueinnextdept | smallint | YES |
| 24 | statusdescription | character varying | YES |
| 25 | originalamount | double precision | YES |
| 26 | originalrate | double precision | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id
- stay_id → mimiciv_icu.icustays.stay_id
- itemid → mimiciv_icu.d_items.itemid

### mimiciv_icu.outputevents — 约 5,359,063 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | stay_id | integer | NO |
| 4 | caregiver_id | integer | YES |
| 5 | charttime | timestamp without time zone | NO |
| 6 | storetime | timestamp without time zone | NO |
| 7 | itemid | integer | NO |
| 8 | value | double precision | NO |
| 9 | valueuom | character varying | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id
- stay_id → mimiciv_icu.icustays.stay_id
- itemid → mimiciv_icu.d_items.itemid

### mimiciv_icu.procedureevents — 约 808,706 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | subject_id | integer | NO |
| 2 | hadm_id | integer | NO |
| 3 | stay_id | integer | NO |
| 4 | caregiver_id | integer | YES |
| 5 | starttime | timestamp without time zone | NO |
| 6 | endtime | timestamp without time zone | NO |
| 7 | storetime | timestamp without time zone | NO |
| 8 | itemid | integer | NO |
| 9 | value | double precision | YES |
| 10 | valueuom | character varying | YES |
| 11 | location | character varying | YES |
| 12 | locationcategory | character varying | YES |
| 13 | orderid | integer | NO |
| 14 | linkorderid | integer | YES |
| 15 | ordercategoryname | character varying | YES |
| 16 | ordercategorydescription | character varying | YES |
| 17 | patientweight | double precision | YES |
| 18 | isopenbag | smallint | YES |
| 19 | continueinnextdept | smallint | YES |
| 20 | statusdescription | character varying | YES |
| 21 | originalamount | double precision | YES |
| 22 | originalrate | double precision | YES |

**外键关系**:
- subject_id → mimiciv_hosp.patients.subject_id
- hadm_id → mimiciv_hosp.admissions.hadm_id
- stay_id → mimiciv_icu.icustays.stay_id
- itemid → mimiciv_icu.d_items.itemid

## mimiciv_note (4 张表)


### mimiciv_note.discharge — 约 331,793 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | note_id | character varying | NO |
| 2 | subject_id | integer | NO |
| 3 | hadm_id | integer | NO |
| 4 | note_type | character varying | NO |
| 5 | note_seq | smallint | NO |
| 6 | charttime | timestamp without time zone | NO |
| 7 | storetime | timestamp without time zone | YES |
| 8 | text | text | NO |

### mimiciv_note.discharge_detail — 约 186,138 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | note_id | character varying | NO |
| 2 | subject_id | integer | NO |
| 3 | field_name | character varying | NO |
| 4 | field_value | text | NO |
| 5 | field_ordinal | integer | NO |

**外键关系**:
- note_id → mimiciv_note.discharge.note_id

### mimiciv_note.radiology — 约 2,319,857 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | note_id | character varying | NO |
| 2 | subject_id | integer | NO |
| 3 | hadm_id | integer | YES |
| 4 | note_type | character varying | NO |
| 5 | note_seq | smallint | NO |
| 6 | charttime | timestamp without time zone | NO |
| 7 | storetime | timestamp without time zone | YES |
| 8 | text | text | NO |

### mimiciv_note.radiology_detail — 约 6,045,596 行

| # | 列名 | 类型 | 可空 |
|---|---|---|---|
| 1 | note_id | character varying | NO |
| 2 | subject_id | integer | NO |
| 3 | field_name | character varying | NO |
| 4 | field_value | text | NO |
| 5 | field_ordinal | integer | NO |