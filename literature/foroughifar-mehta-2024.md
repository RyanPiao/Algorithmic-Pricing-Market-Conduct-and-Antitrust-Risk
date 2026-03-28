# Foroughifar & Mehta (2024) -- Paper Snapshot

## Citation

Foroughifar, Mohsen and Nitin Mehta (2024). "The Challenges of Deploying an Algorithmic Pricing Tool: Evidence from Airbnb." SSRN Working Paper No. 4891482, May 20, 2024. Authors affiliated with Tepper School of Business (Carnegie Mellon) and Rotman School of Management (University of Toronto).

---

## Research question

Why is the adoption rate of Airbnb's Smart Pricing (SP) algorithm surprisingly low (only 22% of hosts over 20 months), and what are the relative roles of adoption costs, pessimistic prior beliefs about the algorithm, and the algorithm's own sub-optimality in explaining this low uptake? What steps can Airbnb take to improve adoption and profitability for hosts and the platform?

---

## Identification strategy

**Not a reduced-form causal design.** The paper combines descriptive reduced-form regressions with a dynamic structural model. There is no quasi-experiment or sharp identification strategy.

- **Reduced-form stage**: OLS/IPTW-weighted regressions comparing revenues across Base, Custom, and Smart price types, with listing FE, month/year/weekend FE. Selection into Custom vs. Base (and Smart vs. others) is addressed via inverse probability of treatment weighting (IPTW) on observables plus sensitivity analysis (Masten & Poirier 2018). They also run Borusyak et al. (2021) imputation estimators as robustness for staggered adoption.
- **Structural model (core contribution)**: A dynamic structural model with two sides:
  - **Demand**: Random-coefficient aggregate logit model (BLP-style) estimated on Austin market-share data. Price and review endogeneity handled via control-function approach with BLP-type instruments (sum of competitor characteristics in same zip code). Estimated via Bayesian MCMC.
  - **Supply**: Hosts make daily nested decisions -- (1) block vs. operate listing, (2) choose pricing method (Base/Custom/Smart), (3) set Custom price level. The pricing-method choice is a forward-looking dynamic discrete choice problem. Hosts have heterogeneous adjustment costs (switching to Custom), adoption costs (activating SP), marginal costs, and prior beliefs about SP's price-setting behavior. Hosts learn about SP via Bayesian updating from observed Smart price realizations.
  - **Equilibrium concept**: Moment-based Markov Equilibrium (Ifrach & Weintraub 2017) to handle large state space with many hosts.
  - **Estimation**: IJC algorithm (Imai et al. 2009) with Bayesian estimation; hierarchical Bayesian model recovers host-level parameter distributions.
- **Identification of prior beliefs vs. adoption costs**: Separated by exploiting (a) the propensity to adopt SP (depends on both beliefs and adoption cost) vs. (b) the rate of switching away from SP after adoption (depends on posterior beliefs, not adoption cost). Observed Smart price realizations provide signals that update beliefs, generating variation that identifies the prior.

---

## Data

- **Source**: AirDNA (third-party commercial data provider) matched with scraped Airbnb calendar pages. **Not proprietary Airbnb data; not Inside Airbnb either.** AirDNA provides property characteristics, booking/availability status, host characteristics. Scraped calendars provide price levels AND price type labels (Base, Custom, or Smart) -- a unique feature from calendar metadata.
- **Geography**: 5 US cities -- Austin, Los Angeles, New York City, San Francisco, Seattle.
- **Time period**: October 2014 to August 2017 (35 months; 14 months pre-SP, 20 months post-SP deployment in Dec 2015).
- **Sample size**: 13,941 listings; 12+ million listing-night observations for descriptive/reduced-form analyses. Structural model estimated on Austin subsample only (for computational tractability).
- **Key data feature**: For each listing-night, they observe the price level AND whether it is Base, Custom, or Smart type. This lets them track when hosts adopt/abandon SP at the daily level.
- **Summary statistics**: Average price $187, average revenue $39/night; 27% of listing-nights booked, 34% available, 39% blocked. Smart price used on only 4% of listing-nights; Custom on 41%; Base on 55%.

---

## Key findings

1. **Smart Pricing yields lower revenue than Custom prices but higher revenue than Base prices.** SP does not outperform manual Custom pricing in any month. Custom prices earn consistently higher revenue because they incorporate local demand shocks (e.g., SXSW in March, ACL in October) better than SP does. SP is designed to minimize bad price suggestions rather than maximize host profit, since it lacks marginal cost information.

2. **SP benefits hosts with high adjustment costs most, but precisely those hosts are least likely to adopt.** Hosts who rarely switch from Base to Custom (high adjustment cost proxy, pre-SP Base usage rate) would gain most from SP, yet they adopt at significantly lower rates (coefficient on pre-SP Base usage: -0.133***). The irony: the hosts who need the tool most avoid it.

3. **Pessimistic prior beliefs are the dominant barrier to adoption, far more important than adoption costs.** At deployment, hosts on average believe SP sets prices 38% lower than actual Smart prices, translating into a 56.6% gap between actual SP profit and believed SP profit. Eliminating pessimistic beliefs alone would raise adoption from 22% to 81.5% and increase average host profit by 26.5% ($4,957/year); eliminating adoption costs alone raises adoption only to 33.9% with a 3.2% ($277) profit gain. Beliefs matter ~8x more than adoption costs.

4. **Re-training SP with structural marginal cost estimates would substantially improve performance.** When the algorithm is modified to maximize host profit (using recovered marginal costs) instead of minimizing bad price suggestions, host annual profit rises 27.4% ($4,442) even without changing adoption rates. Combining re-training with corrected beliefs yields +98.8% ($18,481) in host profit and +31% ($0.5M) in platform revenue.

5. **Hosts learn about SP through Bayesian updating but learning is slow.** The noise-to-information ratio is very low (0.0065), meaning hosts need many Smart price realizations before beliefs converge. About 40% of adopters permanently abandon SP, with average usage of only 56 days before switching off. Conditional on adoption, high-adjustment-cost hosts are more likely to keep using SP, consistent with them having more to gain and thus updating beliefs faster upon seeing actual performance.

---

## Relevance to our paper

This is our closest competitor studying Airbnb Smart Pricing. Key points of differentiation and engagement:

**How we differentiate:**
- **Research design**: FM use a structural model to study host-level adoption decisions and the platform's optimization problem. We use a sharp reduced-form ITT design exploiting the SP rollout across 8 US cities, which provides cleaner causal identification of market-level equilibrium effects without structural assumptions.
- **Research question**: FM ask "why don't hosts adopt SP?" (a supply-side/adoption question). We ask "what are the equilibrium effects of SP availability on market prices and price dispersion?" -- a fundamentally different market-level question.
- **Data**: FM use AirDNA + scraped calendars for 5 cities. We use [our data source] for 8 cities with a different identification strategy.
- **Findings are complementary, not contradictory**: FM find SP generates lower revenues than Custom prices at the individual host level. Our null effect on price levels is consistent with this -- if SP lowers prices for adopters but adoption is low (22%), the market-level effect would indeed be small/null. Our positive variance finding is novel and not addressed by FM.

**What we should engage with:**
- FM's reduced-form finding that SP does not outperform Custom pricing is important context for our null levels result. We should cite this.
- FM's finding on low adoption (22%) helps explain our null ITT -- intent-to-treat effects would be attenuated by low take-up.
- FM explicitly note they do NOT study competitive/collusive effects of SP adoption (p.7: "the competitive effects of SP adoption are not strong in our data due to its low adoption rate"). This is a gap we can claim to speak to with our market-level equilibrium approach.
- FM's focus is entirely on the host/platform perspective. Our consumer welfare / market equilibrium perspective is distinct.

---

## Methodological lessons

- **Random-coefficient logit demand + dynamic supply with Bayesian learning**: A technically sophisticated structural IO approach. We should cite as a contrasting methodology -- they need strong functional-form assumptions where our reduced-form design does not.
- **IPTW for selection into price types**: They use inverse probability of treatment weighting to address selection into Custom/Smart pricing. Their sensitivity analysis (Masten & Poirier 2018) suggests unobservables would need to cause a 30-40% deviation in treatment probability to nullify effects -- a useful benchmark.
- **Borusyak et al. (2021) imputation estimator**: They use this for robustness with staggered treatment timing. We should consider citing/using the same if relevant to our rollout design.
- **Replication of SP algorithm**: They replicate Airbnb's SP algorithm following Ye et al. (2018) technical note, with MAPE of 9.46%. This is useful methodological detail about how SP works (3-component system: GBM for demand curve, SVR-inspired loss function for pricing, personalization layer for host min/max bounds).
- **Moment-based Markov Equilibrium (Ifrach & Weintraub 2017)**: Interesting solution to the curse of dimensionality in dynamic games with many players. Not directly relevant to our approach but worth citing if we discuss why structural approaches face computational challenges.

---

## Limitations acknowledged (gaps our paper fills)

1. **No market-level equilibrium analysis**: FM explicitly state they do not study competitive effects of SP. They focus entirely on individual host adoption decisions and platform optimization. Our paper fills this gap by estimating market-level equilibrium effects on prices and dispersion.

2. **Structural model estimated on Austin only**: Due to computational constraints, the structural model uses only one city. Reduced-form results cover 5 cities but are descriptive comparisons, not causal. Our design covers 8 cities with a unified causal framework.

3. **No consumer welfare analysis**: FM's welfare analysis is entirely from the host/platform revenue perspective. They do not study guest-side outcomes (booking rates, prices paid, consumer surplus). Our paper can speak to market-level price effects relevant to consumers.

4. **No analysis of price dispersion/variance**: FM compare mean price levels and revenues across pricing types. They do not examine whether SP affects the cross-sectional distribution of prices or within-listing price variance. Our positive variance finding is entirely novel relative to their work.

5. **Cannot study dynamic pricing in the booking-lead-time sense**: They acknowledge they cannot study how prices change as a function of time-to-check-in (they observe only "final" prices). This is a limitation we may share but worth noting.

6. **Single-listing host assumption**: They assume each host operates one listing (only 8% have multiple). In markets with more professional hosts, this assumption may not hold. Depending on our city mix, we may capture more professional-host-heavy markets.

7. **Selection concerns in reduced-form**: Their comparisons of Base vs. Custom vs. Smart prices, even with IPTW, rely on selection-on-observables. Our ITT design sidesteps this by exploiting the rollout itself rather than within-host adoption choices.
