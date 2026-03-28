#!/usr/bin/env python3
"""Session 3, Script 09: DDD variance analysis.

Year-over-year DiD on within-listing price variance:
  var(log_price)_it = α_i + γ_w + τ · year2023 + ε_it

Also: collapsed listing × year paired comparison.

Output:
  - output/tables/ddd_variance.{tex,md}
  - output/figures/ddd_variance_scatter.{pdf,png}
  - data/processed/ddd_variance_results.json
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "processed"
TABLE_DIR = REPO / "output" / "tables"
FIG_DIR = REPO / "output" / "figures"
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42

plt.rcParams.update({
    "font.family": "serif", "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
})


def demean_twoway(df, y_col, fe1_col, fe2_col, max_iter=10, tol=1e-10):
    resid = df[y_col].values.astype(np.float64).copy()
    for _ in range(max_iter):
        m1 = pd.Series(resid).groupby(df[fe1_col].values).transform("mean").values
        resid -= m1
        m2 = pd.Series(resid).groupby(df[fe2_col].values).transform("mean").values
        resid -= m2
        if np.abs(m1).max() < tol and np.abs(m2).max() < tol:
            break
    return resid


def format_stars(p):
    if p < 0.01: return "***"
    if p < 0.05: return "**"
    if p < 0.10: return "*"
    return ""


def main():
    print("[1/5] Loading DDD panel...")
    df = pd.read_parquet(DATA_DIR / "ddd_panel.parquet")
    print(f"  {len(df):,} rows")

    print("[2/5] Computing rolling variance...")
    df = df.sort_values(["listing_city", "date"]).reset_index(drop=True)
    grp = df.groupby("listing_city")["log_price"]

    print("  7-day rolling variance...")
    df["var_7d"] = grp.rolling(7, min_periods=4).var().reset_index(level=0, drop=True)
    print("  14-day rolling variance...")
    df["var_14d"] = grp.rolling(14, min_periods=7).var().reset_index(level=0, drop=True)

    print("[3/5] Year-over-year DiD on rolling variance...")
    var_results = []

    for var_col, label in [("var_7d", "7-day Var(log price)"), ("var_14d", "14-day Var(log price)")]:
        valid = df[var_col].notna()
        sub = df[valid].copy()
        print(f"  {label}: {len(sub):,} obs...")

        y_dm = demean_twoway(sub, var_col, "listing_city", "week_of_year")
        x_dm = demean_twoway(sub, "year2023", "listing_city", "week_of_year")

        model = sm.OLS(y_dm, x_dm).fit(
            cov_type="cluster",
            cov_kwds={"groups": sub["listing_city"].values},
        )

        r = {
            "label": label,
            "coef": round(float(model.params[0]), 6),
            "se": round(float(model.bse[0]), 6),
            "ci_lower": round(float(model.conf_int()[0, 0]), 6),
            "ci_upper": round(float(model.conf_int()[0, 1]), 6),
            "pval": round(float(model.pvalues[0]), 6),
            "n_obs": int(model.nobs),
            "status": "ok",
        }
        s = format_stars(r["pval"])
        print(f"    τ={r['coef']:.6f}{s} (SE={r['se']:.6f}), p={r['pval']:.4f}")
        var_results.append(r)

    print("[4/5] Collapsed listing × year variance (paired comparison)...")
    collapsed = (
        df.groupby(["listing_city", "city_slug", "year"])["log_price"]
        .agg(["var", "std", "mean", "count"])
        .reset_index()
        .rename(columns={"var": "listing_var", "std": "listing_std",
                         "mean": "listing_mean", "count": "n_days"})
    )
    # Keep listings with enough obs in both years
    collapsed = collapsed[collapsed["n_days"] >= 14]

    pivot = collapsed.pivot_table(
        index="listing_city", columns="year",
        values=["listing_var", "listing_std", "listing_mean", "n_days"],
    )
    # Drop listings missing a year
    pivot = pivot.dropna()
    print(f"  {len(pivot):,} listings with ≥14 days in both years")

    var_2022 = pivot[("listing_var", 2022)].values
    var_2023 = pivot[("listing_var", 2023)].values
    diff = var_2023 - var_2022

    from scipy import stats as sp_stats
    t_stat, p_val = sp_stats.ttest_rel(var_2023, var_2022)
    mean_diff = diff.mean()
    se_diff = diff.std() / np.sqrt(len(diff))

    print(f"  Paired t-test: Δvar = {mean_diff:.6f} (SE={se_diff:.6f}), t={t_stat:.2f}, p={p_val:.4f}")
    print(f"  Mean var 2022: {var_2022.mean():.6f}, 2023: {var_2023.mean():.6f}")

    paired_result = {
        "mean_var_2022": round(float(var_2022.mean()), 6),
        "mean_var_2023": round(float(var_2023.mean()), 6),
        "mean_diff": round(float(mean_diff), 6),
        "se_diff": round(float(se_diff), 6),
        "t_stat": round(float(t_stat), 2),
        "pval": round(float(p_val), 6),
        "n_listings": int(len(pivot)),
    }

    # City-level paired comparison
    city_var = []
    listing_city_col = collapsed.set_index("listing_city")
    for city in sorted(df["city_slug"].unique()):
        city_listings = df[df["city_slug"] == city]["listing_city"].unique()
        cpivot = pivot.loc[pivot.index.isin(city_listings)]
        if len(cpivot) < 10:
            continue
        v22 = cpivot[("listing_var", 2022)].values
        v23 = cpivot[("listing_var", 2023)].values
        d = v23 - v22
        pct = (d.mean() / v22.mean() * 100) if v22.mean() > 0 else np.nan
        city_var.append({
            "city": city,
            "var_2022": round(float(v22.mean()), 6),
            "var_2023": round(float(v23.mean()), 6),
            "diff": round(float(d.mean()), 6),
            "pct_change": round(float(pct), 1),
            "n_listings": int(len(cpivot)),
        })
        print(f"  {city}: 2022={v22.mean():.6f}, 2023={v23.mean():.6f}, Δ={d.mean():+.6f} ({pct:+.1f}%)")

    print("[5/5] Saving...")

    # Scatter plot: 2022 vs 2023 variance by listing
    fig, ax = plt.subplots(figsize=(6, 6))
    # Subsample for visibility
    rng = np.random.RandomState(SEED)
    idx = rng.choice(len(var_2022), size=min(5000, len(var_2022)), replace=False)
    ax.scatter(var_2022[idx], var_2023[idx], s=2, alpha=0.3, color="#2166ac")
    lim = min(np.percentile(var_2022, 99), np.percentile(var_2023, 99))
    ax.plot([0, lim], [0, lim], "k--", linewidth=0.8, label="45° line")
    ax.set_xlabel("Within-listing Var(log price), 2022")
    ax.set_ylabel("Within-listing Var(log price), 2023")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.legend(fontsize=9)
    ax.set_title("Listing-Level Price Variance: 2022 vs 2023")
    fig.savefig(FIG_DIR / "ddd_variance_scatter.pdf")
    fig.savefig(FIG_DIR / "ddd_variance_scatter.png")
    plt.close()

    # Tables
    lines = ["### DDD Variance Estimates", "",
             "| Outcome | τ | SE | 95% CI | p-val | N |",
             "|---|---:|---:|---|---:|---:|"]
    for r in var_results:
        s = format_stars(r["pval"])
        lines.append(f"| {r['label']} | {r['coef']:.6f}{s} | {r['se']:.6f} "
                     f"| [{r['ci_lower']:.6f}, {r['ci_upper']:.6f}] | {r['pval']:.4f} | {r['n_obs']:,} |")
    (TABLE_DIR / "ddd_variance.md").write_text("\n".join(lines))

    city_lines = ["### Paired Variance Comparison by City", "",
                  "| City | Var 2022 | Var 2023 | Δ | % Change | N |",
                  "|---|---:|---:|---:|---:|---:|"]
    for cv in city_var:
        city_lines.append(f"| {cv['city']} | {cv['var_2022']:.6f} | {cv['var_2023']:.6f} "
                         f"| {cv['diff']:+.6f} | {cv['pct_change']:+.1f}% | {cv['n_listings']:,} |")
    (TABLE_DIR / "ddd_variance_city.md").write_text("\n".join(city_lines))

    all_results = {
        "rolling_var_did": var_results,
        "paired_test": paired_result,
        "city_variance": city_var,
    }
    (DATA_DIR / "ddd_variance_results.json").write_text(json.dumps(all_results, indent=2))
    print("Done.")


if __name__ == "__main__":
    main()
