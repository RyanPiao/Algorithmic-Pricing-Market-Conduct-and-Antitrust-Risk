### Wild Cluster Bootstrap: City-Level Inference

Main specification: `log_price_resid = α + τ·post + β₁·x + β₂·x·post + ε`
within ±60d bandwidth.

**Point estimate:** τ = 0.0067 (0.67% effect on prices)

| Inference Method | SE | t-stat | p-value | Clusters |
|---|---:|---:|---:|---:|
| Listing-clustered (analytical) | 0.0007 | 9.276 | 0.0000*** | 130,856 |
| City-clustered (analytical) | 0.0061 | 1.090 | 0.2759 | 8 |
| Wild cluster bootstrap (city) | — | — | 0.2472 | 8 |

N = 14,896,717 listing-day observations.
Wild cluster bootstrap: 999 iterations, Rademacher weights,
seed = 42.

Bootstrap t-statistic distribution:
  - Mean: -0.0264
  - Std:  0.8832
  - 5th percentile: -1.4472
  - 95th percentile: 1.5212

Reference: Cameron, Gelbach & Miller (2008), 'Bootstrap-Based
Improvements for Inference with Clustered Errors', REStat.