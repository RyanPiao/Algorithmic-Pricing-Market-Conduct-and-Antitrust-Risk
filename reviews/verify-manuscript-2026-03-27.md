# Adversarial Verification Report: Algorithmic Pricing on Airbnb

**Date:** 2026-03-27
**Posture:** Referee 2 -- hostile but fair. Nothing assumed correct until verified.
**Scope:** All 6 .qmd chapters, 11 code scripts, 20 output tables, 8 output figures, references.bib, 5 literature snapshots, NOTATION.md

---

## LENS 1: MATH VERIFICATION

### Equation (1) -- ITT Reduced Form (empirical-strategy.qmd, line 8)

$$
\tilde{Y}_{ict} = \alpha + \tau \cdot \mathbf{1}[t \geq c_0] + \beta_1 \cdot r_t + \beta_2 \cdot r_t \cdot \mathbf{1}[t \geq c_0] + \varepsilon_{ict}
$$

**Notation check:**
- $\tilde{Y}_{ict}$: Residualized log price, listing $i$, city $c$, date $t$. Consistent with text ("described below") and code (s3_03: `log_price_resid`). PASS.
- $c_0$: Cutoff date. Text says September 1, 2023. Code says `CUTOFF = pd.Timestamp("2023-09-01")`. PASS.
- $r_t = t - c_0$: Running variable in days. Code: `df["days_from_cutoff"] = (df["date"] - CUTOFF).dt.days`. PASS.
- $\mathbf{1}[t \geq c_0]$: Treatment indicator. Code: `df["post_cutoff"] = (df["date"] >= CUTOFF)`. PASS.

**Dimensional consistency:**
- LHS: dimensionless (log price residual).
- RHS: $\alpha$ (intercept, dimensionless), $\tau$ (dimensionless, multiplied by indicator), $\beta_1 \cdot r_t$ (coefficient in 1/days times days = dimensionless), $\beta_2 \cdot r_t \cdot \mathbf{1}$ (same). PASS.

**Special cases:**
- At $t = c_0$ (cutoff): $r_t = 0$, $\mathbf{1} = 1$, so $\tilde{Y} = \alpha + \tau$. The discontinuity at the cutoff is $\tau$. PASS.
- Far pre ($t \ll c_0$): $\tilde{Y} = \alpha + \beta_1 r_t$. Linear in running variable. PASS.
- Far post ($t \gg c_0$): $\tilde{Y} = (\alpha + \tau) + (\beta_1 + \beta_2) r_t$. Separate slope. PASS.

**Code implementation (s3_03_itt_rdd.py, line 58):**
```python
X = np.column_stack([np.ones(len(y)), post, x, x * post])
```
This is `[1, D, r, r*D]` where D = post indicator. The coefficient on `post` (index 1) is $\tau$. MATCHES equation (1). PASS.

**ISSUE [MINOR]: Subscript inconsistency between NOTATION.md and equation.**
NOTATION.md lists subscripts as $i$ (listing), $t$ (date), $n$ (neighborhood), $c$ (city). Equation (1) uses $ict$ subscripts, which is consistent with notation. However, NOTATION.md describes the outcome as `log_price_{it}` (no city subscript), while the equation uses `\tilde{Y}_{ict}`. The text says city FE are absorbed in residualization, which would make the $c$ subscript on $\tilde{Y}$ technically redundant after residualization. COSMETIC -- no bias, but could confuse readers.

**ISSUE [MODERATE]: NOTATION.md describes a LATE/IV framework that is not the paper's actual design.**
NOTATION.md defines $\beta$ as "second-stage treatment effect (LATE)", $\pi$ as "first-stage coefficient", and `available_{it}` as "endogenous treatment proxy" with `post_cutoff_{it}` as "instrument." This describes a fuzzy IV/2SLS design. The paper uses a SHARP ITT reduced-form RDD -- no first stage, no LATE. The notation guide is stale and describes an abandoned specification. This is a **documentation mismatch** that would confuse anyone auditing the project.

### Equation (2) -- Year-over-Year DiD (empirical-strategy.qmd, line 56)

$$
Y_{ict} = \gamma_0 + \gamma_1 \cdot \text{Post}_{ct} + \gamma_2 \cdot \text{Year}_t + \tau^{DD} \cdot \text{Post}_{ct} \times \text{Year}_t + \mathbf{X}_{ict}'\delta + \varepsilon_{ict}
$$

**Notation check:**
- $Y_{ict}$: Non-residualized log price (note: NOT $\tilde{Y}$). Consistent with DiD design absorbing seasonality via year differencing. PASS.
- $\text{Post}_{ct}$: Post-rollout indicator. Text says "dates after the rollout-week calendar equivalent." PASS.
- $\text{Year}_t$: Rollout year indicator (2023 vs 2022). PASS.
- $\tau^{DD}$: DiD estimator of interest. PASS.
- $\mathbf{X}_{ict}'\delta$: Covariates. PASS.

**Code implementation (s3_08_ddd_price_levels.py):**
The code does NOT implement equation (2) as written. Instead, it uses Frisch-Waugh two-way demeaning (listing FE + week-of-year FE) and regresses demeaned `log_price` on demeaned `year2023`. This absorbs listing FE ($\alpha_i$) and week FE ($\gamma_w$) via demeaning, then the `year2023` coefficient captures the year-over-year difference. This is a DIFFERENT specification from equation (2):
- Equation (2) has $\text{Post} \times \text{Year}$ interaction. The code's main spec regresses on `year2023` alone (no Post interaction) with listing + week FE.
- The code's "Oct 1 DDD" spec does include `year2023_x_post_oct1`, which is closer to equation (2).

**ISSUE [MAJOR]: Equation (2) does not match the primary DiD implementation.** The main DiD spec in the code is a year fixed-effect model (listing + week FE, coefficient on year2023), not a Post x Year interaction model. Equation (2) describes a traditional DiD with a Post x Year interaction but NO listing or week FE in the written formula. The text calls this "year-over-year DiD" and "DDD" interchangeably, but the code implements a two-way FE model that is conceptually different from the written equation. The paper should either rewrite equation (2) to match the actual specification or explain the equivalence.

**ISSUE [MINOR]: Terminology confusion -- "DDD" vs "DiD."** The table files use "DDD" prefix (ddd_price_levels.md, ddd_variance.md), the code uses "ddd" in filenames, and the text oscillates between "DiD", "DDD", and "year-over-year DiD." A triple-difference requires three dimensions of variation; the design has only two (pre/post and year). Calling it "DDD" is misleading.

---

## LENS 2: EMPIRICAL CLAIMS vs OUTPUT TABLES

### 2.1 Pooled ITT (04-results.qmd, line 7 vs itt_rdd_pooled.md)

| Claim in text | Value in table | MATCH? |
|---|---|---|
| tau = 0.0018 | 0.0018 (all 4 BWs) | PASS |
| SE = 0.0002 | 0.0002 (all 4 BWs) | PASS |
| CI [0.0014, 0.0023] | [0.0014, 0.0023] (all 4 BWs) | PASS |
| 22.6M observations | N = 22,573,179 (resid rows) | PASS (rounds to 22.6M) |
| Raw +30d: 0.0150 | 0.0150 | PASS |
| Raw +45d: -0.0041 | -0.0041 | PASS |
| Raw +60d: -0.0108 | -0.0108 | PASS |
| Raw +90d: -0.0116 | -0.0116 | PASS |

**ISSUE [NOTABLE]: All four residualized bandwidths produce IDENTICAL coefficients, SEs, and CIs (all 0.0018, SE 0.0002, CI [0.0014, 0.0023]).** The table confirms this: all four rows are exactly identical including N = 22,573,179. This is suspicious. Examining the code: s3_03 filters on `days_from_cutoff_resid` (the residualized running variable) within [-bw, +bw]. But the residualized running variable has been demeaned by city x month and day-of-week FE, so its range and distribution differ fundamentally from the raw running variable. After demeaning, the residualized running variable no longer has a clean mapping to "days from cutoff," and bandwidth filtering on the residualized variable likely includes the same observations regardless of the nominal bandwidth. Indeed, all four rows show N = 22,573,179, confirming that bandwidth filtering on the RESIDUALIZED running variable is ineffective -- it captures the entire sample regardless of the bandwidth parameter. **This means the "bandwidth sensitivity" analysis for residualized outcomes is illusory.** The paper claims "near-identical point estimates across bandwidths reflect the effectiveness of the residualization" -- this is wrong. They are identical because the same sample is used each time.

**ISSUE [MODERATE]: The rdrobust rows show "---" for all entries.** The table includes two rdrobust rows (raw and residualized daily means) but both show dashes, meaning rdrobust either failed or was not populated. The text references rdrobust estimates for variance but does not flag the missing pooled rdrobust results. This is an incomplete table.

### 2.2 City-Specific Estimates (04-results.qmd, line 13 vs itt_rdd_city.md)

| Claim | Table | MATCH? |
|---|---|---|
| Austin -3.2% | tau = -0.0323, i.e., -3.23% | PASS |
| NYC +1.7% | tau = 0.0172, i.e., +1.72% | PASS |
| LA +1.2% | tau = 0.0119, i.e., +1.19% | PASS (rounds to +1.2%) |
| DC +0.07%, p=0.53 | tau = 0.0007, p = 0.533 | PASS |

**ISSUE [MINOR]: Text says "Washington, DC (+0.07%, p = 0.53)" but tau = 0.0007 = 0.07%, which is correct. Text says "null" for DC, which is fair given p = 0.53.**

Text says city-specific estimates at "+/-60-day bandwidth on residualized outcomes." Table header confirms "+/-60d, Residualized." PASS.

**ISSUE [MODERATE]: Text cherry-picks cities.** The text reports Austin, LA, NYC, and DC but omits Boston (-0.45%), Chicago (-0.64%), San Francisco (-0.56%), and Seattle (+0.51%). Five of eight cities show NEGATIVE effects. This selective reporting overstates sign heterogeneity. All eight should be mentioned or a summary statement should note that 5/8 are negative.

### 2.3 Variance RDD (04-results.qmd, line 23 vs variance_rdd.md)

| Claim | Table | MATCH? |
|---|---|---|
| 7d = 0.0074 | tau_BC = 0.007358 | PASS (rounds to 0.0074) |
| 14d = 0.0094 | tau_BC = 0.009443 | PASS (rounds to 0.0094) |
| p < 0.001 both | p = 0.0000 both | PASS |

**ISSUE [MAJOR]: Table header says "tau_BC" and "SE_rob" suggesting bias-corrected rdrobust estimates, but the code (s3_04_variance.py) runs OLS local-linear RDD with clustered SEs, NOT rdrobust.** The code's `run_variance_rdd` function uses `sm.OLS` with manual bandwidth of 60 days. The table labels are mislabeled: "tau_BC" should be "tau_OLS" and "SE_rob" should be "SE_cluster". The text says "rdrobust bias-corrected RDD estimates" and "bias-corrected coefficient" -- but the code implements plain OLS. This is a **misrepresentation of the estimation method**.

### 2.4 City Variance (04-results.qmd, line 29 vs variance_city_prepost.md)

| Claim | Table | MATCH? |
|---|---|---|
| Austin +99% | +98.6% | PASS (rounds to 99%) |
| Boston +92% | +92.3% | PASS |
| DC +68% | +68.2% | PASS |
| NYC +45% | +44.5% | PASS (rounds to 45%) |
| Chicago -1.0% | -1.0% | PASS |
| LA -2.5% | -2.5% | PASS |
| Seattle +2.8% | +2.8% | PASS |

All city variance claims verified. PASS.

### 2.5 Leave-One-Out (04-results.qmd, line 59 vs leave_one_out.md)

| Claim | Table | MATCH? |
|---|---|---|
| Drop Austin: +0.0077 | 0.0077 | PASS |
| Drop LA: -0.0023 | -0.0023 | PASS |
| Range 0.0019 to 0.0024 for "most" | Boston 0.0019, Chicago 0.0019, SF 0.0024, Seattle 0.0019, DC 0.0019 | PASS |

Text says "Dropping Los Angeles or New York City flips the sign to negative." Table: drop LA = -0.0023, drop NYC = -0.0011. PASS.

**ISSUE [MINOR]: Table headers say "tau_BC" and "SE_rob" but the code (s3_06_falsification.py, `leave_one_city_out` function) uses OLS with clustered SEs, not rdrobust.** Same mislabeling issue as the variance table. The leave-one-out is computed using `log_price_resid` and `days_from_cutoff_resid` with manual bandwidth of 60, plain OLS clustering at listing level.

### 2.6 DiD Estimates (04-results.qmd, line 67 vs ddd_price_levels.md)

| Claim | Table | MATCH? |
|---|---|---|
| Full window: -0.0054, p<0.001 | -0.0054, p=0.000 | PASS |
| Drop Dec: -1.6% | -0.0162 = -1.62% | PASS |

### 2.7 DiD Variance (04-results.qmd, line 75 vs ddd_variance.md)

| Claim | Table | MATCH? |
|---|---|---|
| 7d: -0.0008 | -0.000796 | PASS (rounds to -0.0008) |
| 14d: -0.0008 | -0.000842 | PASS (rounds to -0.0008) |

**ISSUE [MINOR]: Text says both are "-0.0008" but they are actually different: -0.000796 vs -0.000842. Rounding both to 4 decimal places: -0.0008 vs -0.0008 is technically correct but loses the distinction.**

### 2.8 Sample Sizes (introduction.qmd vs code)

| Claim | Source | MATCH? |
|---|---|---|
| 24.2M listing-day obs | Code output N for raw +90d = 22,228,725; residualized = 22,573,179. Neither is 24.2M. | **FAIL** |
| 22.6M observations | Residualized panel N = 22,573,179 | PASS |
| 131,677 unique listings | Not directly verifiable from tables. Text in 02-data-and-setting says "131,677 unique listings" | UNVERIFIED |

**ISSUE [MAJOR]: The introduction claims "24.2 million listing-day observations" for the +/-3 month estimation sample, but the output tables show the largest N is 22,573,179 (residualized) or 22,228,725 (raw +/-90d). The 24.2M figure appears nowhere in the output.** Possible explanations: (1) the 24.2M is the pre-filtering count from the build_panel step (before dropping NaN rows in residualization); (2) the +/-3 month window is wider than +/-90 days (3 months ~ 91 days, so +/-3m may include a few more observations). But the discrepancy (~1.6M rows) is large enough to require verification. The paper should report the ACTUAL estimation sample size consistently.

### 2.9 Covariate Balance

Text says "accommodates (+0.034)" -- table shows 0.0337. PASS (rounds to 0.034).
Text says "bedrooms (+0.013)" -- table shows 0.0130. PASS.
Text says "number of reviews (-2.30)" -- table shows -2.2985. PASS (rounds to -2.30).
Text says "host listing count (-0.18)" -- table shows -0.1832. PASS.

### 2.10 Event Study

Text says "pre-period coefficients range from 0.0026 to 0.0087." Table: pre-period bins (excluding reference): 0.0031, 0.0037, 0.0087, 0.0029, 0.0060, 0.0026. Range = [0.0026, 0.0087]. PASS.
Text says "first two weeks post: 0.0151." Table: [0, 14) bin = 0.0151. PASS.

---

## LENS 3: CAUSAL LOGIC

### 3.1 Causal Claim

The paper claims: (a) algorithm availability does not raise aggregate price levels, (b) it increases within-listing price variance, (c) effects concentrate among sophisticated hosts. The causal mechanism is technology-skill complementarity -- the algorithm enables better intertemporal price discrimination for hosts who can leverage it.

### 3.2 Identification Strategy

Sharp ITT reduced-form RDD exploiting the September 1, 2023 platform-wide rollout as a common cutoff across 8 cities. Running variable is days from cutoff. Local linear polynomial with symmetric bandwidth.

**Key Identifying Assumption:** Smoothness -- $E[Y(0) | r]$ is continuous through the cutoff. The text correctly states this.

### 3.3 Is Smoothness Credible?

**ISSUE [CRITICAL]: The density test reveals a MAJOR violation.** The density plot shows a sharp jump from ~117,000 listings/day pre-cutoff to ~130,000 listings/day post-cutoff -- an 11% increase. This is not a smooth transition; it is a discrete compositional change at the cutoff. The standard McCrary/CJM density test is designed to detect manipulation, but in RDiT, it detects composition changes (entry/exit). An 11% jump in the number of active listings is a SEVERE threat to the smoothness assumption. The paper acknowledges this ("The density jump does not invalidate the RDD if the entering listings are comparable to incumbents on observables") but this defense is undermined by the covariate balance results showing significant discontinuities in ALL EIGHT covariates tested.

**ISSUE [CRITICAL]: ALL covariate balance tests fail.** Every single predetermined covariate (accommodates, bedrooms, bathrooms, reviews, review score, superhost, instant bookable, host listing count) shows a statistically significant discontinuity at p < 0.01. The paper dismisses this as "the statistical significance reflects the extreme precision afforded by the sample size, not economically meaningful selection" -- but this is special pleading. The combination of (a) an 11% density jump and (b) significant imbalance in ALL covariates means the composition of listings changes discretely at the cutoff. The smoothness assumption is NOT credible without further adjustment. The residualization absorbs city x month FE, but if the September compositional shift is within-city (e.g., seasonal listings activating), the residualization does not address it.

### 3.4 Pre-Trends

**ISSUE [MAJOR]: Pre-trends are NOT flat.** The event study shows ALL pre-period coefficients are statistically significant at p < 0.05 (the text acknowledges this). Magnitudes range from 0.26% to 0.87%. While individually small, their significance and non-monotonic pattern indicate that the residualization has not fully removed seasonal confounding. The paper says "the magnitudes are small enough that they do not undermine the core finding" -- a referee would note that this is a judgment call, not a testable claim. If residual seasonality generates pre-trend coefficients of 0.3-0.9%, it could also generate a post-cutoff coefficient of 0.18%. The treatment effect is SMALLER than several pre-period coefficients, which severely weakens identification.

### 3.5 Variance Sign Disagreement

**ISSUE [CRITICAL]: The RDD and DiD give OPPOSITE signs for the variance finding.** The RDD estimates positive variance effects (7d: +0.0074, 14d: +0.0094), while the DiD estimates negative variance effects (7d: -0.0008, 14d: -0.0008). The paper offers two explanations: (1) secular upward trend in pricing flexibility absorbed by DiD but not RDD, (2) different confounders across designs. Both are plausible but unverifiable. A hostile referee would note that when your two identification strategies give OPPOSITE SIGNS for the same outcome, neither result is convincingly identified. The paper should either:
- Present a formal model of the secular trend and show it explains the discrepancy, OR
- Substantially downgrade the variance finding from "the algorithm's primary footprint" to "suggestive evidence that requires further investigation."

The text handles this honestly (Section 4.5) but the Introduction and Conclusion trumpet the variance finding as if it were robust. The sign disagreement should be foregrounded much more prominently.

### 3.6 Placebo Outcome Failure

**ISSUE [MAJOR]: The minimum-nights placebo test FAILS catastrophically.** The DiD shows a -3.62 discontinuity in minimum nights (p < 0.001). This means Airbnb changed minimum-night requirements around the same rollout window. This is a smoking gun for **bundled platform changes** -- the September 2023 update was not just a pricing tool redesign but included other policy changes. If minimum-night requirements changed simultaneously, the "treatment" is not cleanly identified as "pricing tool availability" but rather "the September 2023 platform update package." Any price or variance effects could reflect the minimum-night change rather than the pricing tool.

---

## LENS 4: CITATIONS

### 4.1 Citekey Verification Against references.bib

All citekeys appearing in the .qmd chapters were checked against references.bib.

**Present and matched:**
- @calvano2020artificial -- PRESENT
- @brown2025algorithmic -- PRESENT
- @ye2018customized -- PRESENT
- @hausman2018regression -- PRESENT
- @noack2025flexible -- PRESENT
- @calonico2014robust -- PRESENT
- @assad2024algorithmic -- PRESENT
- @musolff2022algorithmic -- PRESENT
- @huang2025pricing -- PRESENT
- @foroughifar2024challenges -- PRESENT
- @zhang2025smart -- PRESENT
- @hazledine2006price -- PRESENT
- @cattaneo2020density -- PRESENT
- @autor2003skill -- PRESENT
- @bresnahan2002information -- PRESENT
- @brynjolfsson2025generative -- PRESENT
- @mackowiak2009optimal -- PRESENT
- @calderwang2024coordinated -- PRESENT
- @lambin2024learning -- PRESENT
- @bichler2024online -- PRESENT
- @harrington2026hub -- PRESENT
- @garcia2024cognitive -- PRESENT
- @alsudais2021incorrect -- PRESENT
- @murphy1985estimation -- PRESENT

**MISSING from references.bib (cited in text but no bib entry):** NONE found. All citekeys match.

**Entries in .bib not cited in any chapter:** calvano2020protecting, noack2024bias, cattaneo2021multi, werner2026algorithmic, bichler2025survey, fish2024algorithmic, mackowiak2023rational, callaway2021difference, chernozhukov2018double, dou2025ai. These are unused entries -- not an error, but the .bib could be cleaned.

### 4.2 Key Empirical Claims vs Literature Snapshots

**Assad "38%" claim (01-introduction.qmd line 15):**
Text says: "@assad2024algorithmic provide the strongest quasi-experimental evidence of algorithmic collusion in German gasoline duopolies."
Related work (05-related-work.qmd line 5): "document a 38% margin increase in German gasoline duopolies with mutual algorithmic adoption."
Literature snapshot: "Both stations adopted: Mean market margin +3.2 cents (SE 0.012, p<0.01), ~38% increase."
**VERIFIED.** The 38% figure refers to the duopoly both-adopt market-level margin increase (3.2 cents on a 8.3-cent baseline). PASS.

**Foroughifar "22%" claim (01-introduction.qmd line 17, 02-data-and-setting.qmd line 59):**
Text says: "only 22% of hosts adopt Smart Pricing."
Literature snapshot: "Why is the adoption rate of Airbnb's Smart Pricing (SP) algorithm surprisingly low (only 22% of hosts over 20 months)."
**VERIFIED.** PASS.

**ISSUE [MINOR]: The 22% figure is from Foroughifar's sample period (Oct 2014 - Aug 2017, i.e., the original 2015 Smart Pricing). The paper's treatment event is the 2023 Summer Release redesign, not the original Smart Pricing. Adoption rates may differ substantially for the 2023 version. The text should flag this temporal mismatch more explicitly.**

**Huang "85%" claim (01-introduction.qmd line 17):**
Text says: "@huang2025pricing structurally estimates that 85% of Airbnb hosts set near-uniform prices."
Literature snapshot: "Most sellers (~85%) set highly inflexible prices."
**VERIFIED.** PASS.

**ISSUE [MINOR]: Huang's 85% figure is from San Francisco only. Extrapolating to 8 cities as if universal requires a caveat.**

---

## LENS 5: CODE PIPELINE

### 5.1 Code Dates vs Output Dates

All 11 code scripts were last modified on March 22, 2026 (15:43 to 19:55). All output tables were generated on March 22, 2026 (16:38 to 20:02). All output figures were generated on March 22, 2026 (16:41 to 20:02).

**Temporal consistency:** Code files were modified BEFORE their corresponding output files. The pipeline appears to have been run sequentially on March 22:
- s3_01 (15:47) -> s3_02 (16:06) -> s3_03 (16:33) -> tables at 16:38
- s3_04 (17:00) -> variance tables at 17:02
- s3_05 (event study plots at 16:41 -- BUT s3_05 code timestamp is 15:43, BEFORE s3_03). This is INCONSISTENT: s3_05 was modified at 15:43 but its output was generated at 16:41, and it depends on the residualized panel from s3_02 (16:06). Likely explanation: s3_05 was edited before the run but executed later in the pipeline. This is a MINOR timing anomaly, not necessarily an error.
- s3_06 (17:31) -> falsification outputs at 17:31-17:37
- s3_07-s3_11 (19:52-19:55) -> DDD outputs at 19:57-20:02

**PASS with minor note.** All outputs appear to come from a single pipeline run on March 22.

### 5.2 Random Seeds

| Script | Seed | Consistent? |
|---|---|---|
| s3_01_build_panel.py | SEED = 42, np.random.seed(42) | YES |
| s3_02_residualize.py | SEED = 42, np.random.seed(42), plus RandomState(42) for folds | YES |
| s3_03_itt_rdd.py | SEED = 42 (declared but not called -- no randomness in this script) | OK |
| s3_04_variance.py | SEED = 42 (declared but not called) | OK |
| s3_05_event_study.py | SEED = 42 (declared but not called) | OK |
| s3_06_falsification.py | SEED = 42, np.random.seed(42) | YES |
| s3_07_build_ddd_panel.py | SEED = 42, np.random.seed(42) | YES |
| s3_08_ddd_price_levels.py | SEED = 42 (declared but not called) | OK |
| s3_09_ddd_variance.py | SEED = 42 (declared, RandomState(42) for scatter subsample) | YES |
| s3_10_ddd_event_study.py | SEED = 42 (declared but not called) | OK |
| s3_11_ddd_falsification.py | SEED = 42 (declared but not called) | OK |

All seeds are consistently set to 42. PASS.

### 5.3 Absolute Paths

All code scripts use `REPO = Path(__file__).resolve().parent.parent` for relative path construction. No hardcoded absolute paths found. Data input is from `REPO / "data" / "merge"` and `REPO / "data" / "processed"`. PASS.

**ISSUE [MINOR]: s3_01_build_panel.py references `DATA_MERGE = REPO / "data" / "merge"` which expects merged city CSV files from an external source. The pipeline is not self-contained -- it depends on a prior merge step not included in the 11 scripts. Reproducibility requires documenting this upstream dependency.**

### 5.4 Cutoff Date Consistency

| Location | Cutoff | Match? |
|---|---|---|
| 01-introduction.qmd | "September 1, 2023" | YES |
| 02-data-and-setting.qmd | "September 1, 2023" | YES |
| 03-empirical-strategy.qmd | "September 1, 2023" | YES |
| s3_01_build_panel.py | `CUTOFF = pd.Timestamp("2023-09-01")` | YES |
| s3_02_residualize.py | `"cutoff": "2023-09-01"` in metadata | YES |
| s3_03_itt_rdd.py | `"cutoff": "2023-09-01"` in metadata | YES |
| s3_05_event_study.py | `CUTOFF = pd.Timestamp("2023-09-01")` | YES |

All consistent. PASS.

**Beta date:** Text says "May 3, 2023." Code: `BETA_DATE = pd.Timestamp("2023-05-03")`. PASS.

### 5.5 Clustering

Text says "Standard errors are clustered at the listing level." Code: `cov_type="cluster", cov_kwds={"groups": sub["listing_city"].values}` where `listing_city = city_slug + "_" + listing_id`. This clusters at the listing-within-city level, which is correct since the same listing_id could theoretically appear in different cities (it cannot in Airbnb, but the concatenation is a safe practice). PASS.

---

## LENS 6: OVERCLAIMING

### 6.1 "Ruling Out >3%"

Introduction (line 9): "The 95% confidence interval rules out effects larger than approximately 0.23 percent, far below the thresholds that would signal market-wide coordination."
Results (line 7): "The 95% confidence interval of [0.0014, 0.0023] rules out effects larger than approximately 0.23 percent in either direction."

**ISSUE [MODERATE]: The CI is [0.0014, 0.0023], which means the UPPER bound is 0.23%. But this CI does NOT rule out effects of 0.23% "in either direction" -- it rules out negative effects (the lower bound is 0.0014, positive). The effect is POSITIVE and significant at p < 0.001. The correct statement is: "the upper bound of the CI rules out effects above 0.23%." The claim that effects are "ruled out in either direction" is technically wrong -- the CI excludes zero.**

Conclusion (line 3): "rules out economically meaningful collusion effects above approximately 0.23 percent." This phrasing is correct. PASS.

**The "3% threshold" claim:** The power analysis section says "The MDE at 80% power is roughly 50 times smaller than the 3 percent threshold that would signal meaningful collusion." Where does the 3% threshold come from? It is not derived from theory, not cited to any source, and not justified. Assad et al. find 38% in gasoline; even a 1% effect could be policy-relevant in a large market. The 3% threshold appears to be chosen post hoc to make the null look impressive.

**ISSUE [MODERATE]: The "3% collusion threshold" is asserted without justification.** A skeptical referee would ask: who says 3% is the right threshold? The introduction's claim to "rule out >3%" is not actually supported by the CI (which rules out >0.23%), making the 3% framing a strawman.

### 6.2 "Algorithms Don't Cause Collusion"

Conclusion (line 5): "The growing concern that platform-provided pricing algorithms facilitate tacit collusion...does not find support in our setting."

This is carefully worded ("in our setting"). PASS.

But the policy recommendation is stronger: "Regulators should focus enforcement on markets with oligopolistic features rather than applying blanket restrictions to platform pricing tools."

**ISSUE [MAJOR]: This policy recommendation is overclaimed.** The paper studies ONE platform (Airbnb) in ONE country (US) during ONE rollout event (September 2023). The null finding could be specific to: (a) Airbnb's market structure, (b) the particular algorithm design, (c) the low adoption rate (~22%), (d) the short post-period, or (e) the data limitations (posted prices, not transaction prices). Recommending that regulators relax scrutiny of platform pricing tools based on a single null result from a single platform is an unwarranted extrapolation. The paper's own limitations section (conclusion, line 9) acknowledges "our analysis covers a single platform in a single country" and "whether the findings generalize...remains open." The policy recommendation contradicts this caveat.

### 6.3 Variance Claim

Introduction (line 11): "algorithm availability significantly increases within-listing temporal price variance."
Conclusion (line 3): "the algorithm's primary footprint is a significant increase in within-listing temporal price variance."

**ISSUE [MAJOR]: The variance finding is not robust across designs.** As documented in Lens 3, the RDD shows positive variance effects while the DiD shows negative variance effects. Calling the variance increase "the algorithm's primary footprint" in the abstract/conclusion is overclaimed. At minimum, the conclusion should note the sign disagreement and hedge the variance interpretation accordingly.

### 6.4 Technology-Skill Complementarity

Introduction (line 13): "pricing changes concentrate among hosts with high pre-existing pricing sophistication...consistent with technology-skill complementarity."

The empirical strategy (section 3.7) explicitly labels this analysis as "descriptive" and notes the generated-regressor concern. Good. But the introduction and conclusion present it as a substantive finding rather than a descriptive pattern. This is **borderline overclaiming** -- the description is appropriate but the framing elevates it beyond what the evidence supports.

### 6.5 Comparison to Assad et al.

Introduction (line 19): "Together, the two papers map the boundaries of when algorithmic pricing raises prices versus when it enables price discrimination."

**ISSUE [MINOR]: This is a strong framing claim for a working paper comparing itself to a JPE publication.** Two data points (gasoline duopoly, Airbnb platform) do not "map boundaries." They provide two observations. The framing should be "suggestive" rather than definitive.

---

## SUMMARY OF FINDINGS BY SEVERITY

### CRITICAL (3)

1. **Density test shows 11% jump + all covariate balance tests fail.** The smoothness assumption is not credible. The RDD design has a fundamental identification problem. (Lens 3)
2. **Variance sign disagreement: RDD positive, DiD negative.** The core variance finding is not robust across identification strategies. (Lens 3)
3. **Minimum-nights placebo failure.** Bundled platform changes confound the treatment. (Lens 3)

### MAJOR (5)

4. **Equation (2) does not match the DiD code implementation.** The written specification describes a Post x Year interaction model; the code implements a two-way FE year-coefficient model. (Lens 1)
5. **Variance RDD table mislabeled as "bias-corrected rdrobust" when it is OLS.** The paper claims rdrobust estimation for variance but the code uses plain OLS. (Lens 2)
6. **Bandwidth sensitivity is illusory for residualized outcomes.** All four bandwidth rows are identical because filtering on the residualized running variable captures the entire sample. (Lens 2)
7. **24.2M sample size claim does not match any output table.** Largest N in tables is 22.6M. (Lens 2)
8. **Policy recommendation ("regulators should relax scrutiny") overclaimed from a single-platform null.** (Lens 6)

### MODERATE (7)

9. NOTATION.md describes abandoned IV/LATE design, not the actual sharp ITT. (Lens 1)
10. "DDD" terminology used for a two-dimensional DiD design. (Lens 1)
11. Pre-trends not flat: all pre-period event-study coefficients significant, some larger than treatment effect. (Lens 3)
12. CI rules out effects "in either direction" -- incorrect; effect is positive and significant. (Lens 6)
13. "3% collusion threshold" asserted without source or justification. (Lens 6)
14. Variance finding trumpeted in introduction/conclusion despite sign disagreement. (Lens 6)
15. Leave-one-out table headers mislabel OLS estimates as rdrobust. (Lens 2)

### MINOR (7)

16. City-specific results selectively reported (4 of 8 cities in text). (Lens 2)
17. $\tilde{Y}_{ict}$ city subscript redundant after residualization. (Lens 1)
18. Foroughifar 22% adoption rate is from 2015-2017, not 2023 rollout. (Lens 4)
19. Huang 85% is San Francisco only, presented as general. (Lens 4)
20. DiD variance rounding loses distinction between -0.000796 and -0.000842. (Lens 2)
21. Upstream data merge step not documented in pipeline. (Lens 5)
22. "Map the boundaries" framing too strong for two-observation comparison. (Lens 6)

---

## REFEREE RECOMMENDATION

**MAJOR REVISION.** The paper addresses an important and policy-relevant question, and the data collection and pipeline are competently executed. However, the identification strategy has fundamental weaknesses that the current draft does not adequately confront:

1. The RDD smoothness assumption is contradicted by the density jump and universal covariate imbalance. The paper needs either (a) a convincing argument that the compositional change is orthogonal to potential outcomes (e.g., by showing the new entrants have similar price distributions), or (b) a primary specification that addresses composition (e.g., balanced-panel RDD on listings present throughout the window).

2. The variance finding must be substantially reframed given the sign disagreement between RDD and DiD. Present both results with equal prominence and discuss what must be true about secular trends for each to be the correct causal estimate.

3. Equation (2) must match the code. The mislabeling of OLS estimates as rdrobust must be corrected.

4. The policy recommendation should be toned down to match the evidence: a single null finding from one platform does not justify recommending reduced regulatory scrutiny of algorithmic pricing tools in general.

5. The bundled-treatment concern (minimum nights changing simultaneously) should be addressed head-on, ideally with a specification that controls for minimum-night changes or with a subsample analysis excluding listings affected by the minimum-night policy change.

The null finding on price levels is likely robust and informative -- it survives across designs and cities. The variance and heterogeneity findings are interesting but require stronger evidence before they can be presented as established results.
