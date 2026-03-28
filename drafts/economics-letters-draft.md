# Algorithmic Pricing in a Many-Seller Market: Evidence from Airbnb

**Richeng Piao**

Assistant Teaching Professor of Economics, Northeastern University

---

**Abstract.** Does algorithmic pricing raise market prices in differentiated-product platform markets? We exploit the platform-wide rollout of Airbnb's redesigned pricing tools on September 1, 2023 using a sharp regression discontinuity in time across eight major U.S. cities (7.5--22.2 million listing-day observations). Point estimates on residualized log prices are positive in all eight cities (sign test p = 0.004; city-level t-test p = 0.019), ranging from 0.5% to 1.9% depending on bandwidth. However, with only eight city-level clusters, wild cluster bootstrap p-values range from 0.15 to 0.20, and a year-over-year difference-in-differences yields estimates of the opposite sign. A bounding argument places the true effect in [-0.5%, +1.9%], with zero inside the bound. These effects are substantially smaller than the 38% margin increase documented in gasoline duopolies (Assad et al., 2024), suggesting that market structure---many sellers, differentiated products---mediates the competitive effects of algorithmic pricing.

**Keywords:** algorithmic pricing, platform markets, regression discontinuity, Airbnb, tacit collusion

**JEL codes:** L13, L41, L83, D43

---

## 1. Introduction

Pricing algorithms are reshaping competition in digital marketplaces. Recent enforcement actions---the DOJ's suit against RealPage, the FTC's surveillance pricing investigation, and the EU Digital Markets Act---reflect concern that when competing sellers delegate pricing to algorithms, especially those provided by a common platform, the result may be tacit collusion.

The empirical evidence, however, remains concentrated in settings maximally conducive to coordination. Assad et al. (2024) provide the strongest quasi-experimental evidence, documenting 38% margin increases when competing gasoline stations in German duopolies both adopt algorithmic pricing. Calvano et al. (2020) show theoretically that Q-learning agents converge to supra-competitive prices. These studies examine homogeneous products, duopoly or tight oligopoly, and real-time price transparency. Whether algorithmic pricing raises prices in the large, differentiated-product platform markets where it is most prevalent remains an open question.

We study the rollout of Airbnb's redesigned pricing tools across eight major U.S. cities. The platform's 2023 Summer Release introduced updated algorithmic pricing recommendations on September 1, 2023, providing a sharp regression discontinuity in time. We estimate the intent-to-treat effect of algorithm *availability* on listing prices using 7.5 to 22.2 million listing-day observations, with seasonal confounders removed via cross-fitted residualization (Hausman et al., 2018; Noack and Rothe, 2025).

Three results emerge. First, pooled ITT estimates are positive but small (0.5--1.9%) and decline monotonically with bandwidth. Second, all eight city-specific point estimates are positive (sign test p = 0.004), but inference is imprecise under city-level wild cluster bootstrap (p = 0.15--0.20). Third, the effects are an order of magnitude smaller than those in oligopolistic markets, suggesting market structure mediates algorithmic pricing effects.

## 2. Data and Setting

Airbnb launched Smart Pricing in November 2015, offering hosts automated nightly price recommendations based on local demand, seasonality, and listing characteristics (Ye et al., 2018). The tool is opt-in, with approximately 22% adoption (Foroughifar et al., 2024). The 2023 Summer Release substantially redesigned these tools, rolling them out to all hosts on September 1, 2023.

We use publicly available data from Inside Airbnb covering eight cities: Austin, Boston, Chicago, Los Angeles, New York City, San Francisco, Seattle, and Washington, DC. We construct a listing-day panel for the 2022--2023 period, with the running variable measuring days from the September 1, 2023 cutoff. Symmetric bandwidth windows of +/-30, +/-45, +/-60, and +/-90 days yield estimation samples of 7.5 to 22.2 million listing-day observations across approximately 130,000 unique listings. The outcome variable is log nightly listed price (USD), with observations capped at $10,000 per night.

Three data limitations bear noting. First, calendar prices are forward-looking posted prices, not realized transaction prices. Second, we cannot observe individual adoption of the redesigned tools, so estimates are intent-to-treat. Third, third-party pricing tools (Beyond Pricing, PriceLabs) may confound the treatment if their usage changed around the cutoff.

## 3. Empirical Strategy

**Primary specification.** We estimate the intent-to-treat reduced-form discontinuity:

$$\tilde{Y}_{ict} = \alpha + \tau \cdot \mathbf{1}[t \geq c_0] + \beta_1 r_t + \beta_2 r_t \cdot \mathbf{1}[t \geq c_0] + \varepsilon_{ict}$$

where $\tilde{Y}_{ict}$ is the residualized log price for listing $i$ in city $c$ on date $t$, $c_0$ is September 1, 2023, and $r_t = t - c_0$. The coefficient $\tau$ captures the ITT effect of algorithm availability.

**Residualization.** We address seasonal confounding through two-stage cross-fitted residualization. Stage 1 absorbs city $\times$ month-of-year and day-of-week fixed effects via iterative demeaning. Stage 2 subtracts cross-fitted Ridge regression predictions from Fourier harmonics, listing characteristics, and holiday indicators. This procedure is consistent for $\tau$ regardless of whether the adjustment function is correctly specified (Noack and Rothe, 2025, Theorem 1).

**Inference.** With eight cities sharing a common cutoff, listing-level clustering overstates precision. We report wild cluster bootstrap p-values at the city level (8 clusters, 999 Rademacher-weighted iterations) as our preferred inference, alongside nonparametric sign and rank tests that treat each city as one observation.

**Complementary DiD.** As a robustness check, we estimate a year-over-year difference-in-differences comparing 2023 to 2022 with listing and week-of-year fixed effects.

## 4. Results

### 4.1 Pooled estimates

Table 1 reports pooled ITT estimates with three levels of inference. After residualization, point estimates are positive at all bandwidths but decline monotonically: 1.93% at +/-30 days, 0.95% at +/-45 days, 0.67% at +/-60 days, and 0.51% at +/-90 days. With listing-level clustered standard errors, all estimates are highly significant (p < 0.001). However, city-level clustered standard errors---appropriate given that all listings within a city share the same cutoff---render the estimates insignificant (p = 0.26--0.33). Wild cluster bootstrap p-values range from 0.15 to 0.20 across all bandwidths. **None of the estimates are statistically significant at conventional levels when inference accounts for the small number of independent clusters.**

**Table 1: Wild cluster bootstrap results**

| BW | $\hat{\tau}$ | SE (listing) | p (listing) | SE (city) | p (city) | p (bootstrap) | N |
|---:|---:|---:|---:|---:|---:|---:|---:|
| +/-30d | 0.0193 | 0.0006 | <0.001 | 0.0179 | 0.281 | 0.183 | 7,473,139 |
| +/-45d | 0.0095 | 0.0007 | <0.001 | 0.0084 | 0.258 | 0.147 | 11,184,927 |
| +/-60d | 0.0067 | 0.0007 | <0.001 | 0.0061 | 0.276 | 0.151 | 14,896,717 |
| +/-90d | 0.0051 | 0.0008 | <0.001 | 0.0052 | 0.327 | 0.198 | 22,228,725 |

*Notes:* Residualized log price. Local linear RDD, symmetric bandwidth. Wild cluster bootstrap with Rademacher weights at city level (8 clusters), 999 iterations.

### 4.2 City-specific estimates and nonparametric tests

At the +/-60-day bandwidth, all eight city-specific point estimates are positive: Chicago (+5.6%), Seattle (+2.9%), Boston (+1.9%), Washington DC (+1.3%), Austin (+1.1%), New York City (+1.0%), San Francisco (+0.9%), and Los Angeles (+0.06%, p = 0.65). Table 2 reports nonparametric tests that treat each city as one observation.

**Table 2: Nonparametric tests on city-level estimates (+/-60d, residualized)**

| Test | Statistic | p-value |
|---|---:|---:|
| Sign test (7/8 positive) | --- | 0.004 (one-sided) |
| City-level t-test (df = 7) | t = 3.039 | 0.019 |
| Wilcoxon signed-rank | W = 0 | 0.008 |
| Wild cluster bootstrap | --- | 0.151 |

City-level mean effect: 1.84% (95% CI: [0.41%, 3.27%]).

The sign test and Wilcoxon test reject the null that the algorithm has no systematic directional effect across cities. The city-level t-test rejects at the 5% level. However, the wild cluster bootstrap, which accounts for within-city correlation and heteroskedasticity, does not reject.

### 4.3 Robustness and bounding

Three checks support robustness. A balanced-panel specification restricted to listings present on both sides of the cutoff produces nearly identical estimates (e.g., 1.95% vs. 1.93% at +/-30 days), ruling out compositional confounds. Controlling for simultaneous changes in minimum-night requirements leaves estimates unchanged. Leave-one-city-out analysis shows sensitivity to Los Angeles and New York City, the two largest markets.

The year-over-year DiD yields *negative* price estimates (-0.5% to -1.6%), indicating that the sign depends on the identification strategy. The RDD removes slow trends but retains seasonality; the DiD differences out seasonality but absorbs year-over-year market trends. A bounding argument places the true effect in [-0.5%, +1.9%], with zero inside the bound.

### 4.4 Event study

Figure 1 plots bi-weekly event-study coefficients on residualized log prices. Pre-period coefficients are small but nonzero (0.003--0.009), reflecting residual seasonality. Post-period coefficients show a modest upward shift in the first two weeks (0.015), followed by fluctuation between 0.004 and 0.014 with no clear trend. The nonzero pre-trends caution against interpreting the post-period shift as a cleanly identified treatment effect but are consistent with the small magnitudes reported in the RDD.

[Figure 1: Event study coefficients for residualized log prices around September 1, 2023 cutoff. Bi-weekly bins. Dashed vertical line marks the rollout date. See output/figures/event_study_price.png.]

## 5. Discussion and Conclusion

We provide the first large-scale quasi-experimental evidence on algorithmic pricing in a differentiated-product platform market with many sellers. The evidence supports three conclusions.

First, the directional effect is consistent: positive price effects appear in all eight cities (sign test p = 0.004). Second, the magnitude is small and imprecisely estimated: 0.5--1.9% under the RDD, statistically insignificant under wild cluster bootstrap, and potentially zero or negative under alternative identification. Third, even the upper bound of our estimates (1.9%) is substantially below the 38% documented in gasoline duopolies (Assad et al., 2024).

The comparison with Assad et al. (2024) requires three caveats. Our ITT is diluted by partial adoption (~22%); scaling by a plausible first-stage of 0.2--0.3 yields an implied treatment-on-the-treated of 2--10%, narrowing the gap. The market structures differ fundamentally: many differentiated sellers versus gasoline duopoly. And even modest per-listing effects aggregate at platform scale---a 0.5--1.9% price increase implies $50--190 million in additional annual consumer expenditure on Airbnb's U.S. gross booking volume.

These findings support a market-structure-contingent approach to algorithmic pricing enforcement. In concentrated markets with homogeneous products, algorithmic pricing poses genuine coordination risks. In many-seller differentiated-product markets, the same mechanisms lack structural traction: product heterogeneity defeats price-matching, many sellers defeat bilateral monitoring, and host discretion over base prices limits algorithmic commitment. Future work should examine whether effects concentrate in neighborhoods with few close substitutes, testing whether hub-and-spoke coordination operates locally even when it does not operate citywide.

---

**References**

Assad, S., Clark, R., Ershov, D., and Xu, L. (2024). Algorithmic pricing and competition: Empirical evidence from the German retail gasoline market. *Journal of Political Economy*, 132(3), 723--771.

Calvano, E., Calzolari, G., Denicolo, V., and Pastorello, S. (2020). Artificial intelligence, algorithmic pricing, and collusion. *American Economic Review*, 110(10), 3267--3297.

Calonico, S., Cattaneo, M.D., and Titiunik, R. (2014). Robust nonparametric confidence intervals for regression-discontinuity designs. *Econometrica*, 82(6), 2295--2326.

Cameron, A.C., Gelbach, J.B., and Miller, D.L. (2008). Bootstrap-based improvements for inference with clustered errors. *Review of Economics and Statistics*, 90(3), 414--427.

Foroughifar, A., Torabi, Z., and Li, X. (2024). Challenges in adoption of algorithmic pricing: Evidence from Airbnb. Working paper.

Hausman, C., and Rapson, D.S. (2018). Regression discontinuity in time: Considerations for empirical applications. *Annual Review of Resource Economics*, 10, 533--552.

Huang, Y. (2025). Pricing and welfare in short-term rental markets. Working paper.

Noack, C., and Rothe, C. (2025). Flexible covariate adjustments in regression discontinuity designs. Working paper.

Ye, P., Qian, J., Chen, J., Wu, C., Zhou, Y., De Mars, S., Yang, F., and Zhang, L. (2018). Customized regression model for Airbnb dynamic pricing. In *Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 932--940.
