# Referee Report 1: IO Economist
**Paper**: Algorithmic Pricing and Market Conduct on Airbnb
**Venue**: RAND Journal of Economics
**Date**: 2026-03-28

## Summary (1 paragraph)

This paper exploits the September 1, 2023 platform-wide rollout of Airbnb's redesigned pricing tools to estimate the intent-to-treat effect of algorithmic pricing availability on listing prices and price dispersion across eight U.S. cities. Using a sharp regression discontinuity in time (RDiT) on roughly 7.5--22 million listing-day observations and a complementary year-over-year difference-in-differences design, the authors find: (1) small, bandwidth-sensitive positive effects on residualized log prices (0.5--1.9%), with the DiD yielding the opposite sign; (2) increased within-listing temporal price variance under the RDD, but again sign-reversed under the DiD; and (3) a descriptive concentration of pricing changes among hosts with high pre-existing pricing sophistication. The paper frames these findings as evidence that market structure mediates algorithmic pricing effects -- contrasting Airbnb's many-seller, differentiated-product setting with the oligopolistic gasoline markets studied by Assad et al. (2024).

## Main Contribution Assessment

The paper asks a first-order policy question at a moment of intense regulatory activity (DOJ v. RealPage, the FTC's surveillance pricing inquiry, the EU DMA). The idea of testing whether algorithmic pricing concerns generalize from oligopolistic homogeneous-good markets to large differentiated-product platforms is genuinely valuable. If the results were clean, this would be a strong candidate for RAND or AEJ:Micro. Unfortunately, the identification problems are severe enough that the paper's main claims -- including the "opposite end of the spectrum" framing -- rest on shaky empirical foundations.

**Novelty relative to the key comparison papers:**

- *Assad et al. (2024, JPE)*: The paper explicitly positions itself as the market-structure contrast to Assad's gasoline duopoly evidence. This is a well-chosen foil. However, the comparison is asymmetric: Assad estimates a treatment-on-the-treated effect using structural-break IV to identify individual adoption, while this paper estimates an intent-to-treat effect diluted by unknown (and likely low) adoption. Comparing a 38% margin increase (ToT in duopoly) to a 0.5--1.9% price increase (ITT across all hosts, most of whom did not adopt) conflates the extensive and intensive margins. The paper acknowledges this in the limitations but not when making the headline comparison.

- *Musolff (2022)*: Studies repricing algorithms on Amazon -- a different platform architecture (marketplace with buy box) and different mechanism (Edgeworth cycle facilitation). The Airbnb setting is distinct enough that this paper does not directly compete with Musolff.

- *Calder-Wang & Kim (2024)*: Studies RealPage in multifamily rentals -- a hub-and-spoke setting where the algorithm explicitly aggregates competitor data. This is the closest structural analog to the Airbnb concern and the paper should engage more deeply with it (see Major Concern 4 below).

- *Foroughifar & Mehta (2024)*: Studies individual host adoption decisions. This paper claims to complement Foroughifar by estimating market-level equilibrium effects. This is a reasonable positioning, though the inability to observe adoption substantially weakens the complementarity.

- *Huang (2025)*: Provides the structural model that predicts precisely the variance result this paper finds suggestively. The paper should lean more heavily into the Huang connection and less into the Assad comparison.

**Bottom line on novelty**: The question is novel and policy-relevant. The setting is new. But the execution does not yet deliver results clean enough to sustain the paper's ambitious framing.

## Major Concerns (must address)

**1. The RDiT design has fundamental identification problems that the paper does not adequately resolve.**

The regression discontinuity in time faces three simultaneous threats that, taken together, severely undermine causal identification:

(a) *Density discontinuity*: An 11% jump in the number of active listings at the cutoff indicates a discrete compositional change. The balanced-panel check (retaining only listings present on both sides) is helpful but does not fully address this -- it shows that 90% of post-cutoff listings also appear pre-cutoff, but the 10% that are new entrants could have systematically different pricing.

(b) *Universal covariate imbalance*: All eight predetermined covariates show statistically significant discontinuities. The paper dismisses this as a precision artifact, but the combination of density jump plus universal imbalance is more than a precision story -- it indicates that the population of listings changes at the cutoff.

(c) *Non-flat pre-trends*: The event study shows all pre-period coefficients are statistically significant, with magnitudes (0.26--0.87%) comparable to or exceeding the treatment effect at wider bandwidths (0.51% at 90 days). If residual seasonality can generate pre-trend coefficients of this magnitude, it can also generate the post-cutoff estimate.

The Hausman-Rapson (2018) point about RDiT is precisely that time-based cutoffs are vulnerable to seasonal confounders that spatial RDDs avoid. The residualization procedure is a reasonable attempt to address this, but the evidence shows it has not fully succeeded. The paper needs either a stronger first-stage deseasonalization or a fundamentally different identification strategy. One constructive suggestion: if cross-city timing variation in scrape dates generates variation in the effective cutoff, this could be exploited. Another: the beta period (May--August 2023) could serve as a fuzzy treatment for early adopters.

**2. The RDD and DiD produce opposite signs for both outcomes -- the paper needs a framework for adjudicating between them.**

For price levels, the RDD estimates +0.5 to +1.9% while the DiD estimates -0.5 to -1.6%. For price variance, the RDD estimates +0.007 to +0.009 while the DiD estimates -0.0008. When two identification strategies yield opposite signs on the same outcome, neither result is convincingly identified.

The paper handles this honestly in Section 4.5 but then reverts to the RDD as the primary specification in the introduction and conclusion. The reader is left with the impression that the positive RDD estimates are the "real" result and the negative DiD estimates are a sensitivity check. But neither design dominates: the RDD is vulnerable to seasonal confounding (as the pre-trends confirm); the DiD is vulnerable to year-over-year market trends (increased supply, post-COVID normalization). The paper should either:

- Present a formal decomposition showing what secular trends would reconcile the two designs, and argue that one set of assumptions is more plausible, or
- Adopt the position that the true effect is bounded between the RDD and DiD estimates (i.e., approximately zero), and restructure the paper around a well-powered null.

The second option is actually the stronger contribution. A well-identified null in a large differentiated-product market would be informative for policy regardless of sign. But a well-identified null requires confronting the identification problems in Major Concern 1.

**3. The bundled treatment problem is more serious than the paper acknowledges.**

The minimum-nights placebo test reveals a large, significant discontinuity (-3.62 nights, p < 0.001), confirming that Airbnb's September 2023 update bundled pricing tool changes with other policy modifications. The paper controls for minimum nights in the RDD and shows the price estimates are unchanged, which is reassuring for a mechanical confounding channel. But the bundled treatment concern goes beyond mechanical confounding: the minimum-night change could have altered host pricing behavior through general equilibrium channels (e.g., hosts forced to accept shorter stays might adjust nightly prices upward to maintain revenue). A control variable does not address this pathway.

More fundamentally, the bundled treatment means the paper cannot cleanly attribute any effects to "algorithmic pricing tool availability." The treatment is "the September 2023 platform update," which includes pricing tools, minimum-night policy changes, and potentially other modifications. The paper should reframe accordingly, or provide evidence that isolates the pricing-tool component.

**4. The paper does not adequately engage with Harrington's hub-and-spoke theory.**

Harrington (2026) is the most directly relevant theoretical framework for this setting and the paper gives it exactly one paragraph. Harrington shows that a single platform acting as an algorithmic hub can facilitate coordination even with many small sellers -- precisely the structure of Airbnb's Smart Pricing. The paper's dismissal ("the hub exists but the spokes cannot coordinate on prices for fundamentally dissimilar listings") is asserted rather than demonstrated.

Specifically, the paper needs to address:

- *Why does product differentiation defeat hub-and-spoke coordination in theory?* Harrington's model allows for differentiated products under certain conditions. What conditions must fail for the Airbnb result to be consistent with the theory?

- *Is the relevant market really "many-seller"?* Airbnb listings within a neighborhood, room type, and price tier may face only a handful of close competitors. The paper treats the market as the entire city, but the relevant competitive interactions are hyperlocal. A host renting a 2BR apartment in Williamsburg, Brooklyn competes with perhaps 50--100 similar listings, not 40,000 NYC listings. At the neighborhood-room-type level, the market structure may not be as far from oligopoly as the paper claims.

- *Does partial adoption undermine the hub-and-spoke mechanism?* At ~22% adoption, the hub has few spokes. If adoption were 80%, would the results differ? The paper gestures at this in the conclusion but does not analyze it.

**5. The technology-skill complementarity framing is descriptive, and the paper should say so more forthrightly throughout.**

The paper's third finding -- that pricing changes concentrate among sophisticated hosts -- is based on a generated regressor (the unsupervised ML propensity index) that cannot distinguish treatment-effect heterogeneity from selection. The empirical strategy section correctly labels this as "explicitly descriptive," but the introduction and conclusion elevate it to a substantive finding and connect it to the Autor-Levy-Murnane (2003) task framework. This framing is forced. The ALM framework describes occupation-level task reallocation driven by IT adoption; applying it to within-platform pricing heterogeneity across Airbnb hosts is a stretch. The Mackowiak-Wiederholt (2009) rational inattention mechanism is more apt, but even there, the descriptive evidence cannot distinguish "the algorithm amplifies pre-existing expertise" from "hosts who were already adjusting prices frequently continued to do so after the update, and this shows up as a correlation with the propensity index."

I would recommend either (a) developing the heterogeneity analysis into a proper causal exercise (e.g., using a proxy variable IV approach per Lubotsky & Wittenberg 2006) or (b) presenting it straightforwardly as descriptive and removing the ALM framing.

**6. The ITT-vs-ToT comparison with Assad et al. is misleading and should be corrected.**

The paper's headline claim is that its effects are "an order of magnitude smaller" than Assad's 38%. But Assad estimates a ToT effect among duopolies where both stations adopted algorithms. This paper estimates an ITT across all hosts, most of whom did not adopt. If the adoption rate is ~22% (Foroughifar's estimate for the original Smart Pricing), a naive Wald-type scaling implies a ToT of roughly 2.3--8.6%, which is far less than an "order of magnitude" below Assad's 38% but no longer negligible. The paper acknowledges this arithmetic in the limitations (conclusion, paragraph 4) but buries it, while the headline comparison in the introduction and abstract presents the raw ITT-vs-ToT gap as if it were an apples-to-apples market-structure contrast.

This is the single most misleading element of the paper and must be corrected. Either (a) present the Wald-scaled ToT as a back-of-envelope calculation alongside the ITT, or (b) restructure the Assad comparison to compare ITT-to-ITT (Assad's reduced-form structural-break effect, if available) or explicitly note the incomparability.

## Minor Concerns

1. **Bandwidth sensitivity is illusory for residualized outcomes.** The verification report flags that all four residualized bandwidth rows in the pooled table produce identical N counts (22,573,179), suggesting that bandwidth filtering on the residualized running variable captures the entire sample regardless of the nominal bandwidth. The "declining with bandwidth" pattern for residualized estimates in the current tables (1.93%, 0.95%, 0.67%, 0.51%) apparently reflects a correction made after the verification report, but the authors should confirm that the bandwidth filtering now operates on the raw running variable as intended, and document this clearly.

2. **The rdrobust rows in the pooled table show dashes.** If the MSE-optimal bandwidth results are unavailable, they should either be populated or the table rows removed. Presenting empty rdrobust rows alongside OLS estimates creates an incomplete impression.

3. **Equation (2) does not match the code implementation.** The verification report documents that the written DiD equation specifies a Post x Year interaction model while the code implements a two-way FE year-coefficient model. These are algebraically related but not identical. The paper should either rewrite the equation to match the code or explain the equivalence.

4. **Selective reporting of city-specific results.** The results section highlights 4 of 8 cities. The current version (which now reports all 8) is an improvement but should note explicitly that the effect is null in the largest market (Los Angeles, N = 5.0M) and that Chicago's 5.6% effect is a substantial outlier. A leave-one-city-out sensitivity that drops Chicago would be informative.

5. **The "3% collusion threshold" is asserted without justification.** The power analysis claims the design can detect effects 50 times smaller than the 3% threshold "that would signal meaningful collusion." This threshold is not derived from theory or cited to any source. Given that Assad finds 38%, one could argue any effect above 1% is policy-relevant in a market of Airbnb's size. The paper should either justify the threshold or remove it.

6. **The paper does not discuss third-party pricing tools.** Beyond Pricing, PriceLabs, and Wheelhouse serve Airbnb hosts independently of the platform's native tools. If their usage changed around September 2023, this confounds the treatment. The data limitations section mentions this but does not assess the likely direction or magnitude of bias.

7. **Forward-looking posted prices vs. transaction prices.** The outcome variable is the calendar price posted for a future date, not the price at which the night was booked. If the algorithm primarily affects last-minute pricing adjustments (which seems likely for a demand-responsive tool), the forward-looking calendar price may not capture the treatment effect. This limitation deserves more discussion.

8. **The "DDD" terminology should be corrected to "DiD."** The design has two dimensions of variation (pre/post cutoff, year), not three. The code filenames use "ddd" but the text should consistently use "DiD" to avoid confusion.

## Questions for the Author

1. Can you provide the Wald-scaled ToT estimate assuming the Foroughifar 22% adoption rate? How does the Assad comparison change under this scaling?

2. What does the RDD estimate look like when you restrict to listings that were actively adjusting prices in the pre-period (i.e., listings with non-zero pre-cutoff price variance)? This would partially address whether the effect is driven by already-active pricers vs. the full population.

3. Have you examined whether the Chicago outlier (5.6% vs. 0--2% for most other cities) reflects a city-specific confound (e.g., a local regulation change, a major event, or a change in the Inside Airbnb scraping schedule)?

4. The beta period (May--August 2023) could provide a dose-response test: do hosts in the beta window show different pricing patterns from those who first accessed the tools on September 1? This would help distinguish the pricing tool from other bundled changes.

5. At the neighborhood-room-type level, how many effective competitors does a typical listing face? If the "many-seller" characterization applies only at the city level but not at the relevant market level, the contrast with Assad's gasoline duopolies is overstated.

6. The DiD estimates are consistently negative across all leave-one-city-out specifications. How do you interpret a robust negative year-over-year price change? Is this consistent with increased supply or post-COVID normalization, and if so, does it suggest the RDD is picking up a supply-driven composition effect rather than an algorithm effect?

7. Have you considered a triple-difference that interacts the DiD with a measure of local algorithm exposure (e.g., pre-period Smart Pricing adoption rates, if these can be proxied)? This would provide cross-sectional variation that the current designs lack.

8. What is the first-stage adoption rate for the 2023 redesigned tools? Foroughifar's 22% is from the 2015 Smart Pricing rollout. If the 2023 redesign had substantially higher or lower adoption, the ITT interpretation changes materially.

## Overall Recommendation

**Revise and Resubmit (Major Revision)**

The paper addresses a timely and policy-important question -- whether algorithmic pricing concerns from oligopolistic markets generalize to large differentiated-product platforms -- and the data collection effort across eight cities is commendable. The question is squarely within RAND's scope, and a clean answer would be a significant contribution to the IO literature on algorithmic markets.

However, the current draft has identification problems that prevent the results from supporting the paper's ambitious framing. The RDiT design faces simultaneous challenges (density jump, universal covariate imbalance, non-flat pre-trends, bundled treatment) that the residualization does not fully resolve. The two identification strategies yield opposite signs on both outcomes. The headline comparison with Assad et al. conflates ITT and ToT. The technology-skill complementarity framing is descriptive but presented as causal.

The path to publication at RAND requires:

1. Resolving or forthrightly acknowledging the identification challenges, ideally by making the balanced-panel RDD the primary specification and conducting formal sensitivity analyses (e.g., Oster 2019 bounds) for the degree of selection that would explain away the results.

2. Restructuring around a well-powered, honestly presented near-null as the main contribution. "Algorithmic pricing does not raise prices in differentiated-product platform markets" is a publishable finding if the identification is credible. The variance and heterogeneity results should be presented as suggestive secondary findings.

3. Correcting the Assad comparison to account for ITT-vs-ToT, and engaging seriously with Harrington's hub-and-spoke framework at the relevant (neighborhood-level) market definition.

4. Toning down the policy recommendations to match the evidence from a single platform.

I would not recommend desk rejection. The question is important, the data are rich, and the authors are unusually transparent about limitations. But the paper needs substantial revision before the empirical results can support the theoretical and policy claims.
