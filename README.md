# Algorithmic Pricing and Market Conduct: Evidence from Airbnb Smart Pricing

**Richeng Piao**
Department of Economics, Northeastern University
[richeng.info](https://www.richeng.info/)

*Working Paper, March 2026*

---

## Abstract

Short-term rental platforms have transformed urban housing markets, and pricing algorithms are increasingly central to how hosts set nightly rates. We study the rollout of Airbnb's redesigned pricing tools across eight major U.S. cities using a sharp regression discontinuity design exploiting the platform-wide September 2023 rollout. Point estimates for the price-level effect are positive in all eight cities (0.5--1.9 percent depending on bandwidth). The sign consistency is statistically significant (sign test *p* = 0.004; Wilcoxon *p* = 0.008), but a wild cluster bootstrap accounting for only 8 independent city-level clusters yields *p*-values of 0.15--0.20, and a year-over-year difference-in-differences gives opposite-signed estimates. The true effect is bounded between −0.5% and +1.9%, with zero inside the interval. City-level heterogeneity tracks regulatory stringency: larger effects in less-regulated markets and smaller effects in heavily regulated markets. These effects are substantially below the 38% margin increase documented in gasoline duopolies (Assad et al. 2024), suggesting that market structure mediates the competitive effects of algorithmic pricing.

**JEL codes**: L13, L41, L81, D43, C21

**Keywords**: algorithmic pricing, short-term rentals, regression discontinuity, platform markets, Airbnb

---

## Key Results

| Bandwidth | Point estimate | *p* (wild bootstrap) | *p* (sign test) | N |
|---|---|---|---|---|
| ±30 days | +1.93% | 0.183 | 0.004 | 7,473,139 |
| ±45 days | +0.95% | 0.147 | — | 11,184,927 |
| ±60 days | +0.67% | 0.151 | 0.004 | 14,896,717 |
| ±90 days | +0.51% | 0.198 | — | 22,228,725 |

*Notes*: Intent-to-treat estimates on residualized log prices. Local linear RDD with cross-fitted residualization. Wild cluster bootstrap with Rademacher weights at city level (8 clusters), 999 iterations.

---

## Repository Structure

```
├── chapters/                  # Manuscript source (.qmd, Quarto)
│   ├── 01-introduction.qmd
│   ├── 02-data-and-setting.qmd
│   ├── 03-empirical-strategy.qmd
│   ├── 04-results.qmd
│   ├── 05-related-work.qmd
│   └── 06-conclusion.qmd
├── code/                      # Replication scripts (Python)
│   ├── s3_01_build_panel.py        # Panel construction
│   ├── s3_02_residualize.py        # Cross-fitted residualization
│   ├── s3_03_itt_rdd.py            # ITT RDD + balanced panel + controls
│   ├── s3_04_variance.py           # Price variance analysis
│   ├── s3_05_event_study.py        # Event study
│   ├── s3_06_falsification.py      # Density, balance, LOO, MDE
│   ├── s3_07_build_ddd_panel.py    # Year-over-year panel
│   ├── s3_08_ddd_price_levels.py   # DiD price levels
│   ├── s3_09_ddd_variance.py       # DiD variance
│   ├── s3_10_ddd_event_study.py    # DiD event study
│   ├── s3_11_ddd_falsification.py  # DiD robustness
│   ├── s3_13_placebo_bandwidth.py  # Placebo cutoff test
│   └── s3_14_wild_bootstrap.py     # Wild cluster bootstrap
├── output/
│   ├── tables/                # Result tables (.md, .tex)
│   └── figures/               # Figures (.png, .pdf)
├── data/                      # Data (not tracked; see below)
├── _book/                     # Compiled manuscript (PDF)
├── _quarto.yml                # Quarto configuration
├── index.qmd                  # Abstract
├── references.bib             # Bibliography
├── requirements.txt           # Python dependencies
└── LICENSE
```

---

## Replication

### Prerequisites

- Python 3.11+
- [Quarto](https://quarto.org/) 1.4+ (for manuscript compilation)
- TinyTeX or TeX Live (for PDF output)

### Data

The analysis uses publicly available data from [Inside Airbnb](https://insideairbnb.com/) for eight U.S. cities: Austin, Boston, Chicago, Los Angeles, New York City, San Francisco, Seattle, and Washington, DC. Raw data files are not included due to size.

To replicate:
1. Download calendar and listing data from [Inside Airbnb](https://insideairbnb.com/get-the-data/) for each city
2. Place merged city files in `data/merge/` as `merged_{city-slug}.csv`

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Analysis

Scripts are numbered and should be run in order:

```bash
python code/s3_01_build_panel.py       # Build listing-day panel
python code/s3_02_residualize.py       # Cross-fitted residualization
python code/s3_03_itt_rdd.py           # Primary ITT RDD estimates
python code/s3_04_variance.py          # Variance analysis
python code/s3_05_event_study.py       # Event study figures
python code/s3_06_falsification.py     # Diagnostics and robustness
python code/s3_07_build_ddd_panel.py   # Year-over-year panel
python code/s3_08_ddd_price_levels.py  # DiD price levels
python code/s3_09_ddd_variance.py      # DiD variance
python code/s3_10_ddd_event_study.py   # DiD event study
python code/s3_11_ddd_falsification.py # DiD robustness
python code/s3_13_placebo_bandwidth.py # Placebo cutoff test
python code/s3_14_wild_bootstrap.py    # Wild cluster bootstrap
```

Output tables are written to `output/tables/` and figures to `output/figures/`.

### Compiling the Manuscript

```bash
quarto render --to pdf
```

The compiled PDF is output to `_book/`.

---

## Citation

```bibtex
@unpublished{piao2026algorithmic,
  author = {Piao, Richeng},
  title  = {Algorithmic Pricing and Market Conduct:
            Evidence from {Airbnb} Smart Pricing},
  note   = {Working Paper, Northeastern University},
  year   = {2026}
}
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
