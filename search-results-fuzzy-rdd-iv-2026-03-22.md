## Paper Search Results: Fuzzy RDD / IV Methods in Platform Economics
**Date**: 2026-03-22
**Query**: "fuzzy regression discontinuity instrumental variables platform" (2020–2026)
**JEL codes**: C21, C26, C31
**Sources checked**: Semantic Scholar, Google Scholar, NBER

---

### Tier 1: High-priority reads (methodological precedents)

| # | Authors | Year | Title | Venue | Citations | Relevance |
|---|---------|------|-------|-------|-----------|-----------|
| 1 | Noack & Rothe | 2024 | Bias-Aware Inference in Fuzzy Regression Discontinuity Designs | Econometrica | — | **Must cite**: state-of-the-art fuzzy RDD inference; bias-corrected CIs |
| 2 | Cattaneo & Titiunik | 2022 | Regression Discontinuity Designs | Annual Rev. Economics | — | **Definitive survey**: cite for methodological foundation |
| 3 | Lee & Suk | 2025 | Evidence Factors in Fuzzy RDD with Sequential Treatment Assignments | Psychometrika | 0 | Novel framework for multiple IVs in fuzzy RDD — relevant to your multi-cutoff design |
| 4 | Black, Joo, LaLonde, Smith & Taylor | 2022 | Simple Tests for Selection: Learning More from Instrumental Variables | SSRN | 21 | Tests for selection on unobservables in LATE/fuzzy RDD framework |
| 5 | Lee, Tan & Karmakar | 2024 | Constructing Multiple Independent Analyses in the RDD with Multiple Cutoffs | Observational Studies | 0 | Multiple cutoffs → multiple IVs; directly relevant to your multicity design |

### Tier 2: Important methodological background

| # | Authors | Year | Title | Venue | Citations | Relevance |
|---|---------|------|-------|-------|-----------|-----------|
| 6 | Calonico, Cattaneo & Titiunik | 2014 | Robust Nonparametric CI in RD Designs | Econometrica | — | Already in your references; CCT bandwidth |
| 7 | Cattaneo, Jansson & Ma | 2020 | Simple Local Polynomial Density Estimators | JASA | — | McCrary-style density test; must run for your RDD |
| 8 | Xie | 2022 | Nonlinear and Nonseparable Structural Functions in Fuzzy RDD | Working paper | 0 | Fuzzy RDD with continuous treatment — relevant if you frame `available` as continuous |
| 9 | Leventer & Nevo | 2024 | Correcting Invalid RD Designs with Multiple Time Period Data | Working paper | 0 | Multiple time periods to fix continuity violations — relevant for your panel |
| 10 | Chib, Greenberg & Simoni | 2022 | Nonparametric Bayes Analysis of Sharp and Fuzzy RDD | Econometric Theory | 13 | Bayesian fuzzy RDD with covariates; potential robustness check |
| 11 | Han | 2024 | Mining Causality: AI-Assisted Search for Instrumental Variables | Working paper | 9 | LLM-based IV search; could cite for context on AI in causal inference |

### Tier 3: Fuzzy RDD applications (methodological templates)

| # | Authors | Year | Title | Venue | Citations | Setting |
|---|---------|------|-------|-------|-----------|---------|
| 12 | Huang & Zhan | 2023 | Does Health Behavior Change After Diagnosis? Evidence from Fuzzy RDD | J. Econometric Methods | 0 | Anderson-Rubin test in fuzzy RDD; robust to weak ID |
| 13 | Adeleke, Baio & O'Keeffe | 2023 | Risk Ratio Estimation in Fuzzy RDD | Stat. Methods Med. Res. | 2 | Fuzzy RDD with binary outcome |
| 14 | Adeleke, Baio & O'Keeffe | 2022 | RDD for Time-to-Event Outcomes: AFT Models | JRSS-A | 6 | Fuzzy RDD extensions |

---

### Key insights for your paper

1. **Noack & Rothe (2024, Econometrica)** is the current frontier for fuzzy RDD inference. Their bias-aware confidence intervals should be your primary inference procedure (alongside CCT). Referees will expect you to cite this.

2. **Lee, Tan & Karmakar (2024)** on multiple cutoffs in RDD is highly relevant — your multicity design with city-specific rollout dates creates exactly this structure. Their IV construction from multiple cutoffs could strengthen your overidentification argument.

3. **Black et al. (2022)** provide tests for selection on unobservables in the LATE framework. Running their tests on your complier population would address a key referee concern about who the compliers are in your fuzzy RDD.

4. **Leventer & Nevo (2024)** address continuity violations in RDD using multiple time periods — directly relevant if referees challenge your continuity assumption with seasonality concerns.

5. **Platform-specific fuzzy RDD applications are virtually absent** in the literature. Your paper would be among the first to apply fuzzy RDD to study a platform pricing algorithm rollout, making this a genuine methodological contribution to the platform economics literature.

### Suggested next steps
- [ ] /read-paper Noack & Rothe (2024) — critical for inference procedure
- [ ] /read-paper Lee, Tan & Karmakar (2024) — multiple cutoffs framework
- [ ] Check if Black et al. (2022) tests are implementable with your data
- [ ] Consider citing Leventer & Nevo (2024) for multi-period RDD context
