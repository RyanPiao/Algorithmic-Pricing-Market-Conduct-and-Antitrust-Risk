# Noack & Rothe -- RDD Inference Papers (Snapshot)

*Created: 2026-03-22*

There are **two distinct papers** by this author team relevant to RDD methodology. Both are summarized below.

---

## Paper 1: Bias-Aware Inference in Fuzzy RDD (Econometrica 2024)

### Citation

Noack, Claudia, and Christoph Rothe. 2024. "Bias-Aware Inference in Fuzzy Regression Discontinuity Designs." *Econometrica* 92 (3): 687--711. DOI: [10.3982/ECTA19466](https://doi.org/10.3982/ECTA19466).

### Research question

How should we construct confidence sets for treatment effects in fuzzy RDD that remain valid when standard delta-method approximations break down -- e.g., with discrete running variables, donut designs, or weak identification?

### Key innovation

They propose **bias-aware confidence sets** that explicitly incorporate the magnitude of possible estimation bias into the confidence interval, rather than first bias-correcting and then constructing standard CIs (the CCT 2014 approach). The construction is analogous to Anderson--Rubin confidence sets in IV models: they invert a test statistic over a grid of parameter values, checking which values are compatible with the data given a bound on the bias. This avoids the delta-method approximation that standard fuzzy RDD inference relies on (where the Wald ratio's denominator can be close to zero).

### Technical details

- **Estimator basis**: Local linear regression, as in the standard CCT framework.
- **Bias handling**: Instead of subtracting an estimated bias term and then doing standard inference (as in CCT 2014's robust bias-corrected CIs), they assume the regression function belongs to a Holder smoothness class with parameter alpha in (0, 2]. The bias is bounded by B * h^(p+1), and the confidence set is constructed to have correct coverage *uniformly* over all DGPs in the smoothness class.
- **Key difference from CCT (2014)**: CCT estimates the bias using a higher-order local polynomial, subtracts it, and then uses a standard normal critical value (with adjusted variance). Noack--Rothe instead keep the bias as a nuisance parameter and construct CIs that are valid for all bias values within the bound. This is more conservative but avoids relying on the estimated bias being accurate.
- **Anderson--Rubin analogy**: In fuzzy RDD, the estimand is a ratio (reduced-form jump / first-stage jump). Rather than estimating this ratio and applying the delta method, they test H0: tau = tau_0 for each candidate value tau_0, constructing the CS as the set of non-rejected values. This is robust to weak first stages.
- **Validity conditions**: The CSs are asymptotically equivalent to CCT in canonical settings (continuous running variable, strong first stage). But they also cover: (a) discrete running variables, (b) donut designs, (c) weak identification / small first stage.

### Relevance to our paper

**Moderate, but not directly applicable.** This paper is specifically about *fuzzy* RDD, where the key problem is the ratio estimator and delta-method failure. Since we are switching to a **sharp ITT reduced form**, we do not have a fuzzy design and do not face the Wald-ratio / weak-identification issues that motivate this paper. The bias-awareness concept is intellectually relevant -- our sharp RD estimates also have bias from local polynomial approximation -- but the specific machinery (AR-type inversion of the Wald ratio) is not needed.

**Recommendation**: Cite in a footnote when discussing our choice of sharp over fuzzy design, noting that fuzzy RDD inference has additional complications (Noack and Rothe 2024). Do not adopt their specific estimator.

### Implementation

- Replication package on Zenodo: <https://doi.org/10.5281/zenodo.10724847> (R scripts).
- No standalone R/Stata package beyond replication code. The authors use `rdrobust` for bandwidth selection within their code.

---

## Paper 2: Flexible Covariate Adjustments in RDD (Working Paper)

### Citation

Noack, Claudia, Tomasz Olma, and Christoph Rothe. 2025. "Flexible Covariate Adjustments in Regression Discontinuity Designs." Working paper, arXiv: [2107.07942](https://arxiv.org/abs/2107.07942). Latest revision: April 2025.

*Note: As of March 2026, this paper appears to remain a working paper. It has not been confirmed as published in a journal, though it has been actively circulated on the seminar circuit (LSE, Erasmus, Manchester, TSE) and revised through v5.*

### Research question

How can researchers efficiently incorporate covariate information in RDD estimation, especially when there are many covariates and the optimal adjustment function is unknown?

### Key innovation

They propose a **two-step procedure**: (1) estimate an adjustment function g(X) that predicts the outcome from covariates, then (2) run a standard local linear RDD analysis on the *adjusted* outcome Y-tilde = Y - g(X). The critical insight is a **robustness property unique to the RDD setting**: the first-order asymptotic properties of the final RD estimator (bias, variance, distribution) are *invariant* to the estimation error in g(X). This means g(X) can be estimated using flexible machine learning methods (random forests, LASSO, neural nets) without affecting the validity of standard RDD inference.

### Technical details

- **Estimator**: Compute Y-tilde_i = Y_i - g-hat(X_i), then apply standard local linear RD estimation to Y-tilde. The function g-hat can be any consistent estimator of E[Y|X] (or a related conditional expectation).
- **Optimal adjustment**: They characterize the variance-minimizing g*(X) = E[Y|X], i.e., the conditional expectation of the outcome given covariates (evaluated away from the cutoff). Using g* yields maximum efficiency gains.
- **Key assumptions**: Standard RDD smoothness conditions on conditional expectations near the cutoff. The adjustment function g is estimated on the *full* sample (not just near the cutoff), so convergence rates for g-hat can be slow without affecting RD inference.
- **Comparison to CCFT (2019)**: Calonico, Cattaneo, Farrell, and Titiunik (2019) proposed including covariates linearly in the local polynomial regression. Noack--Olma--Rothe show that (a) CCFT's linear adjustment is a special case of their framework, and (b) their method can achieve *larger* efficiency gains when the true adjustment function is nonlinear or when there are many covariates. With a linear g, the two approaches have the same asymptotic variance.
- **Bandwidth and inference**: Because of the robustness property, the researcher can use *existing* bandwidth selectors and bias-corrected inference procedures (e.g., `rdrobust`) directly on Y-tilde, with no modifications needed.

### Relevance to our paper

**HIGH -- this is directly useful.** Our design has multi-city cutoffs with seasonal controls and potentially many city-level covariates. This method allows us to:

1. Flexibly adjust for city characteristics, seasonal patterns, and other covariates *before* running the RD, which can substantially reduce variance and tighten confidence intervals.
2. Use machine learning to estimate the adjustment function without jeopardizing the validity of our RD inference.
3. Continue using `rdrobust` for bandwidth selection and bias-corrected inference on the adjusted outcome.

**Recommendation**: Adopt this method. In practice: (a) estimate g-hat(X) via random forest or LASSO on the full sample, predicting Y from city characteristics, seasonal dummies, and other covariates; (b) compute Y-tilde = Y - g-hat(X); (c) run `rdrobust` on Y-tilde as the outcome. Report standard CCT-style robust bias-corrected confidence intervals. Discuss in the empirical strategy section (not just robustness) since it is part of the main estimation procedure.

### Implementation

- **Python**: Implemented in the `DoubleML` package as `RDFlex` (module `doubleml.rdd`). Install via `pip install doubleml` plus `pip install rdrobust`. See [DoubleML RDFlex documentation](https://docs.doubleml.org/stable/examples/py_double_ml_rdflex.html).
- **R**: No dedicated CRAN package as of March 2026. The procedure is simple to implement manually: estimate g-hat with any ML method, subtract from Y, then use `rdrobust` on the residual. The `rdrobust` package handles bandwidth selection and bias-corrected inference.
- **Stata**: Same manual procedure -- predict, subtract, run `rdrobust`.

### How to cite in our paper

Reference in the **empirical strategy section** when describing the estimation procedure:

> "Following Noack, Olma, and Rothe (2025), we adjust the outcome variable by subtracting a flexible function of covariates estimated via [method], then estimate the RD treatment effect on the adjusted outcome using local linear regression with the bias-corrected robust inference procedures of Calonico, Cattaneo, and Titiunik (2014)."

Also cite in a methods footnote explaining why flexible (ML-based) covariate adjustment does not invalidate standard RD inference.

---

## Summary Table

| Feature | Noack & Rothe (2024, Econometrica) | Noack, Olma & Rothe (2025, WP) |
|---|---|---|
| Focus | Fuzzy RDD inference | Covariate adjustment in RDD |
| Design type | Fuzzy | Sharp and fuzzy |
| Key problem solved | Delta-method failure in Wald ratio | Efficient use of many covariates |
| Relevance to us | Low (we use sharp ITT) | **High** (we have many covariates) |
| Software | Replication code (R) | DoubleML/Python; manual in R/Stata |
| Where to cite | Footnote on fuzzy vs. sharp | Empirical strategy section |

---

## DEEP READ — Paper 2: Flexible Covariate Adjustments (added 2026-03-22)

*Based on full reading of arXiv:2107.07942v5 (April 28, 2025), 44 pages + Online Supplement.*

### Core methodology — step by step

The procedure is **not** simply "estimate g(X), subtract, run rdrobust." The paper is more precise. Here is the exact algorithm (Section 3.2, p. 10):

**Step 1 — Cross-fit the adjustment function:**
1. Randomly split the data {W_i} into S folds of equal size (S = 5 or S = 10 recommended).
2. For each fold s, estimate the adjustment function eta-hat_s(z) using **only data outside fold s** (leave-fold-out).
3. For each observation i in fold s, compute the adjusted outcome: M_i(eta-hat_{s(i)}) = Y_i - eta-hat_{s(i)}(Z_i).

**Step 2 — Standard RD estimation on adjusted outcomes:**
4. Run a standard local linear no-covariates RD estimator on the generated data {(X_i, M_i(eta-hat_{s(i)}))}, treating the adjusted outcome as if eta-hat were known (i.e., ignoring estimation uncertainty in eta-hat).
5. Apply standard bandwidth selection (CCT 2014 or IK 2012) and standard inference (bias-corrected CIs, bias-aware CIs, or undersmoothing) to this adjusted dataset.

**Critical detail — the adjustment function eta-hat must be the SAME on both sides of the cutoff.** Using different adjustment functions on either side would yield inconsistent RD estimates (footnote 1, p. 3; also eq. 3.1 discussion, p. 9).

**What is the optimal adjustment function eta_0?**
It is the equally-weighted average of left and right conditional expectations (eq. 3.4, p. 10):

> eta_0(z) = (1/2)(mu_0^+(z) + mu_0^-(z)), where mu_0^*(z) = E[Y_i | X_i = 0^*, Z_i = z] for * in {+, -}.

This is NOT simply E[Y|Z] — it is the average of E[Y|X just above cutoff, Z=z] and E[Y|X just below cutoff, Z=z]. In practice, since we cannot condition on X_i = 0 exactly, this is approximated by learning the conditional mean near (but on each side of) the cutoff.

### ML methods that can be used for eta-hat

The paper explicitly lists (p. 3, p. 12):
- **LASSO / post-LASSO regression**
- **Random forests** (implemented via `ranger` package with 1000 trees)
- **Deep neural networks**
- **Boosted trees** (implemented via `xgboost`, depth 2, shrinkage 0.1)
- **Ensemble combinations** (Super Learner, Van der Laan et al. 2007)
- Classical nonparametric methods (local polynomials, series regression) for low-dimensional Z
- Parametric specifications (as special case)

**Their recommended implementation (Section 3.4):** An ensemble of 8 learners: (i) linear regression, (ii) post-LASSO, (iii) boosted trees, (iv) random forest — each in both "localized" and "global" versions. The ensemble weights are chosen via Super Learner (cross-validation to minimize MSE near the cutoff). The trivial no-adjustment function is included as a ninth candidate to guard against adjustments that add noise.

**Two implementation strategies for ML (Section 3.3):**
1. **"Global"**: Include the treatment indicator T_i = 1{X_i >= 0} as a predictor in the ML model alongside X_i and Z_i. The ML learner produces a function with a jump at the cutoff. Estimate mu^+(z) as E-hat[Y | T=1, X=0, Z=z] and mu^-(z) as E-hat[Y | T=0, X=0, Z=z]. Uses all observations.
2. **"Localized"**: Apply kernel weighting K(X_i/b) in the ML loss function so that only observations near the cutoff contribute. This is closer to the theoretical optimal but requires choosing an additional tuning parameter b. They set b = h (the RD bandwidth) in practice.

### Covariates: what can/should be included

**Only pre-determined covariates.** The paper is explicit (p. 8): "The linear adjustment estimator is consistent for the RD parameter without functional form assumptions on the underlying conditional expectations if the covariates are predetermined, in the sense that they are not causally affected by the treatment, and thus their conditional expectation given the running variable varies smoothly around the cutoff."

The requirement (footnote 4, p. 7) is: "Throughout the paper, we focus on settings in which covariates are included to improve estimation efficiency and not to restore identification of the RD parameter by making the design plausible."

Z_i can be high-dimensional (d allowed to grow with n; footnote 3, p. 6).

### Estimation sample for eta-hat

The adjustment function is estimated on the **full sample** via cross-fitting (not a sample restricted to observations away from the cutoff). However, the "localized" version of ML estimation effectively uses only observations near the cutoff (via kernel weighting). The paper notes (p. 4): "the function g-hat can be estimated on the full sample (not just near the cutoff), so convergence rates for g-hat can be slow without affecting RD inference."

For the "global" implementation, the treatment indicator T_i is included as a feature, so the ML model learns the jump at the cutoff and all observations contribute.

### Theoretical properties

#### The robustness property (why misspecification is OK)

This is the paper's key theoretical contribution. The moment condition (eq. 3.2, p. 9) is:

> tau = E[M_i(eta) | X_i = 0^+] - E[M_i(eta) | X_i = 0^-] for ALL eta.

The RD parameter tau is identified by the jump in E[Y_i - eta(Z_i) | X_i = x] at x = 0 **for any function eta**, as long as E[eta(Z_i) | X_i = x] is smooth around the cutoff (which holds if covariates are predetermined). This means:

- **The estimator is consistent for any eta.** Misspecifying g-hat does not create bias.
- **The bias term is invariant to eta.** From Theorem 2 (p. 17): the bias B_n = B_base + o_P(1), the same as the no-covariates estimator. Covariate adjustment does not change the leading bias term.
- **Only the variance depends on eta.** V(eta) = (kappa-bar / f_X(0)) * (V[M_i(eta) | X_i = 0^+] + V[M_i(eta) | X_i = 0^-]). Better eta means lower residual variance, hence tighter CIs.

This is **stronger than Neyman orthogonality** (footnote 2, p. 3). In DML-type methods, the moment function has zero derivative w.r.t. the nuisance parameter (local insensitivity). Here, the moment function is **globally invariant** — it does not vary with eta at all. This means the convergence rate of eta-hat can be **arbitrarily slow** (Theorem 1, p. 17).

**Key quote for our empirical strategy section (p. 3):**

> "Our theory does not require that eta_0 is consistently estimated for valid inference on the RD parameter. We only require that in large samples the first-stage estimates concentrate in a mean-square sense around some deterministic function eta-bar, which could in principle be different from eta_0. The rate of this convergence can be arbitrarily slow."

**Key quote on why this works (p. 3):**

> "Our setup can allow for this kind of potential misspecification because our proposed RD estimators are highly insensitive to estimation errors in the preliminary stage. Specifically, they are constructed as sample analogues of a moment function that contains eta_0 as a nuisance function, but does not vary with it."

#### Comparison to standard covariate inclusion in rdrobust (CCFT 2019)

The conventional approach (Calonico et al. 2019, "covs" option in rdrobust) includes covariates **linearly and without kernel localization** in the local linear regression. The Noack-Olma-Rothe paper shows:

1. CCFT's linear adjustment is a **special case** of their framework (set eta(z) = z'*gamma_0 where gamma_0 is the population projection coefficient).
2. Linear adjustment has the **same bias** as no-covariates (B_base) but **lower variance**: V_lin = (kappa-bar / f_X(0)) * (V[Y_i - Z_i'*gamma_0 | X_i = 0^+] + V[Y_i - Z_i'*gamma_0 | X_i = 0^-]). Always V_lin <= V_base.
3. **Flexible adjustment can be strictly better** than linear when the true conditional expectation E[Y|X=0,Z] is nonlinear in Z. The flexible method exploits the nonlinearity that linear adjustment misses.
4. **With many covariates, linear adjustment can HURT** (Simulation II, p. 27-28): when #covariates is large relative to effective sample size, the conventional linear adjustment becomes unstable — standard errors exhibit downward bias (SE/SD ratio drops below 0.70 for 150 covariates), and coverage falls below 85%. Cross-fitted ML adjustments (especially random forests) remain stable.
5. Empirically (Section 6), across 56 specifications from 16 published papers: flexible adjustments reduced CI length by up to **30%** vs. no covariates, and up to **20%** vs. linear adjustment.

#### Conditions for precision improvement vs. harm

From Theorem 3 (p. 17-18):
- **V(eta) < V_base** (flexible adjustment beats no covariates) **if and only if** eta-bar captures *some* of the variance of eta_0(Z_i) near the cutoff. Even inconsistent estimation helps as long as it explains some outcome variance.
- **V(eta) < V_lin** (flexible adjustment beats linear) **if and only if** eta-bar is "closer" to eta_0 than the linear projection Z'*gamma_0 in L2 sense near the cutoff.
- **Covariate adjustment can never make the leading bias worse** — the bias B_base is invariant to the adjustment.
- **In finite samples, adjustment can add noise** if eta-hat is very poor. The Super Learner ensemble guards against this by including the no-adjustment option. Cross-fitting prevents overfitting from inflating variance.

#### Sharp and Fuzzy RDD

**Sharp RDD**: The main results (Theorems 1-4, Sections 2-4) are derived for sharp designs. This is our setting.

**Fuzzy RDD**: Covered in Section 5.3 (p. 21). The fuzzy extension estimates theta = tau_Y / tau_T as a ratio of two covariate-adjusted sharp RD estimators. Proposition 1 gives the asymptotic distribution. The optimal adjustment for fuzzy designs requires separate adjustment functions for Y and T, obtained by separately solving two sharp RD covariate-adjustment problems.

### Implementation for our paper

We have: sharp multi-city RDD, running variable = days from rollout, outcome = log_price, covariates include city x month FE, day-of-week, holiday indicators, listing characteristics, ~24M observations.

**Recommended procedure:**

**Step 1 — Estimate eta-hat(Z) via cross-fitting:**
- Split data into S = 5 folds.
- For each fold s, train a LASSO or random forest on data outside fold s, predicting log_price from covariates (city x month indicators, day-of-week, holiday, listing characteristics).
- **Two approaches for handling the treatment jump:**
  - *Global*: Include T_i = 1{days_from_rollout >= 0} as a feature in the ML model. Predict mu-hat^+(z) and mu-hat^-(z) from the single model by evaluating at T=1 and T=0. Set eta-hat_s(z) = (mu-hat_s^+(z) + mu-hat_s^-(z))/2.
  - *Simpler alternative*: Just predict log_price from covariates WITHOUT the running variable or treatment indicator. This yields an eta-hat that approximates the marginal E[Y|Z], which is not the theoretically optimal eta_0 but still valid and likely captures most seasonal/city variation. **This simpler approach is valid because the estimator is consistent for any eta.**
- For each i in fold s, compute: M_i = log_price_i - eta-hat_s(Z_i).

**Step 2 — Run rdrobust on adjusted outcomes:**
- Run `rdrobust(Y = M_i, X = days_from_rollout_i)` as if M_i were the original outcome.
- Use standard CCT bandwidth selection and bias-corrected robust CIs.
- No need to adjust standard errors for first-stage estimation uncertainty.

**Step 3 — For multi-cutoff (rdmulti):**
- The paper does not explicitly address multi-cutoff designs, but the procedure is compatible: compute adjusted outcomes M_i for each city-cutoff, then apply rdmulti to the adjusted data. The adjustment function can be estimated on the pooled sample (which is advantageous for ML with many city x month interactions).

**Pitfalls to watch:**
1. **The adjustment must be the SAME function on both sides of each cutoff.** Do NOT use different models for above/below the cutoff. Use the average (mu^+ + mu^-)/2 or the simpler approach of predicting from covariates only.
2. **Cross-fitting is important** — without it, overfitting can cause downward-biased standard errors (demonstrated in Simulation II). With 24M observations and moderate #covariates, this risk is low, but cross-fitting is still best practice.
3. **Repeat the procedure B times** with different random cross-fitting splits and report the median estimate (following Chernozhukov et al. 2018, Section 3.4; recommended for smaller samples but harmless for large ones). The paper uses B = 25 in their empirical analysis.
4. **Smoothness bound calibration**: When using bias-aware CIs, calibrate the smoothness bound on the adjusted outcome M_i, not the original Y_i. The Imbens and Wager (2019) rule of thumb (twice the max second derivative of a global quadratic fitted to each side) works on M_i.

### Does this subsume the Hausman-Rapson approach?

**Yes, largely.** The Hausman-Rapson (2018) augmented approach (regress Y on seasonal controls first, then run RD on residuals) is a special case of the Noack-Olma-Rothe framework where eta(Z) = Z'*gamma is estimated via OLS on seasonal dummies. The NOR framework:
- Generalizes it to nonlinear/ML adjustment functions
- Provides formal theoretical justification (the Hausman-Rapson paper is more heuristic)
- Shows that cross-fitting makes inference valid even with many covariates
- Demonstrates that flexible adjustment can do strictly better than linear

**Recommendation**: Use NOR as our primary framework. Cite Hausman-Rapson as the motivation for seasonal adjustment and note that our flexible covariate adjustment generalizes their approach with formal theoretical backing from NOR.

### Interaction with multi-cutoff estimation (rdmulti)

Not directly addressed in the paper. However, the procedure is modular:
1. Estimate eta-hat on the pooled sample across all cities (beneficial — more data for ML).
2. Compute M_i = Y_i - eta-hat(Z_i) for all observations.
3. Feed {(X_i, M_i)} into rdmulti, treating each city's rollout date as a separate cutoff.

The pooled-sample ML estimation is an advantage: city x month FE and seasonal patterns are estimated more precisely with cross-city data.

### Software

**Python (recommended for our project):**
- `DoubleML` package: `RDFlex` class in `doubleml.rdd` module. Install via `pip install doubleml` + `pip install rdrobust`. This automates cross-fitting + adjustment + rdrobust.
- Manual implementation: `sklearn` (LASSO, Random Forest) + `rdrobust` Python package. Simple loop over folds.

**R:**
- Authors' replication code uses: `xgboost` (boosted trees), `ranger` (random forest), `hdm` (post-LASSO, function `rlasso`), `SuperLearner` (ensemble weights via CV). See footnote 8, p. 14.
- No standalone CRAN package, but manual implementation is straightforward.

**Computational requirements for 24M observations:**
- LASSO/post-LASSO: fast, should handle 24M easily with sparse city x month dummies.
- Random forest: more memory-intensive. With 24M rows, may need subsampling or the "global" variant (which trains on all data but uses T_i as a feature). `ranger` is efficient.
- Cross-fitting with S = 5 means training 5 models, each on ~19.2M observations. Parallelizable.
- The empirical analysis in the paper handles up to 500M observations x covariates (Appendix C.2, p. 41) using only the localized random forest with 2-fold cross-fitting and B = 1.

### Comparison with alternatives

| Method | Approach | Validity | Efficiency | Many covariates? |
|---|---|---|---|---|
| **No covariates** (rdrobust baseline) | Local linear on Y | Valid | Baseline | N/A |
| **CCFT 2019** (rdrobust `covs` option) | Include Z linearly in local linear regression | Valid if Z predetermined | V_lin <= V_base | Breaks down: SE downward-biased, coverage drops below 85% when #covs > ~50 relative to effective n |
| **Hausman-Rapson 2018** | OLS on seasonals, RD on residuals | Valid (heuristic justification) | Like linear adjustment | Same issues as CCFT for many covariates |
| **Kreiss & Rothe 2023** | LASSO in local linear RD | Valid under sparsity | Like linear + regularization | Handles sparse high-dim but still linear |
| **Noack, Olma & Rothe 2025** | Cross-fitted ML adjustment + rdrobust on residuals | Valid for ANY eta (strongest result) | V(eta) <= V_lin when nonlinear structure exists; = V_lin when linear | **Robust**: cross-fitting + regularization prevent breakdown; ensemble includes no-adjustment option as guard |

**When is NOR strictly better?**
- When E[Y|X=0,Z] is nonlinear in Z (e.g., interactions between city and seasonal effects)
- When there are many covariates relative to effective sample size (our case: many city x month cells)
- When the researcher is uncertain about the correct functional form for adjustment

**When is NOR no better than linear?**
- When E[Y|X=0,Z] is truly linear in Z and #covariates is small relative to effective n. In this case, all methods produce the same V_lin.

### Specific quotes for our empirical strategy section

**On robustness to misspecification (p. 3):**
> "Our theory does not require that eta_0 is consistently estimated for valid inference on the RD parameter. We only require that in large samples the first-stage estimates concentrate in a mean-square sense around some deterministic function eta-bar, which could in principle be different from eta_0. The rate of this convergence can be arbitrarily slow."

**On why this works — the global invariance property (p. 3):**
> "Our proposed RD estimators are highly insensitive to estimation errors in the preliminary stage. Specifically, they are constructed as sample analogues of a moment function that contains eta_0 as a nuisance function, but does not vary with it."

**On why this is stronger than DML-type Neyman orthogonality (footnote 2, p. 3):**
> "A moment function is Neyman orthogonal if its first functional derivative with respect to the nuisance function is zero. In contrast, the (conditional) moment function on which our estimates are based is fully invariant with respect to the nuisance function."

**On practical implementation with existing software (p. 4):**
> "Practical issues like bandwidth choice and construction of confidence intervals can be addressed in a straightforward manner. Specifically, we show that standard methods remain valid if they are applied to a data set in which the outcome Y_i is replaced with the generated outcome Y_i - eta-hat(Z_i) and one ignores that eta-hat has been estimated."

**On the scope of efficiency gains (p. 4):**
> "Including covariates in the RD regression does not meaningfully reduce the length of the confidence intervals in about half of the specifications [...] but our proposed flexible adjustments also achieve a reduction of more than 30% in one setting. To put this into perspective, obtaining this reduction would require roughly increasing the sample size by a factor of 2.4 if the covariates were not used."

**On choosing between LASSO and RF:** The paper does not give explicit guidance on LASSO vs. RF. Their recommended implementation is the **Super Learner ensemble** that includes both (plus boosted trees and linear regression, each in localized and global versions). The ensemble automatically selects the best combination via cross-validation. In their Simulation II (p. 27-28), random forests are notably more stable than linear methods as the number of covariates grows.

### Key theorems (reference list)

- **Theorem 1** (p. 17): Asymptotic equivalence — the feasible estimator (with estimated eta-hat) is asymptotically equivalent to the infeasible oracle (with deterministic eta-bar), regardless of convergence rate.
- **Theorem 2** (p. 17): Asymptotic normality — sqrt(nh) * V(eta-bar)^{-1/2} * (tau-hat - tau - h^2 * B_n) -> N(0,1). Bias = B_base (same as no covariates). Variance = V(eta-bar) (depends on quality of adjustment).
- **Theorem 3** (p. 17-18): Optimal adjustment — V(eta) is minimized at eta = eta_0. Characterizes when V(eta^(a)) < V(eta^(b)) in terms of L2 distance to eta_0.
- **Theorem 4** (p. 18): AMSE-optimal bandwidth — better adjustment reduces variance, which also reduces optimal bandwidth and AMSE. The AMSE ratio scales as (v(eta^(a))/v(eta^(b)))^{4/5}.
- **Proposition 1** (p. 21): Fuzzy RD extension — same framework works for ratio estimator theta = tau_Y/tau_T with separate adjustments for Y and T.
