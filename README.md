# Algorithmic Pricing and Market Conduct: Evidence from Airbnb Smart Pricing

**Richeng Piao**
Assistant Teaching Professor of Economics, Northeastern University
[richeng.info](https://www.richeng.info/)

---

## Abstract

We study the market-level effects of Airbnb's redesigned algorithmic pricing tools across eight major U.S. cities using a sharp reduced-form regression discontinuity design. Point estimates for the price-level effect are positive in all eight cities (0.5--1.9 percent depending on bandwidth). The sign consistency is statistically significant: a nonparametric sign test rejects zero at the 1% level (p = 0.004). However, a wild cluster bootstrap accounting for only 8 independent city-level clusters yields p-values of 0.15--0.20, and a year-over-year difference-in-differences gives opposite-signed estimates, indicating that the common-cutoff design lacks the precision to reliably quantify the effect's magnitude. The evidence suggests a small positive effect --- substantially below the 38% found in gasoline duopolies (Assad et al. 2024) even after adjusting for intent-to-treat dilution --- but the true effect is bounded between -0.5% and +1.9%, with zero inside the interval.

**JEL codes**: L13, L41, L81, D43, C21

**Keywords**: algorithmic pricing, price discrimination, regression discontinuity, platform markets, Airbnb

---

## Key Results

### Inference Comparison (±60-day bandwidth, residualized outcome)

| Inference Method | SE | p-value |
|---|---|---|
| Listing-clustered (130K clusters) | 0.0007 | 0.000*** |
| City-clustered analytical (8 clusters) | 0.0061 | 0.276 |
| **Wild cluster bootstrap (8 cities)** | — | **0.151** |
| **Sign test (8/8 positive)** | — | **0.004*** |
| **City-level t-test** | 0.0060 | **0.019** |

### Point Estimates by Bandwidth

| BW | τ (RDD) | p (bootstrap) | p (sign test) |
|---|---|---|---|
| ±30d | +1.93% | 0.183 | 0.004 |
| ±45d | +0.95% | 0.147 | — |
| ±60d | +0.67% | 0.151 | 0.004 |
| ±90d | +0.51% | 0.198 | — |

### Bounding Argument

- **RDD upper bound**: +1.9% (narrow bandwidth)
- **DiD lower bound**: -0.5%
- **True effect**: ∈ [-0.5%, +1.9%], zero inside
- **Assad et al. (2024) comparison**: 38% in gasoline duopolies vs. ~3% implied TOT here (~12.5x gap)

---

## Project Structure

```
.
├── chapters/               # Manuscript (.qmd files for Quarto)
│   ├── 01-introduction.qmd
│   ├── 02-data-and-setting.qmd
│   ├── 03-empirical-strategy.qmd
│   ├── 04-results.qmd
│   ├── 05-related-work.qmd
│   └── 06-conclusion.qmd
├── code/                   # Analysis scripts (Python)
│   ├── s3_01_build_panel.py
│   ├── s3_02_residualize.py
│   ├── s3_03_itt_rdd.py          # Primary ITT RDD + balanced panel + min-nights control
│   ├── s3_04_variance.py          # Variance RDD
│   ├── s3_05_event_study.py
│   ├── s3_06_falsification.py     # Density, balance, leave-one-out, MDE
│   ├── s3_07_build_ddd_panel.py
│   ├── s3_08_ddd_price_levels.py  # Year-over-year DiD
│   ├── s3_09_ddd_variance.py
│   ├── s3_10_ddd_event_study.py
│   └── s3_11_ddd_falsification.py
├── output/
│   ├── tables/             # Result tables (.md + .tex)
│   └── figures/            # Figures (.png + .pdf)
├── literature/             # Paper snapshots (5 Tier 1 papers)
├── synthesis/              # Literature review, debate map, gap analysis
├── reviews/                # Self-review and adversarial verification reports
├── external-research/      # AI-assisted research returns (Gemini, ChatGPT, Claude)
├── data/                   # Data directory (symlinks to external drive)
│   └── processed/          # Analysis-ready panels (.parquet, not tracked)
├── _book/                  # Compiled manuscript (PDF)
├── _quarto.yml             # Quarto book configuration
├── index.qmd               # Abstract and front matter
├── references.bib          # Bibliography (33 entries)
├── research-plan.md        # Research plan v2.0 with pivot rationale
├── reading-list-2026-03-22.md  # 32-paper prioritized reading list
└── STYLE_GUIDE.md          # Writing conventions
```

---

## Replication

### Prerequisites

- Python 3.11+ with packages: `pandas`, `numpy`, `statsmodels`, `rdrobust`, `scikit-learn`, `matplotlib`
- [Quarto](https://quarto.org/) 1.4+ for manuscript compilation
- TinyTeX or TeX Live for PDF output

### Data

The analysis uses publicly available data from [Inside Airbnb](https://insideairbnb.com/) for eight U.S. cities. Raw data files are not included in this repository due to size. To replicate:

1. Download calendar and listing data for Austin, Boston, Chicago, Los Angeles, New York City, San Francisco, Seattle, and Washington DC from Inside Airbnb
2. Place merged city files in `data/merge/` as `merged_{city-slug}.csv`

### Running the Analysis

```bash
# Create virtual environment
python -m venv .venv && source .venv/bin/activate
pip install pandas numpy statsmodels rdrobust scikit-learn matplotlib

# Run analysis pipeline (in order)
python code/s3_01_build_panel.py      # Build listing-day panel
python code/s3_02_residualize.py      # Cross-fitted residualization
python code/s3_03_itt_rdd.py          # ITT RDD (primary results)
python code/s3_04_variance.py         # Variance analysis
python code/s3_05_event_study.py      # Event study figures
python code/s3_06_falsification.py    # Diagnostics (density, balance, LOO, MDE)
python code/s3_07_build_ddd_panel.py  # Build year-over-year panel
python code/s3_08_ddd_price_levels.py # DiD price levels
python code/s3_09_ddd_variance.py     # DiD variance
python code/s3_10_ddd_event_study.py  # DiD event study
python code/s3_11_ddd_falsification.py # DiD robustness
```

### Compiling the Manuscript

```bash
quarto render --to pdf
# Output: _book/Algorithmic-Pricing-and-Market-Conduct--Evidence-from-Airbnb-Smart-Pricing.pdf
```

---

## Citation

```bibtex
@unpublished{piao2026algorithmic,
  author = {Piao, Richeng},
  title = {Algorithmic Pricing and Market Conduct: Evidence from {Airbnb} Smart Pricing},
  note = {Working Paper, Northeastern University},
  year = {2026}
}
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
