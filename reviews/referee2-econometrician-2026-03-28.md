# Referee Report 2: Econometrician / RDD Methodologist
**Paper**: Algorithmic Pricing and Market Conduct: Evidence from Airbnb's Pricing Tools
**Venue**: RAND Journal of Economics
**Date**: 2026-03-28

## Summary

This paper estimates the intent-to-treat effect of Airbnb's September 2023 pricing-tool rollout on listing prices and price variance across eight U.S. cities using a sharp regression discontinuity in time (RDiT) design. The residualized RDD finds small positive price-level effects (0.5--1.9%) that decline monotonically with bandwidth, and positive variance effects. A year-over-year difference-in-differences specification yields estimates of the opposite sign for both outcomes. The paper is commendably transparent about this disagreement and the identification challenges it implies. However, the methodological concerns are sufficiently serious that I cannot recommend acceptance in the current form. The core problem is that neither identification strategy is convincing on its own, and together they bracket an effect that is plausibly zero. Several diagnostics --- universal covariate imbalance, nonzero pre-trends, sign-flipping leave-one-out results, and a bundled treatment --- compound the identification difficulties.

## Identification Assessment

The paper's primary identification strategy is a sharp RDiT exploiting the common September 1, 2023 rollout date. The identifying assumption requires that the conditional expectation of potential outcomes is continuous through the cutoff after seasonal adjustment. I assess this assumption as unlikely to hold cleanly, for four reasons:

1. **The density discontinuity is large and acknowledged.** An 11% jump in active listings at the cutoff indicates a first-order compositional change. The balanced-panel robustness check (retaining ~90% of listings) is helpful but does not fully address the concern: the 10% of listings that appear only post-cutoff may differ systematically from continuing listings, and their exclusion changes the estimand. More importantly, even among continuing listings, the *intensity* of listing availability may shift at the cutoff (e.g., hosts reactivating calendars for fall bookings), changing the effective composition of listing-days even within the balanced panel.

2. **Universal covariate imbalance.** All eight predetermined covariates show statistically significant discontinuities at the cutoff ($p < 0.001$ for seven of eight, $p = 0.001$ for host listing count). The paper argues these are small relative to variable means and driven by the massive sample size. This argument is incomplete. The relevant question is not whether the imbalances are large in absolute terms, but whether they are large enough to generate the estimated treatment effects through the covariate-outcome relationship. With a 0.5--1.9% treatment effect on log prices, even small compositional shifts in accommodates (+0.034), bedrooms (+0.013), or review count (-2.3) could produce bias of the same order of magnitude as the estimated effect. The paper should report the implied bias from a back-of-envelope calculation using the covariate imbalances and the covariate coefficients in a hedonic regression.

3. **Nonzero pre-trends in the event study.** The event-study pre-period coefficients are statistically significant and, as the paper acknowledges, several are larger than the treatment effect at wider bandwidths. This directly undermines the continuity assumption. The paper's candor on this point is appreciated, but the implication is stark: the residualization procedure does not remove enough seasonal variation to make the RDiT credible at the precision level this sample affords.

4. **The running variable is calendar time, not an assignment variable.** The fundamental tension in any RDiT design is that time is not a conventional forcing variable --- units do not sort around the cutoff in the McCrary sense, but seasonal patterns create structural breaks that mimic treatment effects. The Hausman-Rapson (2018) critique applies with full force here. The September 1 cutoff coincides with the transition from summer to fall, a first-order event in short-term rental markets (back-to-school demand shifts, Labor Day weekend effects, seasonal host reactivation). The residualization procedure is the paper's defense against this critique, but the evidence from the pre-trends and bandwidth sensitivity suggests it is insufficient.

## Major Concerns (Must Address)

### 1. The RDD vs. DiD Sign Disagreement Is More Damaging Than Acknowledged

The paper presents both the RDD (+0.5 to +1.9%) and DiD (-0.5 to -1.6%) estimates and states the true effect is "plausibly bounded between them --- plausibly near zero." This framing buries the lead. If two credible identification strategies yield opposite-signed, statistically significant estimates for the same parameter, the correct inference is that at least one (and possibly both) is contaminated by confounders. The paper treats this as an interpretive nuance; I view it as a fatal identification problem that must be resolved or at least substantially narrowed before publication.

**Required action**: The paper must provide a formal decomposition of what drives the sign disagreement. Specifically: (a) estimate the DiD on the exact same bandwidth windows as the RDD (not just weeks 38--52); (b) construct a triple-difference estimator that uses the 2022 same-calendar-date observations to deseasonalize the 2023 RDD directly; (c) report whether the sign disagreement persists in the balanced panel restricted to listings present in both 2022 and 2023.

### 2. The Bandwidth-Declining Pattern Is Consistent with Residual Seasonal Confounding

The monotonic decline from 1.9% at +/-30 days to 0.5% at +/-90 days is the central empirical pattern, and the paper correctly identifies two interpretations: genuine local effect versus residual confounding. However, the paper does not provide tests to discriminate between these hypotheses.

**Required action**: (a) Report the placebo RDD at September 1, 2022 and September 1, 2021 (same calendar date, no treatment) and show the bandwidth-sensitivity profile. If the placebo exhibits the same declining pattern, the confounding interpretation dominates. (b) Report the Calonico-Cattaneo-Farrell (2020) bias-corrected estimates with robust confidence intervals for each bandwidth --- the missing `rdrobust` rows in Table 1 (currently showing dashes) are essential. (c) Implement a data-driven bandwidth selector (CCT optimal) and report whether the optimal bandwidth is closer to 30 or 90 days.

### 3. The Noack-Olma-Rothe Implementation Needs More Detail and Validation

The paper invokes Noack, Olma, and Rothe (2025) to justify the cross-fitted residualization procedure. The theoretical guarantee (Theorem 1: consistency regardless of adjustment function specification) is correctly stated but potentially misleading in this context. The guarantee applies to the RDD estimator's consistency for the true treatment effect, conditional on the adjustment function being estimated on data outside the local neighborhood of the cutoff. However, the paper's implementation uses a Ridge regression with Fourier harmonics trained on the full bandwidth window, including observations near the cutoff. If the adjustment function is estimated using data that includes the treatment effect, the Noack-Olma-Rothe guarantee does not apply in its standard form.

**Required action**: (a) Clarify whether the cross-fitting excludes a neighborhood around the cutoff from the training folds or only cross-fits across listings. (b) If the former, specify the excluded neighborhood width. (c) If the latter, acknowledge that the Noack-Olma-Rothe guarantee requires modification when training data includes treated observations. (d) Report the R-squared of the first-stage residualization and the Ridge penalty parameter. (e) Show the residualized outcome series as a time-series plot (not just the event study) so readers can visually assess whether seasonal patterns remain.

### 4. Bundled Treatment and the Minimum-Nights Confound

The paper acknowledges that the September 2023 release bundled pricing tools with other changes, including minimum-night requirements. The placebo test on minimum nights shows a large, significant discontinuity (-3.62, $p < 0.001$). The paper argues that "controlling for minimum nights in the RDD does not change the price estimates." But this is a bad-control argument: minimum nights is itself a treatment delivered simultaneously with the pricing tools. If the minimum-nights change affects prices (as it almost certainly does --- binding minimum-night constraints mechanically affect the effective nightly price by changing the booking duration), then controlling for it either absorbs part of the treatment effect or introduces collider bias, depending on the causal structure. The near-identical estimates with and without the control could reflect either (a) genuinely no confounding or (b) the minimum-nights effect operating through a channel orthogonal to the RDD's local linear trend.

**Required action**: (a) Discuss the causal structure explicitly --- is minimum nights a mediator, a confounder, or a co-treatment? (b) If a co-treatment, acknowledge that the ITT captures the joint effect of all bundled changes, not the pricing-tool effect alone. (c) Test whether the minimum-nights change itself exhibits bandwidth sensitivity or a declining pattern. If it does, this strengthens the confounding interpretation of the price results.

### 5. Leave-One-Out Results Reveal Fragility, Not Robustness

The leave-one-out table shows that dropping Los Angeles or New York City --- the two largest markets, contributing roughly 30% and 28% of observations respectively --- flips the pooled estimate negative. The positive pooled result is driven by mid-size cities (Chicago at +5.6%, Seattle at +2.9%). This is not a robustness check that passes; it is evidence that the treatment effect is highly heterogeneous and the pooled estimate is not representative. The paper buries this in a single sentence.

**Required action**: (a) Report the pooled estimate with inverse-variance weighting across cities (random-effects meta-analysis) alongside the OLS pooled estimate. (b) Report a formal test for treatment effect heterogeneity across cities (e.g., Q-statistic). (c) Discuss why Chicago shows a 5.6% effect --- nearly six times the pooled estimate --- and whether this reflects a genuine city-specific mechanism or a city-specific confounder.

## Minor Concerns

1. **Standard errors may be too small.** Clustering at the listing level accounts for within-listing serial correlation but not for cross-listing spatial correlation within city-dates. With 130,000 listings across only 8 cities, there are effectively 8 clusters at the city level. The paper should report Cameron-Gelbach-Miller wild cluster bootstrap standard errors at the city level, or at minimum acknowledge that the listing-clustered SEs may substantially understate uncertainty. With 8 clusters, the effective degrees of freedom for the treatment effect are very low.

2. **The variance outcome is not residualized.** The paper residualizes the level outcome but computes the variance RDD on raw rolling variances. This inconsistency is acknowledged but undercuts the variance result. Seasonal transitions mechanically increase within-listing price variance (summer-to-fall price adjustments). The paper should residualize the variance outcome using the same two-stage procedure or explain why this is infeasible.

3. **Forward-looking posted prices vs. transaction prices.** The paper notes this limitation but does not discuss the direction of bias. If algorithmic pricing induces more frequent price adjustments to match demand, forward-looking calendar prices observed weeks before check-in may not reflect final booking prices. The treatment effect on posted prices could overstate or understate the effect on transaction prices, depending on the timing of the calendar scrape relative to the booking window.

4. **The heterogeneity analysis (technology-skill complementarity) is underdeveloped.** The latent sophistication proxy is constructed from the same pricing behavior that the algorithm is supposed to change. Hosts who already engage in dynamic pricing (high pre-treatment variance, weekend premiums) are likely different on unobservables. The paper calls this "descriptive," which is appropriate, but the conclusion section elevates it to a "finding" on par with the price-level and variance results.

5. **The `rdrobust` rows in Table 1 are empty.** These are crucial --- the Calonico-Cattaneo-Titiunik bias-corrected estimates with robust confidence intervals are the standard in the literature and should be the headline specification, not the manual-bandwidth OLS. Their absence is a significant gap.

6. **The beta period (May 3 -- August 31, 2023) is problematic.** Observations from this period fall on the pre-cutoff side of the running variable, but some hosts were already using the redesigned tools. This contaminates the control group in a way that biases the ITT toward zero. The paper should report specifications excluding the beta period entirely (using only pre-May 3 data as the pre-period), even though this would asymmetrize the bandwidth.

7. **No discussion of multiple testing.** The paper reports results for 2 outcomes (levels, variance) x 4 bandwidths x 3 specifications (full, balanced, controlled) x 8 cities. With massive sample sizes producing $p < 0.001$ throughout, the multiple-testing concern is less about false positives from $p$-hacking and more about the interpretive weight placed on patterns across specifications. The bandwidth-declining pattern, for instance, involves comparing four non-independent estimates.

8. **The related-work section places this paper relative to Assad et al. (2024) but understates the identification gap.** Assad et al. have a genuine instrument (brand-HQ adoption decisions) and document a 38% effect. This paper has no instrument, documents a 0.5--1.9% effect that sign-flips under an alternative design, and cannot attribute it to the pricing tool specifically. The comparison is aspirational rather than methodological.

## Required Additional Tests

1. **Placebo cutoff bandwidth profiles.** Estimate the RDD at September 1, 2022 and September 1, 2021 at all four bandwidths. Report whether the declining-with-bandwidth pattern is unique to the treatment year.

2. **Wild cluster bootstrap at the city level.** Report $p$-values from Cameron-Gelbach-Miller wild bootstrap with 8 city-level clusters for all headline specifications.

3. **Triple-difference estimator.** Use 2022 same-calendar-date observations to deseasonalize the 2023 RDD directly: $\tilde{Y}_{2023} - \tilde{Y}_{2022}$ as the outcome in the RDD. This combines the strengths of both designs.

4. **Bias decomposition from covariate imbalance.** Using hedonic regression coefficients, compute the implied bias from the covariate discontinuities and compare to the estimated treatment effect.

5. **Complete the `rdrobust` estimates.** Report CCT bias-corrected estimates with robust confidence intervals and the MSE-optimal bandwidth for both outcomes.

6. **Residualized variance RDD.** Apply the two-stage residualization to the variance outcome and re-estimate.

7. **Exclude-the-beta-period specification.** Use only pre-May 3, 2023 observations as the pre-period in the RDD.

8. **Time-series plot of residualized outcomes.** Show the daily mean of the residualized outcome across the full sample period so readers can assess the quality of the seasonal adjustment.

9. **Heterogeneity in the declining-bandwidth pattern.** Report whether the bandwidth sensitivity is concentrated in specific cities. If Chicago's 5.6% effect does not decline with bandwidth while other cities' effects do, this would point toward city-specific confounders.

10. **Permutation inference.** Randomly reassign the cutoff date (within reasonable calendar windows) and estimate the RDD. Report where the actual estimate falls in the permutation distribution. This is the most direct test of whether the September 1 discontinuity is unusual relative to other calendar dates.

## Overall Recommendation

**Revise and Resubmit (Major Revision)**

This paper addresses an important policy question --- whether platform-provided algorithmic pricing tools raise prices in differentiated-product markets --- and the answer matters for antitrust enforcement. The institutional setting is well-chosen, the data are large-scale, and the paper is unusually honest about its limitations. These are substantial virtues.

However, the identification is not yet convincing. The core RDiT design faces serious challenges: universal covariate imbalance, a large density discontinuity, nonzero pre-trends, a bundled treatment, and --- most critically --- sign disagreement with the complementary DiD strategy for both outcomes. The monotonically declining bandwidth pattern, while potentially reflecting a genuine local effect, is also consistent with residual seasonal confounding that the Noack-Olma-Rothe residualization does not fully remove. The leave-one-out analysis reveals that the positive pooled estimate is driven by a few mid-size cities and is not robust to excluding the two largest markets.

The paper's honesty is its greatest asset but also exposes the depth of the problem: the authors have essentially presented evidence that their two identification strategies disagree, that neither is definitive, and that the true effect is "plausibly near zero." A RAND-quality publication requires either resolving this disagreement (via the triple-difference or permutation tests suggested above) or reframing the contribution away from causal identification and toward a methodological case study of RDiT limitations in platform settings. The latter framing would be legitimate and valuable but would require significant restructuring.

I would be willing to review a revised version that implements the triple-difference estimator, completes the `rdrobust` specifications, reports wild-cluster-bootstrap inference, and provides the placebo bandwidth profiles. If these additional tests narrow the RDD-DiD disagreement and point toward a coherent story, the paper could be publishable. If they do not, the paper should be reframed as a cautionary methodological contribution rather than a causal study of algorithmic pricing.
