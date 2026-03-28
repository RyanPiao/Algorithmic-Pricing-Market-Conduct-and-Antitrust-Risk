# Gap Analysis: Algorithmic Pricing and Market Conduct

**Project**: Algorithmic Pricing and Market Conduct — Evidence from Airbnb Smart Pricing
**Date**: 2026-03-24

---

## Gaps Identified

### Gap 1: No quasi-experimental evidence from many-seller differentiated markets (DESIGN GAP)

**What exists**: Quasi-experimental evidence on algorithmic pricing exists only for (a) gasoline duopolies (Assad et al. 2024), (b) Amazon Buy Box repricing (Musolff 2022), and (c) multifamily rentals (Calder-Wang & Kim 2024). All are homogeneous-product oligopolies or near-oligopolies.

**What's missing**: No study provides credible causal estimates of algorithmic pricing effects in a many-seller, differentiated-product platform market. Foroughifar & Mehta (2024) and Huang (2025) study Airbnb but use structural models, not quasi-experimental designs.

**Why it matters**: The antitrust debate implicitly assumes algorithmic pricing effects generalize across market structures. Without evidence from the differentiated-product end of the spectrum, regulators cannot calibrate their response.

**How our paper fills it**: Sharp ITT exploiting Airbnb's platform-wide September 2023 pricing tool rollout across 8 US cities. 24.2 million listing-day observations. First multicity quasi-experiment on a major platform pricing algorithm.

---

### Gap 2: No separation of price-level vs. price-dispersion effects (MEASUREMENT GAP)

**What exists**: Assad et al. (2024) examine margin levels and between-duopolist price dispersion (finding null on dispersion). Musolff (2022) focuses on price cycles. Huang (2025) structurally decomposes frictions but does not empirically estimate the causal effect of algorithm access on variance.

**What's missing**: No study empirically separates the effect of algorithmic pricing on (a) average price levels from (b) within-seller temporal price variance/dispersion. The distinction is critical because collusion predicts level increases while discrimination predicts variance increases --- the two have opposite welfare and policy implications.

**Why it matters**: A null on levels alone is uninformative --- it could reflect either "no effect" or "effects on the wrong outcome." The variance finding converts the null into a positive result with a clear economic interpretation.

**How our paper fills it**: Dual-outcome RDD estimating effects on both log_price levels and within-listing rolling price variance. The joint finding (null levels + positive variance) identifies the mechanism as discrimination, not collusion.

---

### Gap 3: No empirical test of technology-skill complementarity in pricing (MECHANISM GAP)

**What exists**: The technology-skill complementarity framework (Autor et al. 2003; Bresnahan et al. 2002) is well-established for labor markets. Brynjolfsson et al. (2025) test it for generative AI in customer service (finding the opposite pattern: AI helps low-skill workers). Garcia et al. (2024) provide suggestive structural evidence for hotel pricing. Huang (2025) documents the bimodal skill distribution but does not test how algorithm *access* interacts with skill.

**What's missing**: No reduced-form empirical test of whether algorithmic pricing tools disproportionately benefit sophisticated vs. unsophisticated sellers. The technology-skill complementarity framework has not been applied to platform pricing algorithms.

**Why it matters**: If algorithms help all sellers equally, the policy concern is about aggregate market effects. If they help only sophisticated sellers, the concern shifts to distributional effects and unequal access --- a different regulatory problem.

**How our paper fills it**: ML-constructed latent sophistication proxy from pre-treatment pricing behavior. Descriptive heterogeneity analysis (cross-fitted, bootstrap SEs) showing effects concentrate among high-sophistication hosts. Framed via supermodularity of (algorithm access, host sophistication).

---

### Gap 4: No study of the "opposite end" from Assad et al. (BOUNDARY GAP)

**What exists**: Assad et al. (2024) study the setting most conducive to algorithmic collusion: homogeneous product, duopoly, mandated real-time transparency, identifiable rivals. They explicitly note their results may not generalize.

**What's missing**: A study of the setting *least* conducive to collusion --- providing the other bookend needed to map the boundaries of when algorithmic pricing raises competition concerns. The theoretical predictions are clear (many sellers + differentiation + imperfect transparency should dampen coordination), but no empirical study confirms this.

**Why it matters**: Together with Assad et al., such a study would establish the empirical frontier: regulators could then assess where specific markets fall on the spectrum and calibrate enforcement accordingly.

**How our paper fills it**: Airbnb represents the polar opposite of German gasoline on every dimension that matters for coordination (see debate map). Our null on levels combined with Assad et al.'s positive finding maps the boundary.

---

### Gap 5: Welfare implications of algorithm-enabled price discrimination on platforms (OPEN)

**Status**: NOT filled by our paper. Our paper identifies the *mechanism* (discrimination, not collusion) and *who benefits* (sophisticated hosts), but does not estimate consumer welfare effects. Under standard theory, third-degree price discrimination has ambiguous welfare effects (Varian 1985). Huang (2025) provides structural welfare estimates for a single city; quasi-experimental welfare estimation across multiple markets remains open.

**Testable next step**: Combine our ITT estimates with a demand model (following Huang's framework) to simulate consumer surplus effects of the variance increase. Alternatively, test whether Smart Pricing availability increases total bookings (extensive margin) --- a sufficient statistic for welfare improvement if new bookers have lower willingness-to-pay.

---

## Contribution Statement (3 sentences)

This paper provides the first multicity quasi-experimental evidence on the market-level effects of a major platform pricing algorithm. We establish three novel findings: (a) precise bounds ruling out aggregate price-level increases above 3%, shifting the debate from "does algorithmic pricing cause collusion?" to "what does it cause instead?"; (b) a positive causal effect on temporal price dispersion, identifying price discrimination as the algorithm's primary market footprint; and (c) descriptive evidence that pricing changes concentrate among hosts with high pre-existing sophistication, consistent with technology-skill complementarity. Together with Assad et al. (2024), these findings map the empirical frontier of when algorithmic pricing raises competition concerns versus when it enables efficiency-enhancing discrimination.
