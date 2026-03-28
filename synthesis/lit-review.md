# Literature Review: Algorithmic Pricing, Market Conduct, and Price Discrimination

**Project**: Algorithmic Pricing and Market Conduct — Evidence from Airbnb Smart Pricing
**Date**: 2026-03-24
**Type**: Standalone survey (5 thematic sections + embedded contribution section)
**Papers covered**: 32 from prioritized reading list + supplementary references

---

## Embedded Contribution Section (for paper introduction)

This paper contributes to three strands of literature.

First, we contribute to the growing empirical literature on algorithmic pricing and competition. Calvano et al. (2020) demonstrate in simulation that Q-learning agents converge to supra-competitive pricing with reward-punishment strategies, sparking intense debate about real-world algorithmic collusion. Assad, Clark, Ershov, and Xu (2024) provide the strongest quasi-experimental evidence to date: in German gasoline duopolies, mutual adoption of algorithmic pricing raises margins by 38%, with effects emerging only after 12 months and only when both competitors adopt. Musolff (2022) documents similar tacit coordination among Amazon marketplace repricing algorithms. Brown and MacKay (2025) show theoretically that even without collusion, a single firm with a fast, committed pricing algorithm can coerce rivals into sustaining supra-competitive prices. Yet all of these settings share features maximally conducive to coordination: homogeneous products, oligopoly, real-time price transparency, and identifiable bilateral rivals. We provide the first large-scale quasi-experimental evidence from a differentiated-product platform market with many sellers, where these conditions are absent. Our precisely estimated null on price levels --- ruling out effects above 3% --- establishes that algorithmic pricing does not universally raise prices; market structure fundamentally mediates the competitive effects.

Second, we contribute to the literature on platform-mediated pricing and pricing frictions. Huang (2025) structurally estimates that 85% of Airbnb hosts set near-uniform prices due to cognitive constraints, and that the welfare-optimal platform remedy sets price *variation* while hosts retain control over price *levels*. Foroughifar and Mehta (2024) document that only 22% of hosts adopt Smart Pricing, with pessimistic prior beliefs --- not adoption costs --- as the primary barrier. Zhang, Mehta, Singh, and Srinivasan (2025) show that differential algorithm adoption contributes to the racial revenue gap on Airbnb. These papers study individual host decisions; we complement them by estimating the market-level equilibrium consequences of algorithm availability. Our finding that the algorithm's primary footprint is increased temporal price variance, not price-level inflation, is precisely the outcome Huang's structural model predicts under platform-assisted pricing.

Relative to the most closely related paper, Assad et al. (2024), we differ along four dimensions: (i) market structure (many differentiated sellers vs. gasoline duopoly), (ii) identification strategy (sharp ITT exploiting platform-wide rollout vs. structural-break IV for individual adoption), (iii) the outcome we emphasize (price variance/discrimination vs. price levels/margins), and (iv) the mechanism we identify (technology-skill complementarity vs. tacit collusion through punishment of undercutting). Together, the two papers map the boundaries of when algorithmic pricing raises prices versus when it enables price discrimination.

---

## 1. Algorithmic Collusion: Theory and Empirical Evidence

### 1.1 Theoretical foundations

The theoretical literature on algorithmic collusion begins with the insight that autonomous pricing agents can learn to sustain supra-competitive outcomes without explicit communication. Calvano et al. (2020, AER) show that tabular Q-learning agents in a Bertrand oligopoly with logit demand consistently converge to prices above Nash equilibrium and develop reward-punishment strategies resembling those in the theory of repeated games. Their finding that convergence requires approximately 500,000 periods --- roughly a year in daily pricing --- became a key empirical prediction. The companion piece in *Science* (Calvano et al. 2020b) translates these findings into policy implications, arguing that standard antitrust tools may be insufficient.

However, the robustness of these findings has been contested. Lambin (2024) demonstrates that memoryless agents with no capacity for punishment strategies also produce supra-competitive prices, suggesting the mechanism may be "learning inertia" rather than genuine strategic collusion. Bichler, Durmann, and Oberlechner (2024) show that more sophisticated algorithms (bandit methods, PPO, DQN) generally converge closer to Nash equilibrium than tabular Q-learning, with collusion risk concentrated in the simplest learning algorithms. Dou, Goldstein, and Ji (2025) propose an alternative mechanism: algorithms collude via homogenized learning biases ("artificial stupidity") that over-prune the strategy space, rather than through learned punishment.

Brown and MacKay (2025) introduce a fundamentally distinct channel: *coercion*, not collusion. A single firm with a fast pricing algorithm and multi-period commitment can reshape a rival's within-period payoffs, sustaining prices that exceed even the fully collusive benchmark. Critically, this mechanism requires asymmetric speed advantage, monitoring of a specific rival, and commitment to a persistent rule --- conditions satisfied in tight oligopolies with homogeneous products but unlikely in many-seller differentiated markets.

### 1.2 Empirical evidence

Empirical evidence on real-world algorithmic pricing effects remains scarce. Assad et al. (2024, JPE) provide the cleanest design: using structural breaks in pricing behavior to detect adoption and brand-HQ adoption shares as instruments, they estimate that mutual algorithmic adoption in German gasoline duopolies raises market margins by 3.2 cents/liter (~38%), with effects concentrated at 12+ months post-adoption. The monopolist/non-monopolist split --- showing null effects for monopolists --- provides compelling evidence for the competition channel. Critically, their null finding on between-duopolist price dispersion (Table 7) indicates that algorithms raise both firms' prices in tandem.

Musolff (2022) exploits a regression discontinuity in Amazon Buy Box eligibility to show that automatic repricing algorithms facilitate Edgeworth-cycle-style coordination in e-commerce. Werner (2026) provides lab evidence that algorithms are more collusive than humans in small-numbers settings. On the skeptical side, Bichler et al. (2024) argue that most practical online optimization algorithms converge to Nash, suggesting collusion risk may be overstated for non-tabular-Q-learning methods.

### 1.3 Where our paper fits

The empirical settings studied to date share features maximally conducive to coordination: homogeneous products (gasoline, commodity goods), small numbers (duopoly/triopoly), real-time price transparency, and identifiable bilateral rivals. Our Airbnb setting represents the opposite end of the spectrum --- highly differentiated products, many sellers per market, imperfect comparability, and diffuse competition --- providing a natural test of whether algorithmic pricing effects generalize beyond coordination-prone markets.

### Literature comparison: Algorithmic collusion empirics

| Authors | Year | Setting | Products | Market structure | Algorithm type | Key finding | N (obs) |
|---------|------|---------|----------|-----------------|---------------|-------------|---------|
| Assad et al. | 2024 | German gas stations | Homogeneous | Duopoly (median 2/ZIP) | Third-party competitive-reaction | +38% margins (both adopt) | 448K station-months |
| Musolff | 2022 | Amazon marketplace | Differentiated | Oligopoly (Buy Box) | Automatic repricing | Edgeworth cycles, coordination | -- |
| Werner | 2026 | Lab experiment | Homogeneous | Duopoly/triopoly | Q-learning agents | Algorithms more collusive than humans | -- |
| Calder-Wang & Kim | 2024 | US multifamily rentals | Homogeneous (apts) | Local oligopoly | RealPage (centralized) | Coordination via shared algorithm | -- |
| **This paper** | 2026 | Airbnb (8 US cities) | Highly differentiated | Many sellers | Platform demand-prediction | **Null on levels; +variance** | 24.2M listing-days |

---

## 2. Airbnb and Platform Pricing

### 2.1 Pricing frictions on Airbnb

Airbnb hosts exhibit substantial pricing frictions. Huang (2025) documents a bimodal distribution: approximately 85% of San Francisco hosts set near-uniform prices (median within-listing standard deviation of log price is 5%), while only 15% display algorithm-like flexible pricing. Using a structural model with Calvo-style adjustment costs and cognitive constraints, he estimates that pricing frictions cost consumers 14% in welfare and the most affected sellers up to 15% in profit. Crucially, pricing sophistication is a *persistent host type* correlated with multi-listing status but not caused by scale or learning (Table 2B), supporting a technology-skill complementarity interpretation.

Huang's most policy-relevant finding is Counterfactual 3: a platform-assisted pricing design where the platform sets price *variation* (adjustment function across nights and booking lead-time) while sellers retain the right to set price *levels* nearly achieves the first-best, raising consumer surplus 3.2% above first-best while benefiting 62% of sellers. This structural prediction maps directly onto our empirical result: Smart Pricing availability increases temporal price variance without shifting price levels.

### 2.2 Smart Pricing adoption and performance

Foroughifar and Mehta (2024) study why only 22% of Airbnb hosts adopt Smart Pricing over 20 months. Using AirDNA data with price-type labels for five US cities and a structural dynamic adoption model, they find that pessimistic prior beliefs --- hosts believe Smart Pricing sets prices 38% lower than it actually does --- are the dominant barrier, explaining 8x more non-adoption than adoption costs. They also document that Smart Pricing generates lower revenue than manual Custom pricing, because the algorithm is designed to maximize bookings (platform revenue) rather than host profit, and it lacks marginal cost information.

Zhang, Mehta, Singh, and Srinivasan (2025, Marketing Science) document that differential Smart Pricing adoption contributes to racial disparities in Airbnb revenue. Black hosts adopt Smart Pricing at higher rates but see smaller revenue gains, consistent with the algorithm interacting with pre-existing differences in pricing knowledge and market positioning.

### 2.3 Platform pricing algorithms more broadly

Calder-Wang and Kim (2024) study RealPage's algorithmic pricing tool in US multifamily rentals, finding evidence of price coordination through a centralized algorithm. Their setting differs fundamentally from ours: RealPage serves as a shared pricing oracle for landlords of nearly identical apartment units in local oligopolies, creating a hub-and-spoke structure. Airbnb's Smart Pricing, by contrast, provides individualized demand predictions to each host for a highly differentiated product, and operates in a many-seller market. The contrast illustrates that the coordination mechanism requires both product homogeneity and concentrated market structure.

Garcia, Tolvanen, and Wagner (2024, Management Science) document cognitive/adjustment frictions in hotel pricing --- a setting institutionally similar to Airbnb --- and find that the benefit of pricing tools depends on the host's pre-existing strategy quality. This supports our finding that algorithm effects concentrate among sophisticated hosts.

### Literature comparison: Airbnb and platform pricing

| Authors | Year | Platform | Data | Design | Key finding |
|---------|------|----------|------|--------|-------------|
| Huang | 2025 | Airbnb (SF) | Inside Airbnb | Structural model | 85% set near-uniform prices; optimal remedy: platform sets variance, host sets level |
| Foroughifar & Mehta | 2024 | Airbnb (5 cities) | AirDNA + scraped calendars | Structural dynamic adoption | 22% adoption; pessimistic beliefs dominate; SP lowers host revenue |
| Zhang et al. | 2025 | Airbnb | AirDNA | Reduced form + structural | Racial revenue gap persists; differential adoption |
| Calder-Wang & Kim | 2024 | RealPage (rentals) | Proprietary | Structural | Centralized algorithm coordinates apartment prices |
| Garcia et al. | 2024 | Hotels | Revenue mgmt data | Structural | Cognitive frictions; tool benefit depends on strategy quality |
| Ye et al. | 2018 | Airbnb (internal) | Airbnb proprietary | System description | Smart Pricing: GBM demand curve + SVR-inspired loss + personalization |
| **This paper** | 2026 | Airbnb (8 cities) | Inside Airbnb | Sharp ITT + ML heterogeneity | Null on levels; +variance; effects concentrate among sophisticated hosts |

---

## 3. Technology-Skill Complementarity

### 3.1 The canonical framework

The technology-skill complementarity literature, anchored by Autor, Levy, and Murnane (2003, QJE), argues that information technology substitutes for routine tasks while complementing nonroutine analytical and interpersonal tasks. Workers with higher pre-existing skill benefit disproportionately because technology amplifies their comparative advantage. Bresnahan, Brynjolfsson, and Hitt (2002, QJE) extend this to a three-way complementarity between IT, worker skill, and organizational practices.

This framework provides a natural lens for algorithmic pricing: the algorithm substitutes for the routine task of monitoring demand signals and updating prices (which sophisticated hosts already do manually) while complementing the nonroutine task of strategic pricing decisions (interpreting demand forecasts, setting base price levels, choosing which algorithmic suggestions to follow). Hosts with high pre-existing pricing sophistication can better leverage algorithmic recommendations because they understand the economic context in which those recommendations are generated.

### 3.2 Rational inattention as the specific mechanism

Mackowiak and Wiederholt (2009, AER) formalize rational inattention in price-setting: firms with limited information-processing capacity optimally allocate attention to the most important demand signals, leaving some signals unmonitored. Mackowiak, Matejka, and Wiederholt (2023, JEL) provide a comprehensive review. In this framework, a pricing algorithm relaxes the attention constraint by automating signal processing, enabling more frequent and demand-responsive price adjustments. The effect should be larger for hosts who were previously attention-constrained (sophisticated enough to benefit from dynamic pricing but unable to implement it manually at sufficient frequency) and smaller for hosts who were already unconstrained (professional revenue managers) or who lack the complementary knowledge to use dynamic pricing effectively (cognitively constrained hosts in Huang's typology).

### 3.3 Contrast with recent AI-and-labor findings

Brynjolfsson, Li, and Raymond (2025, QJE) find that generative AI in customer service disproportionately benefits *low-skill* workers, compressing the productivity distribution. Our finding --- that algorithmic pricing benefits *high-sophistication* hosts --- represents the opposite pattern. The distinction maps cleanly onto the Autor et al. (2003) task framework: customer service involves predominantly routine interpersonal tasks where AI substitutes for low-skill workers' weaknesses, while dynamic pricing involves predominantly nonroutine analytical tasks where the algorithm complements high-skill workers' existing capabilities.

### 3.4 Supermodularity and formal model predictions

The technology-skill complementarity story can be formalized via supermodularity (Milgrom and Roberts 1990). If the pricing production function exhibits complementarity between algorithm access and host sophistication, the cross-partial derivative is positive: the marginal value of the algorithm is increasing in sophistication. This generates four testable predictions that map to our four core findings:

1. **Null aggregate effect on price levels** (Hazledine 2006): under linear demand, optimal discriminatory prices have the same weighted mean as the optimal uniform price
2. **Positive effect on price variance**: finer time segmentation increases variance without changing the mean
3. **Effects concentrate among sophisticated hosts**: supermodularity of (algorithm, sophistication)
4. **No price spillovers to non-adopting neighbors**: with many sellers and differentiated products, each host's pricing is approximately independent

---

## 4. Methodology: Sharp RDD in Time, Variance Analysis, and ML Heterogeneity

### 4.1 Regression discontinuity in time

Hausman and Rapson (2018) caution that regression discontinuity designs exploiting policy changes in time face unique challenges: seasonal patterns can create spurious jumps, and the standard RD assumption of local smoothness must contend with calendar-driven periodicity. They recommend augmenting the local linear specification with seasonal controls (month-of-year FE, day-of-week FE, holiday indicators) and validating with placebo cutoffs at the same calendar dates in adjacent years. Our design implements this recommendation through a residualization approach: we first estimate and remove seasonal patterns, then apply the RD to residualized outcomes.

Calonico, Cattaneo, and Titiunik (2014, Econometrica) provide the standard framework for MSE-optimal bandwidth selection and bias-corrected confidence intervals. Noack, Olma, and Rothe (2025) generalize covariate adjustment in RDD, showing that flexible (ML-based) adjustment functions produce consistent RD estimates with potentially large efficiency gains --- up to 30% reduction in confidence interval length --- without requiring correct specification of the adjustment function. Their key insight is a global invariance property: the RD moment condition does not depend on the adjustment function, so even misspecified ML adjustments produce valid inference. We adopt their cross-fitted ML adjustment framework, which subsumes the Hausman-Rapson seasonal controls as a special case.

### 4.2 Multi-cutoff RDD

Our design exploits a common platform-wide cutoff (September 1, 2023) across eight US cities, estimating the RDD separately in each market. The multi-city replication provides robustness through leave-one-city-out analysis and cross-city heterogeneity diagnostics, though it does not provide the staggered-timing variation that a multi-cutoff design (Cattaneo, Keele, Titiunik, and Vazquez-Bare 2021) would afford.

### 4.3 ML-based heterogeneity analysis

Our descriptive heterogeneity analysis constructs a latent sophistication proxy via unsupervised learning on pre-treatment pricing behavior. This approach follows the generic ML framework of Chernozhukov et al. (2018) for heterogeneous treatment effects, with cross-fitting to prevent overfitting and bootstrap standard errors (Murphy and Topel 1985 correction) to account for generated-regressor bias. We position this analysis as explicitly descriptive --- "where do effects concentrate?" --- rather than causal, and validate with pre-trend tests.

### 4.4 Staggered adoption and alternative estimators

Callaway and Sant'Anna (2021) develop group-time average treatment effect estimators for staggered designs that are robust to treatment effect heterogeneity across groups and time. While our common-cutoff design does not exploit staggered timing, the year-over-year DiD provides an alternative identification strategy that differences out calendar-date-specific confounders. Black et al. (2022) provide selection tests for the complier population in IV/LATE frameworks, applicable to characterizing which hosts' behavior changes in response to algorithm availability.

---

## 5. Antitrust and Regulatory Context

### 5.1 US enforcement

The US regulatory landscape for algorithmic pricing has evolved rapidly. The DOJ v. RealPage case (filed August 2024, amended January 2025, settled November 2025) established that a centralized algorithmic pricing tool used by competing landlords can constitute an antitrust violation --- though the settlement focused on information-sharing restrictions rather than algorithmic pricing per se. The FTC launched a surveillance pricing study (6(b) orders, July 2024; interim findings January 2025) investigating algorithmic pricing across multiple industries. Harrington (2026, JIE forthcoming) develops a hub-and-spoke theory showing that algorithmic coordination is feasible even with many small firms when a single platform acts as the "hub."

### 5.2 EU regulation

The EU Digital Markets Act (effective May 2023, gatekeeper compliance March 2024) addresses platform market power broadly but does not specifically target pricing algorithms. EU Commission proceedings against Airbnb and Booking.com (January 2026) focused on data-sharing compliance rather than algorithmic pricing. The EU Commission's "Algorithm and Competition" working paper series signals growing interest in algorithmic collusion regulation.

### 5.3 Implications of our findings for regulation

Our findings support a nuanced regulatory approach. The precise null on price levels suggests that blanket restrictions on platform-provided pricing tools are not warranted in many-seller differentiated markets --- the collusion concern that motivates regulation does not arise in our setting. However, the positive effect on price variance raises a different regulatory question: does algorithm-enabled price discrimination harm consumers? Under standard welfare theory (Hazledine 2006; Varian 1985), the welfare effects of third-degree price discrimination are ambiguous --- they depend on whether discrimination opens new markets or merely redistributes surplus. Our evidence that discrimination concentrates among sophisticated hosts suggests the mechanism is more "revenue management by professionals" than "exploitation of consumer inattention," but the consumer welfare implications require further analysis.

---

## 6. Open Questions and Future Directions

1. **Long-run equilibrium effects.** Our design captures short-run effects around rollout timing. Whether algorithm-enabled price discrimination persists, intensifies, or attracts competitive entry in the long run remains open.

2. **Cross-platform algorithm interactions.** What happens when hosts use third-party tools (Beyond Pricing, PriceLabs) alongside or instead of Airbnb's Smart Pricing? If multiple algorithms interact, do platform-level coordination risks emerge even in differentiated markets?

3. **Consumer welfare implications of increased price variance.** Our positive variance finding is consistent with enhanced intertemporal price discrimination. Whether this improves or harms consumer welfare depends on demand elasticity heterogeneity and whether the algorithm enables or forecloses access for price-sensitive travelers.

4. **Generalization beyond Airbnb.** Does the technology-skill complementarity pattern hold for other platform pricing tools (Uber surge pricing, Amazon dynamic pricing, hotel revenue management systems)?

5. **Algorithm design and market conduct.** Ye et al. (2018) describe Smart Pricing as a demand-prediction tool, but its exact objective function is proprietary. How does the algorithm's design --- maximizing bookings vs. revenue vs. host profit --- affect market-level outcomes?
