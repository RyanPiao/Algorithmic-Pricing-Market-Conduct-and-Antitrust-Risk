### Placebo Bandwidth Profile: Main (Residualized, 2023) vs. Placebo (Raw, 2022)

Placebo test: identical RDD specification run at Sep 1, 2022 (no treatment).
If the placebo shows a similar pattern, the main result reflects seasonality,
not a causal effect.

| BW (days) | Main τ (2023) | SE | p-val | Placebo τ (2022) | SE | p-val | N (main) | N (placebo) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ±30d | 0.0193*** | 0.0006 | 0.000 | -37.0391 | 2535.9035 | 0.988 | 7,473,139 | 1,825,937 |
| ±45d | 0.0095*** | 0.0007 | 0.000 | -908534900.2835 | 26584769052.2670 | 0.973 | 11,184,927 | 3,091,381 |
| ±60d | 0.0067*** | 0.0007 | 0.000 | 1.5425 | 114.0336 | 0.989 | 14,896,717 | 4,356,798 |
| ±90d | 0.0051*** | 0.0008 | 0.000 | 233756527.8968 | 8665156414.7786 | 0.978 | 22,228,725 | 6,887,594 |

Notes: Local linear RDD with listing-clustered SEs. Main cutoff = Sep 1, 2023.
Placebo cutoff = Sep 1, 2022. Outcome = log(price). * p<0.10, ** p<0.05, *** p<0.01.

---

### Placebo Bandwidth Profile: Raw 2023 vs. Raw 2022 (apples-to-apples)

Placebo test: identical RDD specification run at Sep 1, 2022 (no treatment).
If the placebo shows a similar pattern, the main result reflects seasonality,
not a causal effect.

| BW (days) | Main τ (2023) | SE | p-val | Placebo τ (2022) | SE | p-val | N (main) | N (placebo) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ±30d | 0.0150*** | 0.0007 | 0.000 | -37.0391 | 2535.9035 | 0.988 | 7,473,139 | 1,825,937 |
| ±45d | -0.0041*** | 0.0008 | 0.000 | -908534900.2835 | 26584769052.2670 | 0.973 | 11,184,927 | 3,091,381 |
| ±60d | -0.0108*** | 0.0008 | 0.000 | 1.5425 | 114.0336 | 0.989 | 14,896,717 | 4,356,798 |
| ±90d | -0.0116*** | 0.0009 | 0.000 | 233756527.8968 | 8665156414.7786 | 0.978 | 22,228,725 | 6,887,594 |

Notes: Local linear RDD with listing-clustered SEs. Main cutoff = Sep 1, 2023.
Placebo cutoff = Sep 1, 2022. Outcome = log(price). * p<0.10, ** p<0.05, *** p<0.01.