## Research Plan: Algorithmic Pricing and Price Discrimination — Evidence from Airbnb Smart Pricing

**Date**: 2026-03-22 (revised)
**Revision**: v2.0 — Major pivot from fuzzy RDD/IV to ITT reduced form
**Target output**: Journal paper (major rewrite of existing working paper)
**Timeline**: 4 weeks

---

### PIVOT RATIONALE

External research convergence (Gemini literature sweep, ChatGPT fact-check, Claude Referee 2 critique, Claude cognitive constraint analysis) identified three existential flaws in the original fuzzy RDD/IV design:

1. **Wrong endogenous variable**: `available` measures calendar openness, not Smart Pricing adoption. The Wald ratio has no economic interpretation (Hahn, Todd & Van der Klaauw 2001).
2. **Mechanical first stage**: F-statistics of 4,158–13,906 reflect seasonal covariation, not instrument strength. Increasing F with bandwidth is diagnostic of seasonality, not causality.
3. **Exclusion restriction failure**: 6+ violation channels (information effects, bundled changes, competitor tools, platform growth, anticipation, seasonality).

The Referee 2 critique confirms: "This null finding is itself informative and potentially publishable as a well-identified ITT result." The reduced form null + variance finding + descriptive heterogeneity = a complete, defensible paper.

**Decision**: Abandon fuzzy RDD. Switch to sharp reduced-form / ITT as primary identification.

---

### 1. Research question

**Revised**: Does the rollout timing of Airbnb's Smart Pricing algorithm predict local changes in price levels or price discrimination patterns across major U.S. markets?

**Sub-questions**:
1. Can we rule out economically meaningful aggregate price-level effects at the market level? (Bounds on the null)
2. Does algorithm availability increase price *variance* and temporal *dispersion*, consistent with enhanced price discrimination rather than coordination?
3. Where do algorithm-linked pricing changes concentrate, and is the pattern consistent with technology-skill complementarity?

### 2. Proposed answer / hypothesis

We expect to confirm a precisely estimated null on aggregate price levels, ruling out market-wide collusion effects above ~3% (95% CI). The algorithm's primary footprint is increased temporal price variance — consistent with dynamic yield management and intertemporal price discrimination rather than tacit coordination. Effects concentrate among hosts with high pre-existing pricing sophistication, consistent with the technology-skill complementarity framework (Autor, Levy & Murnane 2003): the algorithm complements nonroutine strategic pricing knowledge while substituting for routine monitoring tasks, with the specific mechanism being relaxation of rational inattention constraints (Maćkowiak & Wiederholt 2009).

### 3. Identification strategy

**REVISED DESIGN**: Multicity sharp reduced-form RDD with variance analysis and ML-heterogeneity extension

#### Primary specification: ITT reduced form (sharp RDD)

- **Estimand**: Intent-to-treat effect of Smart Pricing *availability* on listing prices
- **Equation**: `log_price_it = α + τ · post_cutoff_ct + f(running_var_ct) + X_it'β + γ_c + δ_dow + η_holiday + ε_it`
- **Key variation**: City-specific Smart Pricing rollout timing creates quasi-experimental variation in algorithm exposure. `post_cutoff` is the treatment indicator — whether the listing-date observation falls after the city's rollout.
- **Key assumption**: Smoothness — potential outcomes `E[Y(0)|X=x]` are continuous through the cutoff, conditional on seasonal controls and city FE. This is substantially weaker than the exclusion restriction required by the prior fuzzy RDD.
- **Identifying variation**: Cross-city differences in rollout timing allow for multi-cutoff estimation (Cattaneo, Keele, Titiunik & Vazquez-Bare 2021), with city-specific and pooled estimates.
- **Why ITT, not LATE**: Smart Pricing adoption is unobserved in the data. The ITT estimates the policy-relevant parameter: what happens to market prices when the platform makes an algorithmic pricing tool available? This directly answers the antitrust question without requiring adoption data.

#### Secondary specification: Price variance / dispersion analysis

- **Estimand**: Effect of Smart Pricing availability on within-listing temporal price variance
- **Equation**: `var(log_price)_it_window = α + τ · post_cutoff_ct + f(running_var) + X_i'β + γ_c + ε_it`
- **Variance decomposition**: Separate systematic variance (predicted by demand factors: day-of-week, seasonality, events) from residual variance. Show the increase is in systematic, demand-responsive pricing, not noise.
- **Rationale**: Under linear demand, optimal discriminatory prices have the same weighted average as the optimal uniform price (Hazledine 2006), but higher variance. An algorithm enabling finer time segmentation increases variance without changing the mean — explaining both the null on levels and the positive variance finding.

#### Supplementary: Descriptive ML heterogeneity (repositioned)

- **Estimand**: Descriptive pattern of where pricing changes concentrate across host types
- **Method**: Cross-fitted latent sophistication proxy (Chernozhukov et al. 2018) with bootstrap SEs (Murphy & Topel 1985 correction)
- **Framing**: "Where do effects concentrate?" — explicitly descriptive, not causal. Supported by formal model predictions (supermodularity of algorithm × sophistication).
- **Validation**: Pre-trend test for high-propensity hosts; if differential pre-trends exist, this is selection, not treatment effect heterogeneity.

#### DROPPED from primary specification

- ~~Fuzzy first stage: `available` regressed on `post_cutoff`~~ — moved to appendix with full caveats
- ~~Wald ratio / LATE interpretation~~ — abandoned due to endogenous variable misspecification
- ~~First-stage F-statistics as evidence of instrument strength~~ — acknowledged as seasonal artifact

#### Robustness and diagnostics battery

1. **Seasonal controls**: Hausman & Rapson (2018) augmented local linear approach — city × month-of-year FE, day-of-week FE, holiday indicators
2. **CCT bandwidth**: Calonico, Cattaneo & Titiunik (2014) MSE-optimal selection + bias-corrected CIs via `rdrobust` Python v1.3.0; Noack & Rothe (2024, Econometrica) bias-aware inference
3. **Multi-cutoff**: `rdmulti` package for city-specific + pooled estimates
4. **McCrary/CJM density test**: Cattaneo, Jansson & Ma (2020) at each city cutoff
5. **Covariate balance**: Listing characteristics tested at cutoff
6. **Placebo cutoffs**: Same calendar dates in 2014 and 2016
7. **Donut-hole RDD**: Excluding ±7 and ±14 days around cutoff
8. **Placebo outcomes**: Number of reviews, host response rate, minimum nights
9. **Leave-one-city-out**: Drop each city in turn
10. **Event-study specification**: Weekly/bi-weekly coefficients around cutoff; primary graphical evidence
11. **Alternative estimator**: Callaway & Sant'Anna (2021) staggered DiD exploiting cross-city timing via `csa-py` or `differences` Python packages
12. **Power analysis**: Monte Carlo MDE at 80% power for each bandwidth — quantifies the "informative null"
13. **Alternative clustering**: City-date, city, neighborhood levels

### 4. Data requirements

- **Unit of observation**: Listing × date (listing-step)
- **Time period needed**: Symmetric ±1m, ±2m, ±3m windows around city-specific rollout dates
- **Key variables (revised)**:
  - `log_price` — primary outcome (forward-looking posted calendar price, not transaction price; disclose)
  - `post_cutoff` — treatment indicator (city-specific)
  - `running_var` — days from city-specific rollout date
  - Listing characteristics — pre-determined covariates for balance tests
  - `price_variance` — within-listing temporal variance (secondary outcome)
  - `latent_proxy` — ML-constructed sophistication proxy (supplementary; cross-fitted)
  - `occupancy_proxy` — from calendar blocked dates (diagnostic; acknowledge booked ≠ blocked)
- **DROPPED from key variables**: ~~`available` as endogenous variable~~
- **Existing datasets**: Inside Airbnb multicity panel — Austin, Boston, Chicago, LA, NYC, SF, Seattle, DC
  - Step 2 panel: `data/processed/step2/fact_listing_day_multicity_bw_3m.csv.gz` (24.2M obs)
  - Step 4 estimates: `data/processed/step4/`
  - ML extension: `data/processed/ml_extension/`
  - Panel extension: `data/processed/panel_extension/`
- **Data gaps to resolve**:
  - City-specific rollout dates — **reframe as estimated from structural breaks in data** (no official schedule exists per fact-check). Validate via contemporaneous media coverage.
  - Calendar prices are forward-looking *posted* prices, not realized transactions (Inside Airbnb Data Assumptions page). Disclose prominently.
  - Calendar `available` does not distinguish booked from host-blocked (Alsudais 2021). Affects occupancy proxy.
  - Price Tips launched June 2015, 5 months before Smart Pricing — discuss potential treatment contamination.
  - Inside Airbnb scraping cadence varies by city (quarterly public, sometimes monthly); document vintage used.

### 5. Literature positioning (revised)

**Strand 1: Algorithmic Collusion — Theory and Evidence**
- Calvano, Calzolari, Denicolò & Pastorello (2020, AER) — Q-learning agents learn to collude
- Lambin (2024, ESSEC WP) — *Critique*: learning inertia, not genuine punishment strategies
- Brown & MacKay (2025, NBER W34070) — Algorithmic coercion via speed + commitment
- Assad, Clark, Ershov & Xu (2024, JPE) — German gasoline: +28% margins in duopoly with mutual adoption
- Musolff (2022, EC) — E-commerce repricing: RDD shows Edgeworth cycles
- Bichler, Deng & Schiffer (2025, BISE) — **Survey**: comprehensive review of theory + empirics
- Bichler, Durmann & Oberlechner (2024) — Skeptical view: most algorithms converge to NE
- Fish et al. (2024) — LLM pricing agents collude without instruction
- Hartline, Long & Zhang (2024) — Auditable non-collusion definition
- Werner (2026) — Algorithms more collusive than humans in lab
- Harrington (2026, JIE forthcoming) — Hub-and-spoke with many small firms

**Strand 2: Airbnb and Platform Pricing**
- Foroughifar & Mehta (2024, SSRN) — **Direct competitor**: Smart Pricing deployment challenges; paradox of adoption
- Huang (2021/2025, SSRN) — Pricing frictions on Airbnb; algorithm increases surplus
- Zhang, Mehta, Singh & Srinivasan (2025, Marketing Science) — Racial revenue gap; differential adoption
- Ye et al. (2018, KDD) — Airbnb's own Smart Pricing system description
- Casamatta et al. (2021) — Professional vs. non-professional host pricing
- Piao (2023/2025) — Airbnb RDD with ML clustering (closest direct competitor)
- Calder-Wang & Kim (2024, JPE forthcoming) — **Key contrast**: RealPage multifamily rentals

**Strand 3: Technology-Skill Complementarity (new theoretical anchor)**
- Autor, Levy & Murnane (2003, QJE) — Canonical task framework: routine substitution, nonroutine complementarity
- Bresnahan, Brynjolfsson & Hitt (2002, QJE) — IT × skill × organization three-way complementarity
- Garicano & Rossi-Hansberg (2006, QJE) — Communication-cost-reducing tech benefits high-ability agents
- Brynjolfsson, Li & Raymond (2025, QJE) — **Contrast**: AI helps *low-skill* workers in customer service
- Garcia, Tolvanen & Wagner (2024, Management Science) — Cognitive frictions in hotel pricing
- Maćkowiak & Wiederholt (2009, AER) — Rational inattention in price-setting
- Maćkowiak, Matějka & Wiederholt (2023, JEL) — Rational inattention review

**Strand 4: Methodology — Sharp RDD, Variance Analysis, ML Heterogeneity**
- Hausman & Rapson (2018) — **Critical**: Regression discontinuity in time; seasonal confounding
- Calonico, Cattaneo & Titiunik (2014, Econometrica) — Robust RD confidence intervals
- Noack & Rothe (2024, Econometrica) — Bias-aware fuzzy RDD inference
- Cattaneo, Jansson & Ma (2020, JASA) — RD density tests
- Cattaneo, Keele, Titiunik & Vazquez-Bare (2021) — Multi-cutoff RDD
- Chernozhukov et al. (2018, Econometrics Journal) — Double/debiased ML
- Callaway & Sant'Anna (2021, J. Econometrics) — Staggered DiD
- Lee, Tan & Karmakar (2024) — Multiple cutoffs → multiple IVs
- Black et al. (2022) — Selection tests in LATE framework

**Strand 5: Antitrust and Regulatory Context**
- DOJ v. RealPage (filed Aug 2024; amended Jan 2025; settled Nov 2025; Federal Register Jan 2026)
- FTC surveillance pricing study (6(b) orders July 2024; interim findings Jan 2025)
- EU DMA (effective May 2023; gatekeeper compliance March 2024)
- EU Commission proceedings against Airbnb/Booking.com (Jan 2026 — data-sharing compliance, not pricing)
- Harrington (2024–2025) — Hub-and-spoke vs. parallel adoption empirical tests

**Marginal contribution (revised)**: First multicity quasi-experimental study of a major platform's pricing algorithm providing (a) precise bounds on the aggregate null effect of algorithm availability on price levels, (b) novel evidence that the algorithm's footprint is temporal price dispersion (discrimination), not price-level inflation (collusion), and (c) descriptive evidence that pricing changes concentrate among sophisticated hosts, consistent with technology-skill complementarity — shifting the policy debate from "does it cause collusion?" to "does it enable targeted price discrimination, and for whom?"

### 6. Target journals (updated)

| Journal | Fit | Rationale |
|---------|-----|-----------|
| **RAND Journal of Economics** | Primary target | IO focus; values well-identified reduced-form evidence with policy relevance. "Informative null + discrimination mechanism" framing fits editorial preference. Has published precise-null papers. Recent algorithmic pricing content. |
| **AEJ: Microeconomics** | Strong alternative | Shorter format suits the focused ITT + variance + heterogeneity structure. Values clean reduced-form designs. The discrimination mechanism angle is a good fit. |
| **Journal of Industrial Economics** | Solid fallback | Traditional IO outlet. More receptive to comprehensive market-conduct studies. Would appreciate the regulatory context framing. Faster turnaround. |
| **Marketing Science** | New consideration | The technology-skill complementarity angle and platform pricing framing fit well. Zhang et al. (2025) published here on a closely related Airbnb topic. Slightly less emphasis on identification rigor, more on managerial relevance. Consider if RAND/AEJ desk-rejects. |

**Note**: Target journal ranking unchanged from v1, but Marketing Science added as fallback given the new framing's emphasis on platform pricing and host heterogeneity. The discrimination mechanism + technology-skill complementarity story has marketing appeal.

### 7. Task breakdown (revised — incorporates P0 critical path)

| Week | Task | Deliverable | Priority | New vs. Revised |
|------|------|-------------|----------|-----------------|
| **1** | **Literature & framing** | | | |
| 1.1 | ~~Deep literature search~~ ✅ | Reading list (32 papers) | — | Done |
| 1.2 | ~~External research reviews~~ ✅ | Fact-check, referee report, action list | — | Done |
| 1.3 | Read and distill Tier 1 papers (5 papers) | Paper snapshots in `./literature/` | P1 | New |
| 1.4 | Synthesize lit review positioning | `./synthesis/lit-review.md`, debate map, gap analysis | P1 | New |
| 1.5 | Decide on final title and abstract structure | Title + abstract draft | P1 | Revised |
| **2** | **Identification overhaul (P0 critical path)** | | | |
| 2.1 | **Switch to ITT reduced form** — re-estimate `log_price` on `post_cutoff` with seasonal controls | Primary results table | **P0** | New |
| 2.2 | **Hausman-Rapson seasonal controls** — city × month FE, DOW FE, holiday indicators; augmented local linear | Specification comparison table | **P0** | New |
| 2.3 | **Full RDD diagnostics** — McCrary density, covariate balance, CCT bandwidth, donut-hole, bandwidth sensitivity | Diagnostics appendix | **P0** | New |
| 2.4 | **Multi-cutoff estimation** via `rdmulti` — city-specific + pooled | Multi-cutoff table + figure | **P0** | New |
| 2.5 | **Event-study plot** — weekly coefficients around cutoff | Primary graphical evidence (Figure 1) | P1 | New |
| 2.6 | **Placebo cutoffs** — same dates in 2014 and 2016 | Placebo table | P1 | New |
| 2.7 | **Placebo outcomes** — reviews, response rate, minimum nights | Placebo outcomes table | P1 | New |
| 2.8 | **Leave-one-city-out** | Robustness table | P1 | New |
| 2.9 | **Variance analysis** — within-listing temporal price variance as outcome | Variance results table | P1 | New (promoted) |
| 2.10 | **Variance decomposition** — systematic vs. residual | Mechanism table | P1 | New |
| 2.11 | **Power analysis / MDE** — Monte Carlo at 80% power | Power curve figure | P2 | New |
| **2–3** | **ML interaction fix** | | | |
| 2.12 | Implement cross-fitting (K=5 fold) for latent proxy | Cross-fitted proxy | P1 | New |
| 2.13 | Bootstrap two-step SEs (Murphy-Topel correction) | Corrected SE table | P1 | New |
| 2.14 | Pre-trend test for high-propensity hosts | Pre-trend figure | P1 | New |
| 2.15 | Occupancy proxy diagnostic | Mechanism test table | P2 | New |
| 2.16 | Construct Assad et al. pricing sophistication proxy | Alternative treatment proxy | P2 | New |
| 2.17 | Staggered DiD (Callaway-Sant'Anna) as alternative estimator | Alternative results table | P2 | New |
| 2.18 | Alternative clustering (city-date, city, neighborhood) | Robustness table | P2 | New |
| **3** | **Writing (full rewrite)** | | | |
| 3.1 | Draft Introduction (Head formula) — lead with bound on null | `./drafts/introduction.md` | P1 | Rewritten |
| 3.2 | Draft Empirical Strategy — clean ITT framework | `./drafts/empirical-strategy.md` | P1 | Rewritten |
| 3.3 | Draft Results — null levels → variance → heterogeneity | `./drafts/results.md` | P1 | Rewritten |
| 3.4 | Draft Related Work — position vs Assad, Musolff, Foroughifar, Calder-Wang | `./drafts/related-work.md` | P1 | Rewritten |
| 3.5 | Draft Conclusion — policy (ruling out >3%; discrimination; DMA/DOJ) | `./drafts/conclusion.md` | P1 | Rewritten |
| 3.6 | Formal model (4–6 page appendix) — monopolistic competition, 4 propositions | `./drafts/model.md` | P2 | New |
| 3.7 | Fix institutional claims per fact-check log | All sections | P1 | Revised |
| 3.8 | Publication-quality tables and figures | `.tex` + `.md` + `.png` | P2 | Revised |
| **4** | **Review & verify** | | | |
| 4.1 | Self-review all sections (`/self-review`) | Revised drafts | P2 | New |
| 4.2 | Adversarial verification (`/verify`) — math, citations, code-output | Verification report | P2 | New |
| 4.3 | Cross-verify with Gemini/ChatGPT | Cross-check report | P3 | New |
| 4.4 | Compile full draft (Quarto → PDF) | `_book/` output | P2 | New |
| 4.5 | Final pass and submission prep | Clean PDF + cover letter | P2 | New |

### 8. Risk register (revised)

| Risk | Probability | Mitigation |
|------|-------------|------------|
| **Seasonal confounding in ITT** | High | (1) Hausman & Rapson augmented approach; (2) placebo cutoffs at same dates ±1 year; (3) event-study showing flat pre-trends; (4) cross-city timing variation provides multiple seasonal windows |
| **Straw-man objection** ("testing collusion, finding nothing") | Medium | (1) Frame as "market conduct" not "collusion test"; (2) variance result is a *positive* finding; (3) cite policy relevance (DOJ RealPage, FTC surveillance pricing, EU DMA); (4) explain why null is structurally predicted (many sellers, differentiation, atomistic) |
| **ML interaction seen as spurious** (t=264) | High → Medium | (1) Cross-fitting eliminates overfitting; (2) bootstrap SEs correct generated-regressor bias; (3) pre-trend test separates selection from treatment effect; (4) reposition as descriptive, not causal |
| **Foroughifar & Mehta (2024) scoops the finding** | Medium | (1) Read immediately and differentiate; (2) their focus appears to be deployment *challenges*, not market conduct → complementary papers; (3) your multicity design + variance analysis is distinct |
| **Revenue management alternative explains everything** | Medium | (1) Occupancy proxy test: RM predicts occupancy ↑, cognitive constraint predicts occupancy →; (2) cite Zhang et al. (2021): ADR fell 5.7% but revenue rose 8.6%; (3) acknowledge as complementary, not contradictory |
| **Calendar price ≠ transaction price** | Medium | (1) Disclose prominently (Inside Airbnb Data Assumptions); (2) cite Alsudais (2021); (3) diagnostic: is variance increase driven by extreme tails or reasonable demand-responsive variation? |
| **Null result → desk rejection** | Low | (1) Target RAND/AEJ:Micro which value precise nulls; (2) variance result and heterogeneity analysis are positive findings; (3) power analysis shows MDE — "we can rule out effects above X%" |
| **No official city-specific rollout dates** | High | (1) Estimate from structural breaks following Assad et al. (2024); (2) validate against Nov 12, 2015 announcement date; (3) robustness to alternative cutoff dates |

### 9. Key framing decisions (RESOLVED)

1. **Title**: "Algorithmic Pricing and Market Conduct: Evidence from Airbnb Smart Pricing"
   - Alternative: "Does Algorithmic Pricing Enable Price Discrimination? Evidence from Airbnb"

2. **Abstract lead**: Start with the bound on the null. *"We study the rollout of Airbnb's Smart Pricing algorithm across eight major U.S. cities. Using a sharp reduced-form RDD exploiting city-specific rollout timing, we can rule out aggregate price-level increases above 3% (95% CI). Instead, the algorithm's primary footprint is increased temporal price dispersion, consistent with enhanced intertemporal price discrimination. Effects concentrate among hosts with high pre-existing pricing sophistication, consistent with technology-skill complementarity."*

3. **Identification framework**: Sharp reduced-form / ITT as primary. Fuzzy RDD in appendix only. Staggered DiD as robustness.

4. **ML extension placement**: Section 5 ("Where Do Effects Concentrate?") — explicitly descriptive. Cross-fitted with bootstrap SEs.

5. **Variance result**: Promoted to Section 4 as co-equal core finding alongside the level null.

6. **Theoretical framework**: 4–6 page appendix model. Monopolistic competition with heterogeneous cognitive costs. Four propositions mapping to four findings: null mean (Hazledine 2006), positive variance (finer segmentation), supermodularity in (algorithm, sophistication) (Milgrom & Roberts 1990), no spillovers (large N independence).

7. **"Cognitive constraint" → "Technology-skill complementarity"**: Anchor in Autor, Levy & Murnane (2003); use rational inattention (Maćkowiak & Wiederholt 2009) as specific mechanism.

### 10. Immediate next actions

- [x] Run Session 2 literature searches (Semantic Scholar + database search strings)
- [x] Generate and distribute Gemini/ChatGPT/Claude cross-verification prompts
- [x] Process external research returns → fact-check log, referee report, action list
- [x] **PIVOT DECISION**: Switch from fuzzy RDD to ITT reduced form
- [ ] Read 5 Tier 1 papers and generate snapshots (Assad et al., Foroughifar & Mehta, Huang, Brown & MacKay, Noack & Rothe)
- [ ] Synthesize lit review positioning (`/lit-review`)
- [ ] Begin Week 2 P0 critical path: re-estimate ITT with seasonal controls
- [ ] Implement full RDD diagnostics battery
- [ ] Run variance analysis as secondary outcome
