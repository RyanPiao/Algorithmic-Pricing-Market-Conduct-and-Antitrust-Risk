#!/usr/bin/env python3
"""Session 3, Script 11: DDD falsification and robustness.

1. Placebo outcomes (min_nights, availability)
2. Leave-one-city-out
3. Power analysis / MDE

Output:
  - output/tables/ddd_placebo.md
  - output/tables/ddd_loo.md
  - output/figures/ddd_mde_power.{pdf,png}
  - data/processed/ddd_falsification_results.json
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


def run_did_simple(df, y_col, fe1, fe2, cluster_col, label):
    """Year-over-year DiD: demeaned y on demeaned year2023."""
    valid = df[y_col].notna()
    sub = df[valid].copy()
    if len(sub) < 100:
        return {"label": label, "status": "insufficient_data"}

    y_dm = demean_twoway(sub, y_col, fe1, fe2)
    x_dm = demean_twoway(sub, "year2023", fe1, fe2)

    model = sm.OLS(y_dm, x_dm).fit(
        cov_type="cluster",
        cov_kwds={"groups": sub[cluster_col].values},
    )
    return {
        "label": label,
        "coef": round(float(model.params[0]), 6),
        "se": round(float(model.bse[0]), 6),
        "pval": round(float(model.pvalues[0]), 6),
        "n_obs": int(model.nobs),
        "status": "ok",
    }


def format_stars(p):
    if p < 0.01: return "***"
    if p < 0.05: return "**"
    if p < 0.10: return "*"
    return ""


def main():
    print("[1/4] Loading DDD panel...")
    df = pd.read_parquet(DATA_DIR / "ddd_panel.parquet")
    print(f"  {len(df):,} rows")

    all_results = {}

    # ── 1. Placebo outcomes ──────────────────────────────────────────────

    print("\n[2/4] Placebo outcomes...")
    placebo_results = []
    for col, label in [("minimum_nights", "Minimum nights"), ("available", "Availability")]:
        print(f"  {label}...")
        r = run_did_simple(df, col, "listing_city", "week_of_year", "listing_city", label)
        if r["status"] == "ok":
            s = format_stars(r["pval"])
            print(f"    τ={r['coef']:.4f}{s} (SE={r['se']:.4f}), p={r['pval']:.3f}")
        placebo_results.append(r)
    all_results["placebo"] = placebo_results

    # ── 2. Leave-one-city-out ────────────────────────────────────────────

    print("\n[3/4] Leave-one-city-out...")
    loo_results = []
    for city in sorted(df["city_slug"].unique()):
        sub = df[df["city_slug"] != city]
        r = run_did_simple(sub, "log_price", "listing_city", "week_of_year", "listing_city", f"Drop {city}")
        if r["status"] == "ok":
            s = format_stars(r["pval"])
            print(f"  Drop {city}: τ={r['coef']:.4f}{s} (SE={r['se']:.4f}), N={r['n_obs']:,}")
        loo_results.append(r)
    all_results["leave_one_out"] = loo_results

    # ── 3. Power analysis ────────────────────────────────────────────────

    print("\n[4/4] Power analysis...")
    # Get primary SE from price results
    price_path = DATA_DIR / "ddd_price_results.json"
    if price_path.exists():
        price_res = json.loads(price_path.read_text())
        primary = [r for r in price_res["pooled"] if r["status"] == "ok"]
        primary_se = primary[0]["se"] if primary else 0.005
    else:
        primary_se = 0.005

    z_alpha = 1.96
    mde_80 = (z_alpha + 0.842) * primary_se
    mde_95 = (z_alpha + 1.645) * primary_se
    mde_80_pct = (np.exp(mde_80) - 1) * 100
    mde_95_pct = (np.exp(mde_95) - 1) * 100

    print(f"  Primary SE: {primary_se:.6f}")
    print(f"  MDE at 80% power: {mde_80:.4f} log points ({mde_80_pct:.2f}%)")
    print(f"  MDE at 95% power: {mde_95:.4f} log points ({mde_95_pct:.2f}%)")

    all_results["power"] = {
        "se": round(primary_se, 6),
        "mde_80_logpts": round(mde_80, 6),
        "mde_80_pct": round(mde_80_pct, 2),
        "mde_95_logpts": round(mde_95, 6),
        "mde_95_pct": round(mde_95_pct, 2),
    }

    # Power curve
    effects = np.linspace(0, 0.10, 200)
    power_vals = [stats.norm.cdf(e / primary_se - z_alpha) for e in effects]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(effects * 100, power_vals, color="#2166ac", linewidth=2)
    ax.axhline(0.80, color="gray", linewidth=0.8, linestyle="--", label="80% power")
    ax.axhline(0.95, color="gray", linewidth=0.8, linestyle=":", label="95% power")
    ax.axvline(mde_80_pct, color="#b2182b", linewidth=1, linestyle="--", alpha=0.7)
    ax.set_xlabel("True effect size (% price change)")
    ax.set_ylabel("Power")
    ax.set_title("Power Curve: DDD Minimum Detectable Effect")
    ax.legend(fontsize=9)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.02)
    fig.savefig(FIG_DIR / "ddd_mde_power.pdf")
    fig.savefig(FIG_DIR / "ddd_mde_power.png")
    plt.close()

    # ── Save ─────────────────────────────────────────────────────────────

    print("\nSaving...")

    # Placebo table
    lines = ["### DDD Placebo Outcomes", "",
             "| Outcome | τ | SE | p-val | N |",
             "|---|---:|---:|---:|---:|"]
    for r in placebo_results:
        if r["status"] == "ok":
            s = format_stars(r["pval"])
            lines.append(f"| {r['label']} | {r['coef']:.4f}{s} | {r['se']:.4f} | {r['pval']:.3f} | {r['n_obs']:,} |")
    (TABLE_DIR / "ddd_placebo.md").write_text("\n".join(lines))

    # LOO table
    lines = ["### Leave-One-City-Out", "",
             "| Dropped | τ | SE | p-val | N |",
             "|---|---:|---:|---:|---:|"]
    for r in loo_results:
        if r["status"] == "ok":
            lines.append(f"| {r['label']} | {r['coef']:.4f} | {r['se']:.4f} | {r['pval']:.3f} | {r['n_obs']:,} |")
    (TABLE_DIR / "ddd_loo.md").write_text("\n".join(lines))

    (DATA_DIR / "ddd_falsification_results.json").write_text(json.dumps(all_results, indent=2))
    print("Done.")


if __name__ == "__main__":
    main()
