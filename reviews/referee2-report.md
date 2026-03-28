# Referee 2 Report: Identification Strategy Critique
**Date**: 2026-03-22
**Source**: Claude deep analysis of the fuzzy RDD/IV design
**Severity**: Major — requires substantial revisions to core identification

---

## Overall Assessment

The referee identifies **eight methodological concerns**, of which three are existential threats to the current design. The critique is rigorous, well-cited, and closely tracks what a top-journal IO referee would write.

---

## Concern 1: WRONG ENDOGENOUS VARIABLE [EXISTENTIAL]

**Problem**: The endogenous variable `available` measures calendar openness, NOT Smart Pricing adoption. The fuzzy RDD requires the endogenous variable to be the actual treatment (Hahn, Todd & Van der Klaauw 2001). Using `available` produces a Wald ratio with no economic interpretation.

**Referee's recommendation**: Either (a) replace with actual Smart Pricing adoption, or (b) abandon fuzzy RDD and present the sharp RDD/ITT reduced form as the primary result.

**Our response options**:
- **Option A (preferred)**: Reframe the paper around the ITT reduced form. The reduced form estimates the effect of Smart Pricing *availability* on prices, which is policy-relevant and avoids the endogenous variable problem entirely. Present this as the primary result.
- **Option B**: Construct a proxy for Smart Pricing adoption using the Assad et al. (2024) structural break methodology on pricing behavior markers. Use this as the endogenous variable. This requires significant new analysis.
- **Option C**: Frame `available` as a measure of "algorithm exposure environment" (weaker but defensible). Acknowledge the proxy limitation prominently.

**Priority**: P0 — must resolve before any other revision.

---

## Concern 2: FIRST-STAGE F-STATISTICS SIGNAL SEASONALITY [EXISTENTIAL]

**Problem**: F-statistics of 4,158–13,906 are implausible for a genuine causal first stage. They likely reflect seasonal covariation between time and calendar availability, especially since rollout dates fall at the fall-to-winter transition. The pattern of *increasing* F with wider bandwidth further suggests seasonal dominance.

**Referee's recommendation**: Implement Hausman & Rapson (2018) augmented local linear approach — regress on seasonal controls first, then run RDD on residuals. Show McCrary density test and covariate balance.

**Our response**:
- Add city × month-of-year FE, day-of-week FE, holiday indicators as controls
- Run donut-hole RDD excluding ±1–2 weeks around cutoff
- Run placebo cutoff tests at same calendar date in prior/subsequent years
- Show event-study specification with pre-trends
- If switching to ITT: first-stage issue becomes moot

**Priority**: P0 — entangled with Concern 1.

---

## Concern 3: EXCLUSION RESTRICTION HAS 6+ VIOLATION CHANNELS [SERIOUS]

**Problem**: The instrument (post-cutoff) may affect prices through: (1) information/attention effects from marketing, (2) bundled platform changes, (3) competitor pricing tool growth, (4) platform growth trends, (5) anticipation effects, (6) seasonal price dynamics.

**Referee's recommendation**: Acknowledge limitations. Use Conley, Hansen & Rossi (2012) sensitivity analysis under plausible exclusion restriction violations.

**Our response**:
- Under ITT framing: exclusion restriction is not required (no first stage). This is a major advantage of switching frameworks.
- For the reduced form: the identification assumption is much weaker — only that potential outcomes are smooth through the cutoff.
- Add placebo outcomes (reviews, response rate) to test whether the cutoff affects non-price dimensions
- Add leave-one-city-out analysis to test robustness to any single city's rollout

**Priority**: P1 — mostly resolved by switching to ITT.

---

## Concern 4: LATE IDENTIFIES MEANINGLESS COMPLIER POPULATION [SERIOUS]

**Problem**: The "compliers" are hosts whose calendar availability changed at the cutoff — not Smart Pricing adopters. No economic interpretation.

**Our response**: Fully addressed by switching to ITT. Under the ITT framework, we estimate the effect on all hosts, not a complier subpopulation.

**Priority**: Resolved by Option A.

---

## Concern 5: SEASONAL CONFOUNDING [SERIOUS]

**Problem**: Nov/Dec 2015 rollout coincides with fall-to-winter seasonal transition across all 8 cities.

**Our response**:
- Hausman & Rapson (2018) augmented approach
- Show that rollout dates are NOT all in the same seasonal window (verify city-by-city timing)
- Year-over-year comparison: run same specification at the same calendar date in 2014 and 2016
- Add within-year seasonal controls (month × city FE)

**Priority**: P1.

---

## Concern 6: ML INTERACTION IS LIKELY SPURIOUS [SERIOUS]

**Problem**: t = 264 is implausibly large. Three issues: (1) uncorrected generated-regressor bias (Pagan 1984; Murphy & Topel 1985), (2) selection masquerading as heterogeneity (high-propensity hosts already price dynamically), (3) no sample splitting (Chernozhukov et al. 2018 requires cross-fitting).

**Referee's recommendation**: If retained: (a) cross-fitting, (b) Murphy-Topel SE corrections or full bootstrap, (c) pre-trend tests for high-propensity hosts, (d) consider instrumental forests (Athey, Tibshirani & Wager 2019).

**Our response**:
- Implement cross-fitting following Chernozhukov et al. (2018)
- Bootstrap the two-step procedure for correct SEs
- Add pre-trend test: do high-propensity hosts show differential price trends pre-rollout?
- Reposition ML extension as **descriptive heterogeneity analysis** (per Session 1 recommendation), not causal
- Consider replacing with causal forest / generalized random forest (Athey, Tibshirani & Wager 2019)

**Priority**: P1.

---

## Concern 7: REDUCED FORM TELLS THE WHOLE STORY [CONSTRUCTIVE]

**Problem**: The reduced form is null. The IV apparatus adds nothing.

**Referee's view**: "This null finding is itself informative and potentially publishable as a well-identified ITT result, provided the seasonal confounding concerns are addressed."

**Our response**: This is actually supportive. The referee is saying the paper has a publishable result — it just needs to be framed honestly. The reduced form null + the variance finding + the heterogeneity analysis = a complete paper without the fuzzy RDD.

**Priority**: P0 — this IS the path forward.

---

## Concern 8: WHAT A CREDIBLE VERSION REQUIRES [CONSTRUCTIVE]

The referee provides a detailed requirements list:

### Essential (must-do)
- [ ] Replace endogenous variable or switch to ITT/reduced form
- [ ] Multi-cutoff RDD via Cattaneo, Keele, Titiunik & Vazquez-Bare (2016, 2021) `rdmulti` package
- [ ] Seasonal controls: city × month FE, day-of-week, holidays
- [ ] McCrary/CJM density test
- [ ] Covariate balance at cutoff
- [ ] Placebo cutoff tests (false dates, prior years)
- [ ] Donut hole RDD (±1–2 weeks)
- [ ] Bandwidth sensitivity with CCT/bias-corrected CIs
- [ ] Event-study pre-trends

### For ML interaction (if retained)
- [ ] Cross-fitting (Chernozhukov et al. 2018)
- [ ] Murphy-Topel SEs or bootstrap
- [ ] Pre-trend tests for high-propensity hosts
- [ ] Consider instrumental forests as alternative

### Alternative strategies to consider
- [ ] Staggered DiD (Callaway & Sant'Anna 2021)
- [ ] Propensity score matching of adopters vs non-adopters
- [ ] Structural demand estimation following Huang (2025)

---

## Strategic Recommendation

**Reframe the paper around three pillars:**

1. **ITT reduced form** (sharp RDD): Smart Pricing availability → null effect on price levels. This is clean, defensible, and policy-relevant ("ruling out collusion above X%").

2. **Variance analysis**: Smart Pricing availability → increased price variance. This is the positive finding. Needs the seasonal controls and donut-hole tests, but is much less vulnerable to the endogenous variable critique.

3. **Descriptive heterogeneity** (repositioned ML): Effects concentrate among sophisticated hosts. Frame as descriptive pattern, not causal. Use cross-fitting for valid inference. Support with the formal model (supermodularity in technology × skill).

This tripartite structure matches the Session 1 recommendation (promote variance, demote ML to supplementary). The referee critique confirms this is the right direction.
