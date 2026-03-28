# Assad, Clark, Ershov & Xu (2024) — Paper Snapshot

## Citation

Assad, Stephanie, Robert Clark, Daniel Ershov, and Lei Xu. 2024. "Algorithmic Pricing and Competition: Empirical Evidence from the German Retail Gasoline Market." *Journal of Political Economy* 132 (3): 723--771. DOI: [10.1086/726906](https://doi.org/10.1086/726906).

---

## Research Question

Does the adoption of algorithmic pricing (AP) software affect competition in retail markets? Specifically, the paper asks whether the widespread introduction of AI-based pricing software in Germany's retail gasoline market beginning in 2017 led to higher margins and prices, and whether these effects operate through changes in competitive interaction rather than through improved demand forecasting or cost tracking.

---

## Identification Strategy

The paper faces three identification challenges: (1) adoption is not directly observed, (2) adoption is endogenous, and (3) higher margins could reflect efficiency gains rather than softened competition.

**Identifying adopters.** Because no data on actual adoption decisions exist, the authors detect adoption through structural breaks in three pricing-behavior markers -- (i) number of daily price changes, (ii) average size of price changes, and (iii) rival response time -- using Quandt-Likelihood Ratio (QLR) tests station-by-station. A station is classified as an adopter if it experiences structural breaks in at least two of three measures within a four-week window. Approximately 3,323 of 16,027 stations are classified as adopters; over 50% of average break dates cluster in the spring/summer of 2017, consistent with known AP software rollout timing.

**Instrumental variable.** Station-level adoption is endogenous (adopters differ systematically on observables and likely on unobservables). The main IV is *brand-HQ-level adoption*: for station *i* at time *t*, the instrument is the share of other stations belonging to *i*'s brand that have been classified as adopters by month *t* (excluding station *i* itself). The identifying assumption is that brand-level strategic decisions to partner with AP software providers are driven by national/brand-wide considerations and should not be correlated with individual station-specific unobservable shocks, conditional on controls. The first stage F-statistic is 35.

**Robustness IV.** As an alternative, broadband internet availability and quality in the station's local area is used (AP software is cloud-based and requires reliable high-speed internet). A "placebo IV" using adoption shares of a *random other brand* yields null effects, as expected.

**Competition test.** To separate competition effects from efficiency gains, the authors split the sample by market structure: monopoly stations (sole station in a ZIP code) vs. non-monopoly stations. If AP only improves operational efficiency, both groups should benefit equally. If AP changes competitive interaction, only non-monopolists should see margin increases. They further examine duopoly markets (two-station ZIP codes), comparing outcomes when zero, one, or both stations adopt.

**Key assumptions required:**
- Brand-HQ adoption decisions are exogenous to individual station-level unobservable shocks (exclusion restriction)
- Structural breaks in pricing behavior reliably indicate AP adoption (measurement validity)
- ZIP-code-level market definition captures relevant competitive interactions

---

## Data

- **Source:** German Market Transparency Unit for Fuels (Markttransparenzstelle fur Kraftstoffe), mandating real-time price reporting by all gas stations since August 2013
- **Fuel type:** Super E5 gasoline (~80% market share in Germany)
- **Frequency:** Minute-level price data, aggregated to daily station-level averages (weekdays 7am--9pm) and monthly station-level summaries
- **Time period:** January 2016 -- December 2018 (36 months)
- **Unit of observation:** Station-month (for main regressions); market-month for duopoly analysis
- **Sample size:** 16,027 stations; 448,221 station-month observations; ~39,148 market-month observations for duopoly analysis
- **Market definition:** 5-digit ZIP codes; 5,781 ZIP codes total, of which 2,094 are monopoly (single station) and 1,307 are duopoly
- **Additional data:** Regional wholesale gasoline prices (Oil Market Report), Eurostat NUTS3-level demographics, German Meteorological Service weather data, EU Commission broadband internet availability (netBravo)
- **Margins:** Retail price minus regional wholesale price minus 19% VAT

---

## Key Findings

- **Station-level margin increase:** AP adoption increases mean station-level margins by 0.8 cents/liter (roughly 9% above the non-adopter mean margin of 8.3 cents), with mean prices rising 0.6 cents/liter. The entire margin and price distribution shifts right (2SLS, Table 3).

- **Monopolists vs. non-monopolists:** Margin increases are driven entirely by non-monopolist stations (0.9 cents/liter, ~11% increase). Monopolist adopters show no statistically significant change in mean margins or prices, except that the 95th percentile of prices *falls* by 1.2 cents (potentially reflecting better demand tracking or avoidance of "too high" prices). This pattern supports the competition channel rather than pure efficiency gains (Table 4).

- **Duopoly market-level results:** In duopoly markets, adoption by only one of two stations produces *no* significant change in market-level margins or prices. When *both* stations adopt, mean market margins increase by 3.2 cents/liter (~38% above zero-adopter baseline) and mean prices increase by 4 cents/liter. The entire margin distribution shifts up. These are lower-bound estimates due to likely measurement error in adoption classification (Table 5).

- **Timing consistent with algorithmic learning:** Margin and price increases in duopoly markets do not appear until roughly one year after both stations adopt, consistent with simulation evidence (Calvano et al. 2020) that algorithms require extended training to converge to tacitly-collusive strategies (Table 6).

- **Mechanism -- undercutting disappears:** In duopoly markets where both stations adopt AP, the probability that the high-price station undercuts the low-price station falls by 13 percentage points (from a 10% baseline to approximately zero). Stations become 18% more likely to match a rival's price *decrease* within 5 minutes, but show no increased propensity to match price *increases*. This asymmetric response effectively teaches algorithms that undercutting is unprofitable (Table 7).

---

## Relevance to Our Paper

This paper is the most important comparator for our Airbnb Smart Pricing study. Key points of connection and contrast:

1. **Same broad question, different market.** Both papers study algorithmic pricing adoption and its effects on market outcomes. Assad et al. find a strong *positive* effect on prices/margins in a homogeneous-good oligopoly; our null finding on price levels in a differentiated-product platform market with many sellers is a meaningful contrast. The difference likely reflects market structure: tacit collusion is feasible among 2-3 gasoline stations in a ZIP code but implausible among dozens of Airbnb hosts.

2. **Adoption identification parallels.** Assad et al. face the same challenge we do -- AP adoption is not directly observed. They use structural breaks in pricing behavior; we use platform-level rollout timing in a sharp ITT design. Their approach is more granular but requires stronger measurement assumptions. Our ITT avoids the need to identify individual adopters but estimates a diluted (intent-to-treat) effect.

3. **Monopoly vs. competition test is directly transferable.** Their clean comparison of monopolists (no competitive interaction) vs. non-monopolists is a design we should cite when motivating our own heterogeneity analyses by market density/competition. If we find that Smart Pricing effects on variance or discrimination differ by the number of nearby listings, this mirrors their logic.

4. **Variance/distribution results.** Assad et al. examine the full distribution of margins (5th, 25th, 50th, 75th, 95th percentiles), finding that the entire distribution shifts. We should similarly present distributional effects, especially since our primary finding is about *variance* and price discrimination rather than levels.

5. **Their finding strengthens our null.** The fact that a top-5 journal publishes a clear positive effect of AP on prices in gasoline makes our Airbnb null more interesting and publishable as a contrast case -- algorithmic pricing does not universally raise prices; market structure mediates the effect.

6. **Hub-and-spoke concern.** Assad et al. note that when multiple competitors use the *same* AP software provider, the algorithm acts as a "hub" in a hub-and-spoke arrangement (Harrington 2018b). This is directly relevant to Airbnb Smart Pricing, where the *platform itself* provides the algorithm -- all adopters use the same tool by construction. Yet we find no price increase, suggesting the hub-and-spoke mechanism requires oligopolistic structure to bite.

---

## Methodological Lessons

1. **Structural-break approach to identifying AP adoption.** The QLR-test method for detecting adoption when adoption dates are unobserved is clever and citable, even though we use a different design. We should reference it when discussing alternative approaches.

2. **Brand-HQ-level IV strategy.** Instrumenting individual adoption with aggregate (brand/platform) adoption decisions is a useful template. In our context, the platform-level rollout of Smart Pricing is analogous to the brand-HQ decision, but because Airbnb rolled out to all hosts simultaneously, we exploit this as a sharp treatment date rather than as a cross-sectional instrument.

3. **Monopoly/non-monopoly split as a falsification test.** Splitting by market structure to distinguish competition effects from efficiency effects is a clean and compelling identification strategy we should adopt in our heterogeneity analysis.

4. **Distributional analysis.** Examining effects at multiple quantiles of the outcome distribution (5th, 25th, 50th, 75th, 95th percentiles) rather than only the mean is a practice we should follow, especially given our variance/discrimination findings.

5. **Timing/event-study for mechanism.** The dynamic analysis showing that effects emerge only after ~12 months (consistent with algorithmic learning) is a useful model for how to present timing evidence in reduced-form work.

6. **Placebo IV test.** Using adoption shares of a *different* brand as a placebo instrument is a clever falsification. We might construct analogous placebo tests.

---

## Limitations Acknowledged

- **Adoption is inferred, not observed.** The structural-break classification may mislabel some adopters as non-adopters (and vice versa), biasing estimates toward zero. The authors acknowledge this produces lower-bound estimates.

- **Cannot distinguish algorithm types.** The authors do not know which specific algorithm each station uses, whether stations fully delegate pricing decisions to the algorithm, or whether multiple stations in a market use the *same* software provider. The hub-and-spoke vs. independent-algorithm distinction has different policy implications.

- **Short sample period.** The 36-month window (Jan 2016 -- Dec 2018) limits the ability to study long-run effects and means many duopoly markets with both adopters are observed for less than a year post-adoption.

- **Market definition sensitivity.** ZIP-code-level market definition is an approximation; robustness checks with 1km-radius circles yield similar but not identical results.

- **External validity.** The authors explicitly note that results are specific to retail gasoline markets in Germany, a homogeneous-good oligopoly with mandated price transparency. They caution against direct extrapolation to other settings (though they note AP software is used across industries).

- **Cannot fully rule out efficiency channel.** While the monopolist/non-monopolist comparison strongly suggests a competition effect, the authors cannot completely exclude the possibility that AP helps non-monopolists track costs *and* softens competition simultaneously.

- **Exclusion restriction not directly testable.** The assumption that brand-HQ adoption is uncorrelated with station-level unobservables (conditional on controls) cannot be formally verified, though the placebo IV and the insensitivity of brand adoption shares to local demographics provide supporting evidence.

---

## DEEP READ (added 2026-03-22)

### Identification details

**AP marker detection (structural breaks).** The three markers used to detect algorithmic pricing adoption are:

1. **Number of daily price changes** -- expected to increase because AP software promises to "rapidly, continuously, and intelligently react to market conditions." Pre-break average: 6 changes/day; post-break average: 9 changes/day.
2. **Average size of price changes** -- direction ambiguous ex ante (algorithm could make smaller, more frequent adjustments, or larger ones if consumers are found to be unresponsive). Pre-break: 2.7 cents; post-break: 2.9 cents.
3. **Rival response time** -- time (in minutes) for a station to respond to a rival's price change. Expected to decrease. Pre-break: 64 minutes; post-break: 54 minutes (~10% drop).

All three measures are aggregated to the **weekly** level for each station. The authors run a **Quandt-Likelihood Ratio (QLR) test** (Quandt 1960, Andrews 1993) on each measure for each station independently. The QLR test searches for the single break date that maximizes the F-statistic for a structural break in a time-series regression. This is well-suited to their problem because the exact adoption date is unknown. The test evaluates every week in a "large window around the time of supposed adoption" and selects the week with the highest F-statistic as the best-candidate break date.

**Classification rule:** A station is classified as an adopter if it experiences best-candidate structural breaks in **at least 2 of 3 measures within a 4-week window.** The logic: a single break in one measure could occur for many idiosyncratic reasons, but concurrent breaks in multiple measures within a short window strongly indicate a systematic change in pricing technology. About **3,323 of 16,027 stations** (~21%) are classified as adopters. Robustness checks: (a) 2-week window instead of 4 weeks, (b) using only the two measures that do not depend on rival presence (number of price changes, average size), (c) requiring breaks in both E5 and Diesel fuel. All yield qualitatively similar results (Appendix E.3).

**Timing validation:** Over 50% of average break dates cluster in spring/summer 2017, consistent with trade press reports (Tankstop, Dec 2017) that a2i's software became available to German stations that summer.

**Instrument construction.** The IV is **brand-HQ-level adoption share**: for station *i* at time *t*, the instrument is the fraction of *other* stations belonging to *i*'s brand that have been classified as adopters by month *t*. Formally:

> IV_it = (number of other stations of i's brand classified as adopters by t) / (total number of other stations of i's brand)

Station *i* is excluded from its own brand's share (leave-one-out). The logic: brand-HQ decisions to partner with AP providers are national/strategic and should not respond to individual station-level shocks.

**First-stage F-statistic: 35.** A 10% increase in brand adoption share increases the probability that station *i* adopts by 65%. This is a strong first stage -- well above the Stock-Yogo critical values. For comparison, our Airbnb paper's first-stage F-stats range from 4,158 to 13,906 for the ITT, but our concern was never instrument weakness; theirs was more legitimate given the constructed nature of the IV.

**Exclusion restriction defense.** They argue that brand-HQ decisions are driven by national/brand-wide strategic considerations and should be uncorrelated with local station-level unobservables, conditional on controls. Supporting evidence:
- **Table B6 (Appendix):** Conditional on brand size (number of stations), brand adoption share is uncorrelated with average local demographics, competition intensity, or other observable characteristics of a brand's stations. The *only* significant correlate of brand adoption probability is brand size.
- **Placebo IV:** They use the adoption share of a **random other brand** (not the station's own brand) as a placebo instrument. This yields null effects on margins/prices, as expected -- confirming that the main IV is not picking up some general time trend in adoption.
- **Broadband IV (robustness):** Local broadband internet availability/quality yields qualitatively similar results, providing a completely different source of identifying variation.

**Placebo / falsification tests:**
1. **Placebo IV** (random brand adoption share) -- null effects.
2. **Monopolist vs. non-monopolist split** -- this is effectively a falsification. If AP only improved operational efficiency, monopolists should see the same margin increase as non-monopolists. They don't -- monopolists show no significant mean margin change.
3. **Non-adopter margins in duopoly markets** -- when a rival adopts but the focal station doesn't, the non-adopter's margins do *not* change (Table C3), ruling out the hypothesis that partial adoption already shifts the competitive equilibrium.
4. **Shell exclusion** -- dropping Shell stations (which had a price-matching guarantee from 2015) does not change results.
5. **Aral exclusion** -- dropping Aral stations (early adopter, potential measurement error concern) does not change results.
6. **Balanced panel** -- results hold when restricting to stations/markets present for the full sample period.

### Results in detail

**Station-level margin increase (Table 3, 2SLS):**
- Mean margin: +0.8 cents/liter (SE 0.002), ~9% above non-adopter mean margin of 8.3 cents
- 5th percentile margin: +1.5 cents (SE 0.002)
- 25th percentile margin: +0.9 cents (SE 0.002)
- 50th (median) margin: +0.6 cents (SE 0.002)
- 75th percentile margin: +0.5 cents (SE 0.002)
- 95th percentile margin: +1.9 cents (SE 0.008)
- Mean price: +0.6 cents/liter (SE 0.002)
- All margin and price percentiles (5th through 75th) increase; 95th percentile price shows no significant change

**Monopoly vs. non-monopoly split (Table 4, 2SLS):**
- **Monopolist adopters (67,300 obs):** Mean margin +0.3 cents (SE 0.005, *not significant*). 5th pctile margin +1.3 cents (p<0.01). Median margin -0.1 cents (ns). 95th pctile margin +5.2 cents (p<0.05). 95th pctile *price* **decreases** by 1.2 cents (p<0.05). Other price percentiles: all null.
- **Non-monopolist adopters (380,826 obs):** Mean margin +0.9 cents (SE 0.002, p<0.01), ~11% increase. All margin percentiles shift right significantly. Mean price +0.7 cents (p<0.01). Entire price distribution shifts right except 95th percentile.

**Duopoly market-level results (Table 5, 2SLS, 39,148 obs):**
- One station adopted: Mean market margin -0.8 cents (SE 0.008, *not significant*). All percentiles: null.
- **Both stations adopted: Mean market margin +3.2 cents (SE 0.012, p<0.01), ~38% increase.** 5th pctile +3.6 cents, 25th pctile +3.2 cents, median +2.8 cents, 75th +3.0 cents, 95th +9.9 cents (p<0.1).
- Market prices: one adopted -- null across the board. Both adopted -- mean +4.0 cents (SE 0.016, p<0.05). All price percentiles shift up significantly.

**"All adopt" vs. "partial adopt" distinction:** This is the core result. The market-level duopoly specification (Equation 2) includes separate indicators for T^1 (one station adopted) and T^2 (both stations adopted). The fact that beta_1 is null and beta_2 is large and significant is the cleanest evidence that AP works through changing *competitive interaction*, not through operational efficiency. If it were efficiency, partial adoption should also raise margins. The pattern is consistent with tacit collusion requiring mutual adoption.

**Price VARIANCE / DISPERSION effects (Table 7, columns 5-6):**
- **Mean within-market within-day absolute price dispersion** (difference between the two duopolists' average daily prices): Both stations adopted yields coefficient of **-0.004 (SE 0.006, not significant)**. One station adopted: +0.008 (SE 0.005, not significant). The time-specific analysis (column 6) also shows null effects across all time bins.
- **CRITICAL FOR OUR PAPER:** Assad et al. find **no significant effect of AP on price dispersion** between duopolists. This means AP raises *both* stations' prices in tandem, maintaining the spread. They do not examine within-station price variance over time (variance of a station's own prices across days).

**Dynamic effects (Table 6):**
- 0-6 months after both adopt: margin effect = +0.6 cents (SE 0.004, not significant)
- 7-12 months after both adopt: margin effect = +1.2 cents (SE 0.006, p<0.1)
- **12+ months after both adopt: margin effect = +3.9 cents (SE 0.018, p<0.05)**
- Pattern: effects grow monotonically over time. No significant effects in the first year.
- One station adopted: null at all time horizons (0-6, 7-12, 12+ months all zero).
- Consistent with Calvano et al. (2020) simulations showing algorithms need ~500,000 periods to converge, corresponding to at least one year.

**Undercutting analysis (Table 7, columns 7-8):**
- Undercutting probability (baseline ~10%, i.e., the high-price station undercuts the low-price station ~3 days/month): falls by **13.4 pp** (SE 0.071, p<0.1) when both adopt, becoming effectively zero. Null when only one adopts.
- Timing: effect grows over time -- not significant at 0-6 months, -6.3 pp at 7-12 months (p<0.05), **-21.3 pp** at 12+ months (p<0.05).

**Response to rival price changes (Table 7, columns 1-4):**
- Probability of matching a rival's price *decrease* within 5 minutes: +18.3 pp (SE 0.073, p<0.05) when both adopt.
- Probability of matching a rival's price *increase* within 5 minutes: -10.8 pp (SE 0.076, not significant) when both adopt. Asymmetric: algorithms quickly match decreases but do not reliably match increases.

### Structural break methodology (potential borrowing for our paper)

**Observable features that distinguish algorithmic from manual pricing:**
1. **Frequency of price changes:** Jumps from ~6/day to ~9/day. This is the most visible marker.
2. **Size of price changes:** Smaller increase (2.7 to 2.9 cents), less distinctive.
3. **Rival response time:** Drops from 64 to 54 minutes. Requires identifying a "rival" and having minute-level data.

**QLR implementation:** The QLR test is applied separately for each station and each measure. For each week in the sample, they estimate a regression with a break at that week and compute the F-statistic. The week with the maximum F is the "best-candidate break date." They check at 5% significance level (13,133 stations have at least one significant break). The approach references Harrington (2008), Clark and Houde (2014), Boswijk et al (2018), and Crede (2019) for prior use of QLR tests in collusion detection. Standard references: Quandt (1960), Andrews (1993).

**Adaptation to Inside Airbnb data:** Challenging but not impossible. We would need:
- Observable pricing behavior markers for Smart Pricing: frequency of price changes (daily scrape data may not have enough resolution), whether prices vary mechanically with demand proxies (weekday/weekend, seasonal), price change *patterns* (e.g., algorithmic prices may update more systematically).
- However, our ITT design largely circumvents this need. The structural break approach is most useful when adoption timing is staggered and individual-level adoption is unknown. Since Airbnb's Smart Pricing was rolled out to all hosts simultaneously (platform-wide feature), we exploit this as a sharp treatment date.
- **Potential use:** We could use structural breaks in listing-level pricing behavior as a *secondary* measure of actual adoption (intensive margin) to complement the ITT. E.g., detect which listings started showing more frequent/algorithmic-looking price changes after the rollout.

### Market structure comparison with Airbnb

**Firms per market in their setting:**
- Market definition: 5-digit ZIP code.
- 5,781 ZIP codes; mean 2.77 stations/ZIP; **median 2**. Of these: 2,094 are monopoly (1 station), 1,307 are duopoly (2 stations). Only 81 ZIPs have >10 stations.
- The key results are from **duopoly markets** (2 stations). This is fundamentally an oligopoly/duopoly setting.

**Product homogeneity:**
- Gasoline (Super E5) is **nearly perfectly homogeneous** -- essentially identical across stations. Competition is on price and location/convenience only.
- Airbnb listings are **highly differentiated** -- unique locations, amenities, sizes, reviews, host characteristics. Even "comparable" listings differ substantially.

**Price transparency:**
- German gasoline: **perfect and mandated transparency.** Since 2013, all stations must report price changes in real time to the Markttransparenzstelle. Prices are publicly available via apps/websites. Algorithms can observe all rivals' prices continuously.
- Airbnb: **moderate transparency.** Listing prices are publicly visible on the platform, but (a) there are far more rivals to track, (b) listing differentiation makes price comparisons less informative, (c) actual *transaction* prices (after cleaning fees, discounts, etc.) are less transparent, (d) occupancy rates are unobserved.

**What THEY say about when AP should NOT raise prices:**
- The paper explicitly notes that their evidence is "particular to retail gasoline markets in Germany (where high frequency pricing data are available)" (p.39).
- They cite Miklos-Thal and Tucker (2019) who argue that "improved demand prediction may lead to the possibility of collusion in markets where it is previously unsustainable, in other markets it may create incentives for deviation that were absent with less prediction capabilities" (p.6). In other words, better demand prediction can cut *either way* on collusion.
- They note that the key mechanism is **speed of detection and punishment of deviations** (p.12): "In a setting with perfect monitoring, increases in the speed of interaction facilitate cooperation, since it is easier to detect and punish deviations from tacitly-collusive equilibria (Abreu et al 1991)."
- Implication: AP should be *less* likely to raise prices in markets where (a) monitoring is imperfect, (b) products are differentiated (making "deviations" hard to detect), (c) there are many firms (making coordination harder).

### Specific quotes to cite

**On mutual adoption as the condition for margin effects:**
> "Markets where only one of the two stations adopts see no change in mean market-level margins or prices. Markets where both stations adopted show a mean margin increase of nearly 38% and the entire distribution of margins shifts to the right." (p.5)

> "Lack of margin changes from partial/asymmetric adoption and substantial increases in margins and prices after complete adoption is suggestive of algorithms facilitating tacit-collusion." (p.31)

**On market structure conditions / when AP may be benign:**
> "While our evidence is particular to retail gasoline markets in Germany (where high frequency pricing data are available), the same algorithmic pricing software is adopted in gasoline retail markets around the world." (p.39)

> "Adopting stations *with no competitors* in their ZIP code (i.e. monopolists) see no statistically significant change in their mean margins or prices." (p.4-5)

> The paper cites Miklos-Thal and Tucker (2019): improved demand prediction from algorithms "may lead to the possibility of collusion in markets where it is previously unsustainable, [but] in other markets it may create incentives for deviation that were absent with less prediction capabilities" (paraphrased, p.6).

**On price dispersion:**
> Table 7, columns 5-6 show that "adoption of algorithmic pricing has no effects on the average differences between station prices in a duopoly market. This is true both immediately after adoption and later. Since Table 5 shows that average market level prices increase after algorithmic adoption, this suggests that both adopting duopolists increase their prices by similar amounts after adoption." (p.37)

### How to position our paper relative to theirs

**The cleanest framing:** Assad et al. (2024) is the first-mover empirical paper on algorithmic pricing and competition. They find that AP raises margins in a setting that is maximally conducive to tacit collusion: (a) homogeneous product, (b) duopoly, (c) mandated real-time price transparency, (d) geographically isolated competitors. Our Airbnb paper provides the natural complement -- studying AP in a setting that is *minimally* conducive to tacit collusion: (a) highly differentiated product, (b) many sellers per market, (c) imperfect price transparency (differentiation makes comparison difficult), (d) the algorithm is designed for demand prediction and revenue management, not competitive interaction.

**Specific contrasts:**

| Dimension | Assad et al. (Gasoline) | Our paper (Airbnb) |
|---|---|---|
| Product | Homogeneous | Highly differentiated |
| Market structure | Duopoly (median 2 stations/ZIP) | Many sellers (dozens per market) |
| Price transparency | Perfect, mandated real-time | Moderate; prices visible but comparison difficult |
| Algorithm provider | Multiple third-party providers | Single platform-provided tool |
| Algorithm design | Competitive reaction ("react to rival changes") | Demand prediction / revenue management |
| Hub-and-spoke | Possible (multiple stations may use same provider) | By construction (all users use Airbnb's tool) |
| Key result | +38% margin increase (both adopt, duopoly) | Null on price levels |
| Price dispersion | No effect (between duopolists) | [Our result: increased within-listing variance] |
| Timing | Effects emerge after ~12 months | [Our timing to be analyzed] |

**Framing the null as complementary:**
- "Assad et al. (2024) document that algorithmic pricing raises margins when duopolists selling a homogeneous product both adopt price-responsive algorithms under mandated transparency. We study the opposite end of the spectrum: a differentiated-product platform market with many sellers, where the algorithm is designed for demand-side prediction rather than competitive reaction. Our null finding on price levels, combined with effects on price *variance*, suggests that market structure fundamentally mediates whether algorithmic pricing operates through the competition channel (raising levels) or the efficiency channel (improving demand tracking)."
- This is the right framing. It positions both papers as mapping out the frontier of when AP does and does not soften competition, rather than treating one as contradicting the other.
- The key insight is that the *mechanism* differs: in gasoline, AP works through faster punishment of undercutting (the competitive-interaction channel). In Airbnb, AP works through better demand forecasting (the efficiency channel), which shows up as price *variance* (tracking demand fluctuations) rather than price *levels*.

**Additional positioning note:** Their finding that monopolist adopters see the 95th percentile of prices *fall* (by 1.2 cents) is potentially analogous to what our algorithm does. Even in their setting, AP has a demand-tracking efficiency component -- it prevents monopolists from setting "too high" prices. In our many-seller setting, this efficiency channel dominates because the competitive-interaction channel is weak (too many sellers, differentiated product, no clear "punishment" mechanism).
