# Algorithmic Pricing and Market Conduct: Evidence from Airbnb Smart Pricing

**Richeng Piao**
Assistant Teaching Professor of Economics, Northeastern University
[richeng.info](https://www.richeng.info/)

---

## Abstract

We study the market-level effects of Airbnb's redesigned algorithmic pricing tools across eight major U.S. cities. Using a sharp reduced-form regression discontinuity design exploiting the platform-wide September 2023 rollout, we estimate the intent-to-treat effect of algorithm availability on listing prices and price dispersion. The aggregate price-level effect is small and bandwidth-sensitive: the pooled ITT ranges from 1.9 percent at ±30 days to 0.5 percent at ±90 days --- an order of magnitude below the effects documented in oligopolistic markets. A balanced-panel specification and controls for simultaneous platform policy changes confirm that the result is not driven by compositional shifts or bundled treatments. The RDD finds increased within-listing price variance, but a year-over-year DiD yields the opposite sign, leaving the variance result's robustness uncertain. Pricing changes concentrate among hosts with high pre-existing pricing sophistication, a descriptive pattern consistent with technology-skill complementarity. Together with evidence of algorithmic collusion in gasoline duopolies (Assad et al. 2024), these findings suggest that market structure mediates whether pricing algorithms raise prices or merely alter pricing patterns.

**JEL codes**: L13, L41, L81, D43, C21

**Keywords**: algorithmic pricing, price discrimination, regression discontinuity, platform markets, Airbnb, technology-skill complementarity

---

## Key Results

| Specification | ±30 days | ±45 days | ±60 days | ±90 days |
|---|---|---|---|---|
| **Full panel (residualized)** | 1.93%*** | 0.95%*** | 0.67%*** | 0.51%*** |
| **Balanced panel** | 1.95%*** | 1.08%*** | 0.73%*** | 0.43%*** |
| **With min-nights control** | 1.91%*** | 0.93%*** | 0.64%*** | 0.48%*** |
| **Year-over-year DiD** | | | -0.54%*** | |

- Price effects are positive but small (0.5--1.9%), declining with bandwidth
- An order of magnitude below the 38% found in gasoline duopolies (Assad et al. 2024)
- Variance finding is suggestive but not robust across identification strategies (RDD positive, DiD negative)

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
