# Huang (2021/2025) -- Pricing Frictions and Platform Remedies: The Case of Airbnb

## Citation

Huang, Yufeng. 2021 (revised 2025). "Pricing Frictions and Platform Remedies: The Case of Airbnb." SSRN Working Paper No. 3767103. University of Rochester Simon Business School. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3767103

Status: Working paper (not yet published in a journal as of the version reviewed). Originally posted January 2021; revised versions through at least September 2025. The version read in detail is the October 2021 draft hosted at Chicago Booth (QME 2021 conference paper).

---

## Research question

What is the equilibrium consequence of sellers' pricing frictions on Airbnb, and can alternative platform designs (pricing algorithms, interface redesigns, platform-assisted pricing) ameliorate these frictions? The paper asks both how costly it is that amateur hosts fail to price-discriminate across nights and over time, and whether the platform's revenue-maximizing algorithm is the right remedy given misaligned incentives between the platform and sellers.

---

## Identification strategy

**Structural model.** The paper estimates a three-part structural equilibrium model:

1. **Demand side:** Logit demand for capacity-constrained, differentiated listings with two consumer segments (early vs. late bookers) arriving at Poisson rates that vary by time-to-check-in, day-of-week, and month. Uses a nested fixed-point algorithm (in the spirit of Berry et al. 1995 / Goolsbee and Petrin 2004 / Chintagunta and Dube 2005) combined with sparse-demand models to handle ~33,000 listing-quarter fixed effects. Average price elasticity: -2.51 (validated against Jeziorski and Michelidaki 2019 experimental estimate).

2. **Supply side -- pricing:** Sellers are a mixture of two types: (a) *dynamic pricers* who solve a finite-horizon dynamic pricing problem subject to Calvo-style price-adjustment costs (probability mu_j of adjusting each month), and (b) *cognitively constrained* sellers who set non-dynamic (time-invariant) prices with limited "price bins" (rho_j price points per quarter). Observed prices are a weighted average of the two types' optimal prices (weight theta_j). Parameters estimated by GMM at the cluster level (150 segments via Bonhomme et al. 2019 hierarchical clustering).

3. **Participation:** Static entry/exit decision each quarter based on expected quarterly profit vs. fixed costs (opportunity cost of listing on Airbnb vs. long-term rental).

**Key identification variation:**
- *Price-adjustment costs vs. cognitive constraints:* Exploits the 2019 introduction of "last-minute discounts" (automated price reduction near check-in). After this interface change, the fraction using dynamic pricing rose from 36% to 45%, but 55% still did not -- separating menu-cost-constrained sellers from cognitively constrained ones.
- *Price endogeneity:* Novel "uniform-pricing instrument" -- because most sellers set uniform prices across unrelated nights (due to frictions), prices of nights in *different quarters* from the focal night serve as instruments. Excluded-variable F-statistic ~10,000. This corrects for night-specific demand shocks that lagged-price IVs miss.
- *Within-seller variation:* Table 2B shows that scaling up (adding listings) does NOT increase price flexibility within seller, ruling out scale economies and learning-by-doing; pricing sophistication is a persistent seller type.

---

## Data

- **Source:** Inside Airbnb (insideairbnb.com) -- publicly available scraped data under CC0 license. NOT proprietary Airbnb data.
- **Market:** San Francisco
- **Sample period:** ~54 months, approximately early 2015 through mid-2020
- **Sample construction:** Listings with min-stay <= 3 nights; private rooms, studios, 1BR, and 2BR apartments (86% of SF listings); sellers who block no more than 25% of nights (full-time sellers).
- **Sample size:** 18,054 listings operated by 12,856 sellers. 30,864,535 listing-night-sampling-date observations. Structural model uses 75% random subsample (~33,354 listing-quarters; ~16.7 million observations for demand).
- **Key variables:** Nightly prices (observed on calendar), availability/booking status, listing characteristics, seller identity and portfolio size.
- **Counterfactual period:** May 2015 -- December 2017 (pre-SF short-term rental regulation).

---

## Key findings

1. **Pricing frictions are pervasive and bimodal.** Most sellers (~85%) set highly inflexible prices: median within-listing std. dev. of log price is only 5% (about $7 at the median price of $150). After conditioning on weekend and month, residual price variation drops to 0.5%. Only ~15% of listings show algorithm-like flexible pricing. About half of sellers are cognitively constrained (theta < 0.5) and do not set dynamic prices at all.

2. **Frictions are costly: 14% consumer welfare loss, 0-15% seller profit loss.** In the first-best counterfactual (no frictions), consumer surplus rises 14%, median seller profit rises 3.8% ($2,350 to $2,440/quarter), and the 5-95th percentile range of seller profit gains is [0%, 15%]. Platform revenue rises only 2.5%, explaining the platform's limited incentive to fix frictions.

3. **The platform's revenue-maximizing algorithm ("Smart Pricing") hurts sellers.** Because it ignores sellers' positive marginal costs (median $38/night, IQR [$24, $68]), the algorithm sets prices 26% below baseline and 18% below first-best. Result: 56% of sellers lose, 8% earn negative profits, 25% see profits drop by 19%+, and seller exit rises. But consumers gain 47% and platform revenue rises 1.7%. This explains widespread host resistance to Smart Pricing.

4. **A better interface alone is insufficient.** Even an "ideal" interface that eliminates all price-adjustment costs (mu=1, rho=31) delivers only one-third of the potential gains because the dominant friction is cognitive constraints, not menu costs. Median seller profit rises only 1.3%.

5. **Platform-assisted pricing (variance, not levels) nearly achieves first-best.** The key counterfactual: the platform sets the price *variation* (adjustment function across nights and time) but the seller retains the right to set the base *price level*. This design achieves prices close to the first-best. Consumer surplus is 3.2% above first-best (due to slightly lower prices); median seller profit is 3.0% above baseline; 62% of sellers gain and only 9% lose; virtually no seller exit. This design leverages the platform's informational and technological advantages while respecting sellers' knowledge of their own costs.

---

## Relevance to our paper

This paper is the primary theoretical and empirical motivation for the "pricing frictions" that our algorithm is supposed to alleviate. Key connections:

**Supports the technology-skill complementarity framing:**
- Huang documents a sharp bimodal distribution: ~15% "sophisticated" (likely algorithm-using) sellers vs. ~85% who set near-uniform prices. This maps directly onto our heterogeneous treatment effects story: the algorithm should differentially benefit hosts who have the skill to use it effectively.
- Multi-listing (professional) sellers are more sophisticated pricers (Table 2A), but this is a persistent type difference, not driven by scale or learning (Table 2B). This is consistent with our finding that the algorithm complements pre-existing host skill rather than substituting for it.

**Critically relevant to the variance vs. levels distinction:**
- Huang's Counterfactual 3 ("platform-assisted pricing") shows that the optimal remedy is for the platform to set price *variation* (across nights and over time) while sellers set *price levels*. This exactly matches our empirical finding: null effect on price levels + positive effect on price variance.
- The paper shows that price levels should be higher than the revenue-maximizing algorithm sets them, because sellers have positive marginal costs the algorithm ignores. This rationalizes why the algorithm does not (and should not) move levels.
- First-best prices have higher dispersion across nights (std dev rises from 4% to 6%) and steeper dynamic discounts (last-month discount rises from 2% to 30%). The algorithm's value-add is in enabling this variance, not in shifting the mean.

**Magnitude benchmarks for our paper:**
- 14% consumer welfare loss from frictions; 0-15% seller profit loss
- Only 15% of listings price flexibly at baseline
- Median marginal cost of hosting: $38/night
- Average price elasticity: -2.51

---

## Methodological lessons

1. **Nested fixed-point algorithm for large-scale demand estimation** with capacity constraints and many product-time fixed effects. Combines BLP-style random coefficients with sparse-demand models (Williams 2021, Pan 2019). Scalable to large differentiated-product datasets.

2. **"Uniform-pricing" instrument for price endogeneity.** Uses prices of far-apart nights (in different quarters) as instruments for the focal night's price, leveraging the fact that pricing frictions make these co-move despite uncorrelated demand. F-stat ~10,000. Novel and potentially applicable to other markets with uniform/sticky pricing.

3. **Bonhomme et al. (2019) clustering for heterogeneous supply-side estimation.** Clusters listings into 150 segments based on observables (prices, portfolio size, discount behavior), then estimates supply parameters by GMM within each cluster. Avoids strong distributional assumptions on seller heterogeneity.

4. **Calvo-style price adjustment costs** adapted from macro to micro IO context. Mu_j (probability of price adjustment) is heterogeneous across sellers and separately identified from cognitive constraints using the 2019 interface change.

5. **Counterfactual design comparing multiple platform remedies** (first-best, revenue-max algorithm, ideal interface, platform-assisted pricing) -- useful template for policy evaluation in platform markets.

---

## Limitations acknowledged

1. **Single market (San Francisco).** Results may not generalize to other cities with different tourism patterns, regulations, or competitive structures.

2. **Inside Airbnb data limitations.** Monthly scraping frequency creates truncation/missing-price problems requiring interpolation. Cannot directly observe booking dates or the exact transaction price at time of booking. No direct measure of algorithm adoption (inferred from price patterns).

3. **The 2021 version is a working paper** (possibly revised by 2025 but not yet published in a peer-reviewed journal as of the version reviewed).

4. **Cognitive constraints are a residual category.** After accounting for price-adjustment costs, the remaining friction is labeled "cognitive," but the paper cannot directly measure cognitive ability or distinguish it from other sources (e.g., inattention, satisficing, delegation to management companies).

5. **Multi-product pricing is simplified away.** The model assumes sellers price each listing independently, ignoring potential cannibalization across a multi-listing portfolio.

6. **Platform-assisted pricing counterfactual uses crude adjustment functions** (averages of first-best ratios by segment-market-time). The paper acknowledges this is a lower bound and that optimizing the adjustment functions is computationally prohibitive.

7. **Does not model the algorithm adoption decision.** Takes pricing behavior as given rather than modeling why sellers choose (or don't choose) to use Smart Pricing or third-party tools. Our paper fills this gap.

8. **No direct evidence on third-party pricing tools** (e.g., Beyond Pricing, PriceLabs). The paper notes these exist but cannot identify users. Our paper directly studies the adoption and effect of such tools.

---

## DEEP READ (added 2026-03-22)

*Based on the October 3, 2021 draft hosted at Chicago Booth (QME 2021 conference paper), 60 pages including appendices.*

### Model structure

**Demand side.** Two consumer segments (k = 1, 2) arrive via Poisson process at the San Francisco Airbnb market. Consumer i of type k looking for night tau in zipcode m has utility:

> u_{ij,tau} = delta_{j,q(tau)} + alpha^k * log((1+r) * p_{j,tau,t(i)}) + xi_{j,tau,t(i)} + epsilon_{ij,tau}

where delta_{j,q(tau)} are listing-quarter fixed effects (33,354 of them), alpha^k is the segment-specific log-price coefficient, r is the platform service fee rate, p is the nightly price, xi captures unobserved demand shocks (parameterized as sigma * eta via a control function), and epsilon is Type-1 extreme value. The outside option is booking a hotel. Consumers within a zipcode choose among available listings via logit. Arrival rates lambda^k_{m,tau,t} depend on time-to-check-in, day-of-week, month-of-year, and holiday status (Equation 7). Segment 1 (early bookers) is more price-sensitive (alpha^1 = -3.214) than Segment 2 (late bookers, alpha^2 = -2.695). Average price elasticity: -2.51.

Key innovation: a nested fixed-point algorithm collapses binary listing-night-month occupancy outcomes to listing-quarter occupancy *rates*, yielding a closed-form expression (Equation 8) that can be solved for the 33,354 delta_{jq}'s given trial parameters. This makes BLP-style estimation feasible on 16.7 million observations.

**Supply side -- dynamic pricing type.** Each listing j's observed price is a mixture of two pricing modes:

> p_{j,tau,t} = theta_j * p^{dynamic}_{j,tau,t} + (1 - theta_j) * p^{non-dynm}_{j,tau}

where theta_j in [0,1] is the listing's propensity for dynamic pricing (estimated; most listings cluster near 0 or 1).

*Dynamic pricing (theta -> 1):* The seller solves a finite-horizon dynamic programming problem. The static flow profit for night tau rented in month t is:

> pi_{j,tau,t}(p, omega) = q_{j,tau,t}(p, omega) * (p * (1 - f) - c_j)

where f = 0.03 is the platform's seller fee and c_j is the listing's marginal cost. The seller faces Calvo-style price-adjustment frictions: with probability mu_j each month she can reset the price; with probability (1 - mu_j) the previous price carries over. She maximizes:

> max_p pi(p, omega) + (1 - q(p, omega)) * E[V_{tau,t+1}(p, omega) | p, omega]

balancing current profit against the option value of selling the night to a future (possibly higher-WTP) customer, solved by backward induction.

*Non-dynamic pricing (theta -> 0):* Cognitively constrained sellers set time-invariant prices. They divide the quarter's 90 nights into K_{jq} consecutive bins (K drawn from Poisson(rho_j)), set one price per bin, and maximize expected profit over the bin's nights:

> p_j^k(K) = max_p sum_{tau in bin k} (p - c_j) * E[occupancy_{j,tau}(p)]

Low rho_j means few price points and highly uniform prices; high rho_j means flexible (but still time-invariant) cross-night prices.

**How pricing friction is modeled formally:** It is a *hybrid* of two mechanisms: (a) Calvo-style stochastic price-adjustment costs (probability mu_j of adjusting each period -- adapted from macro sticky-price models, Calvo 1983), and (b) cognitive constraints captured by the non-dynamic pricing mode with limited price bins. This is *not* rational inattention in the Sims (2003) sense; rather, it is a behavioral mixture model where some sellers simply do not engage in dynamic optimization at all. The 2019 last-minute discount interface change identifies the two mechanisms separately.

**Host's objective function:** Maximize expected quarterly profit net of fixed costs:

> Pi_{jq} = E[sum_{tau in q} sum_{t=1}^{12} (prod_{t'<t}(1-q_{j,tau,t'})) * q_{j,tau,t} * (p_{j,tau,t}*(1-f) - c_j)]

subject to participation constraint Pi_{jq} - F_{jq} > 0, where F_{jq} is the fixed/opportunity cost (parameterized as a function of segment fixed effects, post-regulation indicator, distance to Union Square).

**Platform's objective function:** Maximize total booking revenue (since it collects a fixed ad valorem fee = 3% from sellers + 14% from consumers in SF). Formally, the platform wants seller-*revenue*-maximizing prices, which ignores sellers' marginal costs c_j. This misalignment is the core tension: the platform wants p to maximize q*p, while the seller wants p to maximize q*(p*(1-f) - c).

### Counterfactual details

All counterfactuals use the period May 2015 -- December 2017 (pre-SF regulation). Results are from Table 6 and Table 7:

**Counterfactual 0: First-best (no frictions).** Set mu_j = 1, theta_j = 1, rho_j irrelevant for all listings.
- Median last-month price: $120.49 (baseline: $133.66) -- 10% lower
- Price dispersion across nights (std of log price): 0.06 (baseline: 0.04) -- 50% higher
- Last-month discount: -30% (baseline: -2%) -- massive increase in dynamic pricing
- Occupancy rate: 0.77 (baseline: 0.73)
- Median seller quarterly profit: $2,440 (baseline: $2,350) -- up 3.8%
- Seller participation rate: 1.00 (baseline: 1.00)
- Total platform revenue: $2.42m (baseline: $2.36m) -- up 2.5%
- Consumer surplus: 4.69 utils (baseline: 4.11) -- up 14%
- Within-seller profit changes: 1% lose, 69% gain; 5th-95th percentile of gains = [0%, 15%]

**Counterfactual 1: Revenue-maximizing algorithm (Smart Pricing for all).**
- Median last-month price: $99.27 -- 26% below baseline, 18% below first-best
- Price dispersion: 0.09 -- higher than first-best (algorithm exploits demand variation aggressively)
- Last-month discount: -38%
- Occupancy rate: 0.90 -- very high (low prices fill rooms)
- Median seller quarterly profit: $2,160 -- down 8% from baseline
- Seller participation rate: 0.92 -- 8% of sellers exit
- Platform revenue: $2.40m -- up 1.7% from baseline
- Consumer surplus: 6.03 utils -- up 47% from baseline, up 29% from first-best
- Within-seller profit changes: 8% earn negative profits, 56% lose relative to baseline, 25% see profits drop by 19%+ (from Table 7: 5th percentile profit change = -1.00, i.e., total wipeout). Only 31% gain.

**Counterfactual 2: Ideal flexible interface (eliminate all price-adjustment costs).**
- Sets mu_j = 1 and rho_j = 31 for all listings, but keeps theta_j at estimated values (cognitive constraints remain).
- Median last-month price: $130.26
- Price dispersion: 0.05 (barely higher than baseline)
- Last-month discount: -10% (steeper than baseline's -2%, but far from first-best's -30%)
- Occupancy rate: 0.74
- Median seller quarterly profit: $2,380 -- up 1.3% from baseline (only 1/3 of potential gain)
- Participation rate: 1.00
- Platform revenue: $2.38m -- up 0.8%
- Consumer surplus: 4.23 utils -- up 2.9%
- Within-seller: 0% earn negative, 0% lose, 40% gain; median profit increase = 1%
- **Key takeaway:** Even an ideal interface achieves only ~1/3 of potential gains because the dominant friction is cognitive constraints, not menu costs.

**Counterfactual 3: Platform-assisted pricing (platform sets variation, host sets level).**
- Price is: p_{j,tau,t} = p_bar_{j,q(t)} * (1 + a_{m,l(j),tau,t})
- The platform commits to a price-adjustment function a_{m,l,tau,t} (computed as average ratio of first-best to uniform prices, by market m, listing type l, night tau, and time t). Sellers then set only the quarterly base price p_bar.
- Median last-month price: $118.49 -- close to first-best ($120.49), slightly lower
- Price dispersion: 0.06 -- matches first-best exactly
- Last-month discount: -29% -- nearly matches first-best's -30%
- Occupancy rate: 0.79 -- close to first-best (0.77), slightly higher due to slightly lower prices
- Median seller quarterly profit: $2,420 -- up 3.0% from baseline (vs. 3.8% in first-best)
- Participation rate: 1.00 -- virtually no exit
- Platform revenue: $2.42m -- matches first-best
- Consumer surplus: 4.84 utils -- 3.2% *above* first-best (because prices are slightly lower than first-best due to the crude adjustment function)
- Within-seller: 0% earn negative, 9% lose, 62% gain; 5th-95th = [-2%, 14%]; median gain = 2%

**What happens to price levels vs. price variance in Counterfactual 3:**
- Price *variance* (dispersion across nights) rises from 0.04 to 0.06 -- a 50% increase, matching first-best exactly. The platform's adjustment function a_{m,l,tau,t} introduces the cross-night and time-to-check-in variation that cognitively constrained hosts cannot produce on their own.
- Price *levels* are set by sellers. Median last-month price ($118.49) is slightly below first-best ($120.49) and well below baseline ($133.66). The level drop relative to baseline comes from the dynamic discount path (last-month discount goes from -2% to -29%), not from the platform pushing levels down. Sellers retain the right to set base prices that internalize their marginal costs.
- **Magnitudes for our paper:** The adjustment function a_{m,l,tau,t} is computed as the ratio of first-best prices to counterfactual uniform prices, averaged by segment/market/time. This is explicitly described as "crude" (footnote 26) and a lower bound -- optimizing a_{m,l,tau,t} would yield even better results but is computationally prohibitive.

**Mapping to our Smart Pricing setting:** Our empirical finding (null effect on price levels, positive effect on price variance) is highly consistent with Counterfactual 3. Smart Pricing availability changes the *variance* of prices (by enabling dynamic adjustments across nights and over time) without necessarily shifting the *level* -- because hosts can override the base price. Huang's structural results provide the welfare foundations: this design nearly achieves first-best and benefits most sellers.

### Host heterogeneity

**How Huang measures pricing sophistication:**
1. *Structural parameters:* theta_j (propensity for dynamic pricing, 0 to 1), mu_j (probability of price adjustment per month, 0 to 1), rho_j (expected number of distinct price points per quarter for non-dynamic sellers). These are estimated by GMM within 150 Bonhomme et al. (2019) clusters.
2. *Clustering variables:* For each listing j, the cluster assignment uses: (i) estimated demand intercept (delta), (ii) number of listings operated by the owner, (iii) median price, (iv) price discount in last two months before check-in, and (v) difference in last-month discount before vs. after the 2019 interface change. These are used in hierarchical clustering to form 150 segments.
3. *Reduced-form measures:* (i) std(log price) across nights within a listing-sampling date, (ii) percent last-month discount (ratio of last-month to first-month price minus 1), (iii) percent summer price premium.

**Distribution -- what fraction are "sophisticated" vs. "simple":**
- theta_j: 48% of listings have theta > 0.5 (mostly theta -> 1), meaning they *can* set dynamic prices. The remaining 52% are cognitively constrained (theta -> 0) and set non-dynamic prices.
- Of the 48% with theta > 0.5 (dynamic pricers): 43% always adjust prices (mu -> 1); 31% never adjusted before the 2019 feature (mu -> 0 pre-2019, started using last-minute discounts after); 26% have intermediate mu.
- rho_j (for non-dynamic sellers): average = 5.3 price points/quarter. 74% can set 5 or fewer price points. This means most non-dynamic sellers set very few distinct prices across a quarter's 90 nights.
- Only ~15% of listings display algorithm-like fully flexible pricing (top-5% residual price variation after conditioning on weekend and month).

**Correlation with observable characteristics (Table 5):**
- **Multi-listing status (log number of listings):** The single strongest predictor. One std dev increase in log(#listings) explains 0.23 std dev of theta_j, 0.07 std dev of c_j, 0.11 std dev of rho_j, and -0.01 std dev of mu_j. Multi-listing sellers are substantially more likely to be dynamic pricers.
- **Superhost status:** Negatively correlated with theta (-2.0 pp) and rho (-0.5), suggesting superhosts are *not* more sophisticated pricers -- they may succeed through quality/reviews rather than pricing.
- **Instant booking:** Negatively correlated with theta (-1.6 pp), suggesting instant-booking listings (which are more automated in other ways) are not necessarily dynamically priced.
- **Flexible cancellation:** Negatively correlated with theta (-2.7 pp). Listings with flexible cancellation (more consumer-friendly) tend to have less dynamic pricing.
- **Experience (years on Airbnb):** Appendix Table 3 shows that within-seller changes in experience have essentially zero effect on pricing sophistication. More experienced sellers price higher (reputation effect) and have lower occupancy, but do NOT become more flexible pricers over time.
- **Scale (within-seller):** Table 2B shows that when a seller adds listings, there is virtually no change in price flexibility (coefficients on 2-listing, 3-5-listing, 6+-listing dummies are all near zero and mostly insignificant with seller FEs). Sophisticated pricing is a persistent type, not driven by scale economies or learning.

**Comparison to our ML-constructed latent proxy:** Huang's approach uses structural estimation within ex-ante clusters, producing listing-level structural parameters (theta, mu, rho, c). Our approach constructs a latent sophistication proxy from observed pricing patterns using ML. The key similarity is that both treat pricing sophistication as a persistent host type that correlates with multi-listing status but is not caused by scale. The key difference is that Huang recovers structural primitives (enabling welfare calculations), while our ML proxy is a reduced-form object used for heterogeneous treatment effect estimation.

### Data details

- **Source:** Inside Airbnb (insideairbnb.com), publicly available under CC0 1.0 Universal License.
- **Market:** San Francisco only.
- **Time period:** ~54 months, approximately early 2015 through mid-2020. Counterfactual period restricted to May 2015 -- December 2017 (pre-SF short-term rental regulation).
- **Number of listings:** 18,054 listings operated by 12,856 sellers.
- **Number of observations:** 30,864,535 listing-night-sampling-date observations (full sample). Structural model uses 75% random subsample: 33,354 listing-quarters, ~16.7 million observations for demand estimation.
- **Sample selection criteria:** (1) Minimum stay <= 3 nights (excludes weekly/long-term rentals; 67% of all listings satisfy this). (2) Private rooms (38% of SF listings), studios and 1BR apartments (31%), and 2BR apartments (17%) -- totaling 86%. (3) Seller blocks no more than 25% of nights in a listing-year (full-time sellers; drops 25% of listings).
- **Price variable:** Calendar prices -- the price listed for each future night as observed at each monthly scrape date. These are *posted* prices, not transaction prices. Booked-night prices are missing (the listing disappears from the calendar); Huang interpolates these using pricing-policy functions estimated from observed (non-missing) prices. For listings with uniform prices, the missing price equals the uniform price. For listings with simple policies (base + weekend surcharge, or base + month effects), the policy is estimated from non-missing nights and applied. The interpolation covers 65% of missing prices; the remaining 35% use last-observed price. Only non-missing (observed) prices are used for supply-side estimation and descriptives; interpolated prices enter demand estimation.
- **Inside Airbnb vintage/scrape dates:** Not explicitly stated. The data covers 96 cities worldwide; Huang uses only San Francisco. Scraping frequency is approximately monthly. Specific scrape dates are not reported, but the data spans early 2015 to mid-2020.
- **Key summary statistics (Table 1):**
  - Mean total listings per seller: 4.0; median: 1; 75th percentile: 3; 95th percentile: 11
  - Mean years of experience: 3.6; median: 3.5
  - Mean nights supplied: 329/365; median: 360
  - Mean occupancy rate: 0.612; median: 0.693
  - Mean price: $188; median: $150; IQR: [$108, $235]
  - Std of log price across nights: mean 0.076; median 0.050 (~$7 at median price)
  - Distinct price points per 365 nights: mean 16; median 4
  - Last-month discount: mean 5%; median 2%
  - Summer price premium: mean 2.4%; median 0.4%

### Specific quotes to cite

**Technology-skill complementarity framing:**

1. "Pricing frictions might be particularly pronounced for amateur sellers, who lack the managerial capabilities compared to professionals (Goldfarb and Xiao, 2011; Li et al., 2016). Further, whereas the platform has an incentive to assist seller-pricing, its objective does not necessarily align with sellers'. As a result of the misaligned incentives, platform-provided pricing technologies (pricing interfaces and algorithms) might distort prices away from sellers' (or consumers') desired outcomes and towards that of the platform." (p. 2)

2. "My main explanation of the persistent heterogeneity between sellers in their pricing strategies, which is correlated with (but not driven by) the number of listings. In particular, single-listing sellers face a greater extent of pricing frictions, and thus, tend to set fixed prices across nights and/or over time." (p. 21) -- This directly supports our "technology-skill complementarity" framing: pricing sophistication is a persistent seller type correlated with but not caused by scale, and technology (the algorithm) complements this pre-existing skill.

3. "However, a simple platform design, where the platform sets price variation but gives sellers the final decision right to determine the price levels, will eliminate almost all frictions." (Abstract, p. 1) -- This is the core quote linking Huang's structural findings to our empirical result that Smart Pricing affects variance but not levels.

**Price levels vs. price variance:**

4. "One standard deviation of the price (within listing, across nights) increases from 4% in the baseline to 6% in the first-best for the median listing. Also, first-best prices generally decrease over time as the option value for waiting for additional customers dwindles. I show that the percent last-month discount increases to 30% from 2% (i.e., almost completely sticky prices) for the median listing." (p. 43)

5. "I find that the median price level is close to (but a bit lower than) the first-best, and that the degree of price adjustments over time, price dispersion, and occupancy rate are almost identical to the first-best." (p. 47, on Counterfactual 3)

**Platform's incentive (commission maximization vs. host profit):**

6. "Because the platform's payoff depends on a fixed share of sellers' total booking revenue, it likely wants seller-*revenue*-maximizing prices (throughout the paper, I will assume that the platform will not help sellers collude). In contrast, sellers' *profit*-maximizing prices are higher, so as to internalize their opportunity costs of time. The incentive incompatibility implies that platform-controlled prices might not be at the seller-optimal level." (p. 5)

7. "The platform gains little -- its profit increases by 2.5%. Almost all market participants gain from eliminating all frictions. The frictions significantly impact consumers and some sellers. Yet, around half the sellers and the platform are not affected much by the frictions (below 3% loss in surplus). The platform might have limited incentives to spend significant efforts to eliminate the frictions." (p. 43)

### Limitations and gaps our paper fills

**What Huang does NOT do that we do:**

1. **Single city vs. multi-city.** Huang studies San Francisco only. We study multiple cities, enabling us to examine cross-market heterogeneity in algorithm effects and to test whether results generalize beyond a single high-demand urban market.

2. **No quasi-experimental identification of algorithm effects.** Huang observes the status quo and runs structural counterfactuals. He does not have an exogenous shock to algorithm availability. We exploit the Smart Pricing rollout/availability change as a quasi-experiment, providing reduced-form causal evidence that complements his structural approach.

3. **No market-level equilibrium effects.** Huang's counterfactuals simulate individual-listing-level outcomes taking the competitive environment as given (he resolves equilibrium via forward simulation, but within a single market). We can examine whether algorithm adoption by some hosts affects neighboring hosts' outcomes (spillovers/market-level effects).

4. **Does not model the algorithm adoption decision.** Huang takes pricing behavior as given. We observe which hosts have access to Smart Pricing and can study adoption determinants and selection.

5. **No direct evidence on third-party pricing tools.** Huang notes these exist (footnote 12: "sellers can use paid third-party pricing software. Typically, using third-party interfaces incurs a fee (usually 1% of total revenue)") but cannot identify users. He acknowledges: "While I do not have direct measures of who uses a pricing software, I later demonstrate that price variations are low and display clear patterns consistent with the standard price-setting interface, suggesting that the majority of sellers still use the standard interface to set prices."

6. **No heterogeneous treatment effects of algorithm access.** Huang documents heterogeneity in pricing *types* but does not study how different types differentially *benefit* from algorithm availability. Our paper directly estimates heterogeneous effects by host sophistication.

7. **Counterfactual 3 uses crude adjustment functions.** Footnote 26: "One might imagine that a_{m,l,tau,t}'s can be crude... One might also imagine that a_{m,l,tau,t}'s can be further optimized by the platform. For this counterfactual exercise, I use the crude (and potentially suboptimal) a_{m,l,tau,t}'s to illustrate that improvements can still be gained." Our quasi-experimental evidence can quantify the *actual* gains from the platform's real pricing tool, rather than a stylized counterfactual.

**Assumptions Huang makes that we can test or relax:**

1. **Pricing sophistication is a persistent type.** Huang finds this in Table 2B (no within-seller learning). We can test this with our panel data: does algorithm adoption change hosts' *own* pricing behavior after they stop using the algorithm? If so, there is learning; if not, sophistication is indeed a fixed type.

2. **Revenue-maximizing algorithm sets prices 26% below baseline.** We can test whether Smart Pricing adoption is associated with lower price levels in our data. Our null effect on levels could be because hosts use Smart Pricing's suggestions selectively (accepting variance-increasing adjustments but overriding level-decreasing ones).

3. **The dominant friction is cognitive constraints, not menu costs.** Huang estimates ~52% cognitively constrained. Our heterogeneous treatment effects can provide complementary evidence: if the algorithm helps even hosts with low adjustment costs (i.e., those who already adjust prices frequently), this suggests the algorithm provides more than just a better interface.

4. **Multi-product pricing is simplified away.** Huang assumes sellers price each listing independently, ignoring cannibalization across a multi-listing portfolio. We can examine whether algorithm effects differ for multi-listing hosts in ways that suggest portfolio considerations matter.

5. **Static entry/exit.** Huang's participation model is static (each quarter, listing stays if Pi > F). We can examine dynamic extensive-margin responses to algorithm availability over longer horizons.
