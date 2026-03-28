#!/usr/bin/env python3
"""Session 3, Script 10: DDD event study.

Week-by-week year2023 coefficients after listing FE + week-of-year FE
demeaning. Reference: week 38 (first full overlap week).

Memory-efficient: compute from group means of demeaned outcome.

Output:
  - output/figures/ddd_event_study_price.{pdf,png}
  - output/tables/ddd_event_study_coefs.md
  - data/processed/ddd_event_study_results.json
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
from scipy import stats

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "processed"
TABLE_DIR = REPO / "output" / "tables"
FIG_DIR = REPO / "output" / "figures"
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
REF_WEEK = 38  # Reference week (first full overlap)

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


def estimate_event_study(df, outcome_col):
    """Estimate week-specific year2023 effects via regression.

    After demeaning by listing FE and week-of-year FE, regress on
    week × year2023 interaction dummies (excluding reference week).
    """
    print(f"  Demeaning {outcome_col}...")
    y_dm = demean_twoway(df, outcome_col, "listing_city", "week_of_year")

    weeks = sorted(df["week_of_year"].unique())
    weeks_excl_ref = [w for w in weeks if w != REF_WEEK]

    # Build interaction dummies: year2023 × I(week=w)
    print(f"  Building {len(weeks_excl_ref)} interaction dummies...")
    X_cols = []
    col_names = []
    for w in weeks_excl_ref:
        dummy = ((df["week_of_year"].values == w) & (df["year2023"].values == 1)).astype(np.float64)
        # Demean the dummy by the same two-way FE
        df[f"_tmp_w{w}"] = dummy
        dummy_dm = demean_twoway(df, f"_tmp_w{w}", "listing_city", "week_of_year")
        df.drop(columns=[f"_tmp_w{w}"], inplace=True)
        X_cols.append(dummy_dm)
        col_names.append(w)

    X = np.column_stack(X_cols)
    print(f"  Regressing ({X.shape[0]:,} × {X.shape[1]})...")

    model = sm.OLS(y_dm, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["listing_city"].values},
    )

    coefs = []
    for i, w in enumerate(col_names):
        coefs.append({
            "week": int(w),
            "coef": float(model.params[i]),
            "se": float(model.bse[i]),
            "ci_lower": float(model.conf_int()[i, 0]),
            "ci_upper": float(model.conf_int()[i, 1]),
            "pval": float(model.pvalues[i]),
        })

    # Add reference week
    coefs.append({
        "week": int(REF_WEEK),
        "coef": 0.0, "se": 0.0,
        "ci_lower": 0.0, "ci_upper": 0.0, "pval": 1.0,
    })

    coef_df = pd.DataFrame(coefs).sort_values("week")

    # Parallel trends test: F-test on weeks 38-39
    pre_weeks = [w for w in col_names if w <= 39 and w != REF_WEEK]
    if pre_weeks:
        pre_idx = [col_names.index(w) for w in pre_weeks]
        R = np.zeros((len(pre_idx), len(col_names)))
        for j, idx in enumerate(pre_idx):
            R[j, idx] = 1.0
        f_test = model.f_test(R)
        f_stat = float(f_test.fvalue)
        f_pval = float(f_test.pvalue)
        print(f"  Parallel trends F-test (weeks {pre_weeks}): F={f_stat:.2f}, p={f_pval:.3f}")
    else:
        f_stat, f_pval = np.nan, np.nan

    meta = {
        "outcome": outcome_col,
        "ref_week": REF_WEEK,
        "n_obs": int(model.nobs),
        "n_clusters": int(df["listing_city"].nunique()),
        "parallel_trends_F": round(f_stat, 4) if not np.isnan(f_stat) else None,
        "parallel_trends_p": round(f_pval, 4) if not np.isnan(f_pval) else None,
    }

    return coef_df, meta


def plot_event_study(coef_df, meta, filename, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))

    x = coef_df["week"].values
    y = coef_df["coef"].values
    ci_lo = coef_df["ci_lower"].values
    ci_hi = coef_df["ci_upper"].values

    ax.fill_between(x, ci_lo, ci_hi, alpha=0.2, color="#2166ac")
    ax.plot(x, y, "o-", color="#2166ac", markersize=4, linewidth=1.5)
    ax.axhline(0, color="black", linewidth=0.5)

    # Sep 1 ≈ week 35, Oct 1 ≈ week 40
    ax.axvline(40, color="#b2182b", linewidth=1.5, linestyle="--", label="Oct 1 (full rollout effect)")
    ax.axvspan(38, 39.5, alpha=0.1, color="green", label="Parallel trends window")

    ax.set_xlabel("Week of year")
    ax.set_ylabel(ylabel)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_xticks(range(38, 53, 2))

    pt_text = ""
    if meta.get("parallel_trends_p") is not None:
        pt_text = f"  |  Parallel trends: F={meta['parallel_trends_F']:.2f}, p={meta['parallel_trends_p']:.3f}"
    ax.text(0.02, 0.02,
            f"N = {meta['n_obs']:,}  |  Clusters = {meta['n_clusters']:,}{pt_text}",
            transform=ax.transAxes, fontsize=8, color="gray")

    plt.tight_layout()
    fig.savefig(FIG_DIR / f"{filename}.pdf")
    fig.savefig(FIG_DIR / f"{filename}.png")
    plt.close()
    print(f"  → {FIG_DIR}/{filename}.{{pdf,png}}")


def main():
    print("[1/3] Loading DDD panel...")
    df = pd.read_parquet(DATA_DIR / "ddd_panel.parquet")
    print(f"  {len(df):,} rows, weeks {df['week_of_year'].min()}-{df['week_of_year'].max()}")

    print("\n[2/3] Price level event study...")
    price_coefs, price_meta = estimate_event_study(df, "log_price")

    print("\n  Week coefficients:")
    for _, row in price_coefs.iterrows():
        s = "***" if row["pval"] < 0.01 else "**" if row["pval"] < 0.05 else "*" if row["pval"] < 0.10 else ""
        ref = " (ref)" if row["se"] == 0 else ""
        print(f"    Week {int(row['week']):2d}: δ={row['coef']:+.4f}{s}{ref}")

    print("\n[3/3] Plotting and saving...")
    plot_event_study(price_coefs, price_meta, "ddd_event_study_price",
                     "Year 2023 vs 2022 difference\n(log price, listing & week-of-year FE)")

    # Coefficients table
    lines = ["### DDD Event Study: Week-by-Week Year 2023 vs 2022 Differences", "",
             "| Week | δ | SE | 95% CI | p-val |",
             "|---:|---:|---:|---|---:|"]
    for _, row in price_coefs.iterrows():
        ref = " (ref)" if row["se"] == 0 else ""
        lines.append(f"| {int(row['week'])}{ref} | {row['coef']:.4f} | {row['se']:.4f} "
                     f"| [{row['ci_lower']:.4f}, {row['ci_upper']:.4f}] | {row['pval']:.3f} |")
    (TABLE_DIR / "ddd_event_study_coefs.md").write_text("\n".join(lines))

    results = {"price": {"meta": price_meta, "coefs": price_coefs.to_dict(orient="records")}}
    (DATA_DIR / "ddd_event_study_results.json").write_text(json.dumps(results, indent=2, default=str))

    print("Done.")


if __name__ == "__main__":
    main()
