# Referee Report 3: Antitrust / Policy Economist
**Paper**: Algorithmic Pricing and Market Conduct: Evidence from Airbnb's Pricing Tools
**Venue**: RAND Journal of Economics
**Date**: 2026-03-28

## Summary (1 paragraph)

This paper estimates the market-level effects of Airbnb's September 2023 pricing-tool redesign across eight U.S. cities using a sharp regression discontinuity in time (RDiT) and a complementary year-over-year difference-in-differences design. The authors find small, bandwidth-sensitive price-level increases (0.5--1.9%), suggestive but non-robust increases in within-listing price variance, and descriptive evidence that effects concentrate among hosts with pre-existing pricing sophistication. The two identification strategies yield opposite signs for both outcomes, leading the authors to conclude that the true causal effect is bounded near zero. The paper's central policy claim is that algorithmic pricing effects are market-structure-contingent: the modest Airbnb results contrast with the 38% margin increases Assad et al. (2024) document in German gasoline duopolies, suggesting enforcement should be calibrated to market structure rather than applied uniformly. The paper explicitly engages the DOJ v. RealPage consent decree, the FTC surveillance pricing investigation, and the EU Digital Markets Act.

## Policy Relevance Assessment

This paper arrives at a moment of acute regulatory interest. The FTC's 6(b) surveillance pricing orders (July 2024), the DOJ v. RealPage consent decree (November 2025), and the EU DMA gatekeeper compliance deadline (March 2024) have all raised the operational question this paper addresses: under what market conditions does algorithmic pricing warrant enforcement action? The paper is directly relevant to the FTC investigation's interim findings (January 2025) and would be cited in any future rulemaking or enforcement guidance on algorithmic pricing. Its value to a competition authority lies primarily in the market-structure-contingent framing, which, if accepted, would help agencies prioritize enforcement resources toward concentrated, homogeneous-product markets. However, as detailed below, the evidentiary foundation for the policy recommendations is weaker than the paper's confident framing suggests, and several regulatory dimensions are either underexplored or missing entirely.

## Major Concerns (must address)

### 1. The evidence does not support the strength of the policy claims

The paper's most consequential assertion --- that algorithmic pricing in differentiated-product platform markets produces "at most modest effects" and that enforcement should be calibrated accordingly --- rests on evidence the authors themselves characterize as inconclusive. The RDD and DiD yield opposite signs for both price levels and variance. The authors appropriately note this in the results section but then, in the conclusion, advance a confident "market-structure-contingent enforcement framework" as though the evidence were dispositive. A competition authority reading Section 6 alone would come away with a much stronger impression of the findings than the results warrant.

**Recommendation**: The policy implications section must be rewritten to explicitly condition every enforcement recommendation on the acknowledged identification limitations. Phrases like "our evidence indicates that this theoretical possibility does not materialize" (regarding Harrington 2026 hub-and-spoke coordination) should be softened to "our evidence is consistent with but does not definitively establish that..." A competition authority needs to know the range of plausible effects, including the possibility that the true effect is negative (as the DiD suggests), zero, or modestly positive.

### 2. The Airbnb vs. RealPage design distinction is legally fragile

The paper draws a sharp line: RealPage facilitates coordination via "runtime sharing of competitor rental data" while Airbnb provides "individualized demand predictions" without exposing competitor pricing data. A skilled antitrust lawyer would challenge this distinction on multiple grounds:

- **Endogenous information aggregation.** Airbnb's algorithm is trained on the pricing and booking behavior of all hosts on the platform. Even if an individual host never sees a competitor's price, the algorithm's recommendation embeds an aggregation of competitor behavior. This is precisely the "common agency" structure Harrington (2026) warns about. The fact that the information is laundered through a machine learning model rather than displayed in a dashboard does not necessarily alter its competitive effect. The DOJ's RealPage complaint (paragraphs 47--52) specifically alleges that algorithmic processing of competitor data --- not just raw data sharing --- constitutes the coordinating mechanism.

- **Functional equivalence under Section 1.** Under the hub-and-spoke theory of liability, what matters is not the mechanism by which the hub transmits information but whether the effect is to align competitors' pricing decisions. If Airbnb's algorithm produces convergent pricing recommendations across competing listings in the same micro-market, the legal exposure exists regardless of whether any host sees a competitor's price. The paper does not test for price convergence across competing listings --- only within-listing variance. This is a significant gap.

- **The consent decree's data-aging and geographic-aggregation provisions** (Federal Register, 91 FR 2592) were designed to prevent algorithms from using real-time, disaggregated competitor data as inputs. These provisions would apply equally to any platform algorithm that uses current competitor pricing data as training inputs, regardless of whether the output is framed as a "demand prediction." The paper should discuss whether Airbnb's algorithm would survive scrutiny under the RealPage consent decree's analytical framework.

**Recommendation**: Add a subsection explicitly testing for cross-listing price convergence in local micro-markets (e.g., within census tract or ZIP code by property type). If Smart Pricing causes competing listings to set more similar prices, the RealPage analogy strengthens considerably regardless of the mechanism. Also, discuss in detail whether Airbnb's training data pipeline would satisfy the RealPage consent decree's data-aging and aggregation requirements.

### 3. Small percentage effects aggregate to substantial consumer harm at platform scale

The paper dismisses the 0.5--1.9% price increase as "economically modest," noting it implies only "$1.50--$2.85" per night at the median price. This framing is inconsistent with how antitrust authorities evaluate consumer harm:

- Airbnb reported 448.6 million nights and experiences booked globally in 2023 (Airbnb 10-K, FY2023). Even restricting to the eight study cities and applying the lower-bound 0.5% estimate to a $150 median price, the aggregate transfer from consumers to hosts is on the order of tens of millions of dollars annually. At the upper bound (1.9%), this scales into the hundreds of millions.

- The DOJ's RealPage complaint alleged consumer harm from rent increases of approximately 1--4% --- a range that overlaps substantially with this paper's estimates. The DOJ did not dismiss these as "economically modest."

- The FTC's merger guidelines (2023 revision) define a "small but significant and non-transitory increase in price" (SSNIP) as 5%. The paper's estimates fall below this threshold, but the SSNIP test applies to a hypothetical monopolist's unilateral incentive, not to the aggregate consumer harm from a coordinated price increase. The relevant comparison for enforcement purposes is total consumer surplus loss, not per-night price change.

**Recommendation**: Add a back-of-the-envelope aggregate harm calculation. Discuss explicitly how the estimated effects compare to harm thresholds in recent enforcement actions (RealPage, surveillance pricing). Acknowledge that the per-night framing may be misleading from an enforcement perspective.

### 4. The hub-and-spoke discussion (Harrington 2026) is inadequate

The paper engages Harrington (2026) in a single paragraph and dismisses the hub-and-spoke risk on the grounds that "the spokes cannot coordinate on prices for fundamentally dissimilar listings." This is insufficient for three reasons:

- **Harrington's model does not require product homogeneity for the hub to raise prices.** The hub can implement supra-competitive pricing by solving the platform's joint optimization problem, even with differentiated products, as long as the algorithm internalizes the cross-listing demand externalities. Airbnb's algorithm, which is trained to maximize platform revenue (booking probability times price, times service fee), has exactly this incentive structure. The paper should discuss whether Airbnb's objective function --- platform revenue maximization rather than individual host profit maximization --- creates an alignment of interests that functions as a coordination device even absent product homogeneity.

- **The paper does not discuss the "raising rivals' costs" variant of hub-and-spoke.** If Smart Pricing systematically recommends higher prices to hosts who would otherwise undercut, the algorithm functions as a facilitating device even if it never achieves full coordination. The literature on facilitating practices (Salop 1986; Hay 2006) would be relevant here.

- **The 22% adoption rate is not reassuring in the hub-and-spoke context.** Harrington (2026) shows that a hub can sustain coordination even with partial spoke participation, as long as the hub's recommendations are publicly observable (which they are, via listed prices) and non-participating spokes best-respond to the posted prices of participating spokes. The paper should model or at least discuss how equilibrium prices change as adoption rates increase from 22% toward saturation.

**Recommendation**: Devote a full subsection to the hub-and-spoke theory as applied to Airbnb. Discuss the platform's objective function (platform revenue maximization) and whether it creates a structural incentive for the algorithm to internalize cross-listing externalities. Model or discuss the adoption-rate threshold at which coordination risks become material.

### 5. Third-party pricing tools are mentioned but not analyzed

The paper identifies Beyond Pricing, PriceLabs, and Wheelhouse as potential confounders and as potential hub-and-spoke risks, but does not analyze them. This is a critical gap for enforcement purposes:

- Third-party tools serve competing hosts across multiple platforms (Airbnb, Vrbo, Booking.com), creating a cross-platform coordination channel that platform-specific tools do not. This is structurally analogous to RealPage serving competing landlords.

- If third-party tool adoption changed around the September 2023 cutoff (e.g., because hosts responded to the Airbnb redesign by switching to or from third-party tools), the treatment effect is confounded in a way that cannot be signed a priori.

- The FTC's surveillance pricing 6(b) orders targeted third-party revenue management tools in the short-term rental space. The paper should discuss how its findings relate to the specific information the FTC requested.

**Recommendation**: At minimum, discuss the third-party tool landscape in a dedicated subsection. Ideally, attempt to measure third-party tool usage (e.g., via pricing pattern signatures or API integration markers in listing data) and test whether it confounds or amplifies the estimated effects.

## Minor Concerns

### 1. The "market-structure-contingent enforcement framework" is less novel than presented

Competition authorities have long recognized that collusion risk depends on market structure. The DOJ/FTC Horizontal Merger Guidelines (Section 7.2) explicitly list market concentration, product homogeneity, and pricing transparency as factors facilitating coordinated effects. The EC's Guidelines on Horizontal Cooperation Agreements (2023 revision) similarly condition algorithmic pricing scrutiny on market structure. The paper's contribution is empirical --- showing that the magnitude differs across settings --- not conceptual. The framing should reflect this.

### 2. The beta period (May--August 2023) is a threat to identification

The paper acknowledges a beta period starting May 3, 2023, during which early-access hosts could use the redesigned tools. At the widest bandwidth (plus/minus 90 days), the pre-period extends back to June 3 --- meaning nearly the entire pre-period overlaps with the beta. If sophisticated, early-adopting hosts changed pricing behavior during the beta, the pre-period is contaminated. The paper should report estimates excluding the beta period entirely (i.e., using pre-beta observations as the control period) and discuss how partial pre-treatment adoption affects the ITT interpretation.

### 3. The paper should discuss remedial options more concretely

The conclusion identifies three areas for "ongoing regulatory attention" but does not discuss specific remedial mechanisms. A policy referee expects engagement with questions like: Should platforms be required to disclose their pricing algorithm's objective function? Should there be a firewall between competitor data and algorithmic recommendations? Should adoption-rate thresholds trigger enhanced scrutiny? The RealPage consent decree provides a template --- the paper should discuss which of its provisions (if any) would be appropriate for platform-provided tools like Smart Pricing.

### 4. Posted prices vs. transaction prices

The paper acknowledges that it observes posted calendar prices rather than realized transaction prices. From an enforcement perspective, this distinction matters: if the algorithm raises posted prices but simultaneously increases discounting (via last-minute deals, negotiated rates, or promotional codes), the consumer harm may be smaller than the posted-price analysis suggests. Conversely, if the algorithm reduces discounting, the harm may be larger. The paper should discuss this asymmetry and its implications for enforcement.

### 5. The leave-one-city-out analysis reveals fragility

Dropping Los Angeles or New York City --- the two largest markets by listing count --- flips the pooled sign to negative. This means the positive pooled estimate is driven by mid-sized markets (Chicago, Seattle) with anomalously large effects. A competition authority would need to understand why the algorithm's effect varies so dramatically across cities before applying the findings to enforcement decisions. The paper should explore whether the city-level heterogeneity correlates with observable market-structure variables (concentration, chain-operator share, third-party tool penetration).

### 6. No discussion of dynamic effects or long-run equilibrium

The paper estimates effects within a 90-day window of the rollout. Algorithmic collusion models (Calvano et al. 2020; Brown and MacKay 2025) predict that coordination emerges gradually as algorithms learn to signal and punish. The short estimation window may miss the economically important long-run effects. The paper should acknowledge this limitation and discuss whether longer-run data (now available, given the 2.5 years since rollout) could resolve the question.

## Missing Policy Dimensions

### 1. Consumer welfare beyond price levels

The paper focuses exclusively on price effects. Algorithmic pricing may also affect non-price dimensions of competition: listing quality, host responsiveness, cancellation policies, and platform lock-in. The FTC's surveillance pricing investigation explicitly asks about non-price effects. The paper should at least acknowledge these dimensions.

### 2. Distributional effects and equity

The finding that effects concentrate among "sophisticated" hosts has distributional implications the paper does not explore. If algorithmic pricing tools primarily benefit professional property managers and multi-listing hosts at the expense of individual hosts and guests seeking affordable accommodations, there is an equity dimension relevant to both FTC consumer protection and HUD fair housing enforcement. Zhang et al. (2025) document racial revenue gaps associated with differential algorithm adoption --- the paper should discuss whether its sophistication proxy correlates with host demographics or professionalization.

### 3. International regulatory context is thin

The EU DMA is mentioned once in the conclusion. The paper does not discuss:
- The UK CMA's investigation into algorithmic pricing in the online hospitality sector (commenced 2024).
- The EU's proposed AI Act provisions on high-risk AI systems, which may apply to algorithmic pricing tools that affect consumer welfare.
- Australia's ACCC digital platform inquiry, which flagged algorithmic pricing as a concern.
- The divergent enforcement approaches: the U.S. relies on case-by-case litigation (RealPage), the EU on ex ante regulation (DMA), and the UK on a hybrid model (CMA digital markets unit). The paper's market-structure-contingent framework has different implications under each regime.

**Recommendation**: Add a paragraph or subsection comparing how the paper's findings would translate into enforcement action under U.S., EU, and UK frameworks.

### 4. Interaction between algorithmic pricing and platform market power

Airbnb is a dominant platform in the short-term rental market. The paper does not discuss whether algorithmic pricing tools function as a tying or self-preferencing mechanism that reinforces platform market power. Under the DMA's Article 6(5) (prohibition on self-preferencing), a gatekeeper's pricing algorithm that steers hosts toward platform-preferred pricing strategies could face scrutiny independent of any collusion theory. This dimension is entirely absent from the paper.

### 5. Algorithmic transparency and auditability

The paper cannot observe the algorithm's internal mechanics, training data, or objective function. This is not merely a data limitation --- it is a policy issue. The RealPage consent decree requires algorithmic transparency (disclosure of data inputs, model logic, and output distribution). The paper should discuss whether its findings support or undermine the case for mandatory algorithmic transparency in platform pricing.

## Overall Recommendation

**Revise and Resubmit (Major Revision)**

This paper addresses a first-order policy question at a moment of intense regulatory activity, and the empirical setting is well-chosen. The market-structure-contingent framing is a genuine contribution to the enforcement toolkit, even if the underlying concept is not new. However, the paper cannot be published in its current form for three reasons. First, the policy conclusions substantially overreach the evidence: the RDD and DiD disagree on sign for both outcomes, yet the conclusion section reads as though the paper has established that algorithmic pricing is benign in differentiated markets. A competition authority that relied on these findings to deprioritize enforcement in platform markets would be making a decision unsupported by the paper's own results. Second, the paper's engagement with the hub-and-spoke theory, third-party pricing tools, and aggregate consumer harm is too superficial for a policy-oriented outlet like the RAND Journal. Third, the absence of cross-listing convergence tests leaves the most enforcement-relevant question --- whether the algorithm coordinates prices across competing listings in local micro-markets --- entirely unanswered.

A revised version that (a) tempers the policy language to match the evidentiary uncertainty, (b) adds cross-listing convergence analysis, (c) engages seriously with hub-and-spoke theory and aggregate harm calculations, and (d) discusses remedial frameworks with the specificity expected by a policy audience would be a strong candidate for publication. The empirical design is creative, the data are rich, and the question is important. The paper needs to be as careful with its policy claims as it is with its econometrics.
