#!/usr/bin/env python3
"""Session 3, Script 06: Falsification tests and diagnostics.

1. McCrary/CJM density test at cutoff
2. Covariate balance tests
3. Placebo outcomes (minimum_nights, availability)
4. Leave-one-city-out robustness
5. Power analysis / MDE

Output:
  - output/tables/falsification_*.md + .tex
  - output/figures/density_test.pdf + .png
  - output/figures/mde_power.pdf + .png
  - data/processed/falsification_results.json
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
np.random.seed(SEED)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


# ── 1. Density test ─────────────────────────────────────────────────────

def density_test(df: pd.DataFrame) -> dict:
    """McCrary-style density test: are there bunching/manipulation at cutoff?

    For RDiT this tests whether listings systematically enter/exit
    around the cutoff date. We count unique listings per day and test
    for a discontinuity.
    """
    print("  [Density] Counting listings per day around cutoff...")
    daily = (
        df.groupby("days_from_cutoff")["listing_city"]
        .nunique()
        .reset_index()
        .rename(columns={"listing_city": "n_listings"})
    )

    # OLS local-linear on daily counts within ±60d
    bw = 60
    dsub = daily[(daily["days_from_cutoff"] >= -bw) & (daily["days_from_cutoff"] <= bw)]
    x = dsub["days_from_cutoff"].values.astype(float)
    post = (x >= 0).astype(float)
    X = np.column_stack([np.ones(len(x)), post, x, x * post])
    y_d = dsub["n_listings"].values.astype(float)

    model = sm.OLS(y_d, X).fit()
    coef = float(model.params[1])
    se = float(model.bse[1])
    pval = float(model.pvalues[1])
    status = "ok"
    print(f"  [Density] τ={coef:.2f}, SE={se:.2f}, p={pval:.3f}")

    # Plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(daily["days_from_cutoff"], daily["n_listings"], s=3, alpha=0.5, color="#2166ac")
    ax.axvline(0, color="#b2182b", linewidth=1.5, linestyle="--")
    ax.set_xlabel("Days from cutoff")
    ax.set_ylabel("Unique listings per day")
    ax.set_title("Density Test: Listings Around Cutoff")
    fig.savefig(FIG_DIR / "density_test.pdf")
    fig.savefig(FIG_DIR / "density_test.png")
    plt.close()

    return {
        "test": "density",
        "coef_bc": round(coef, 4) if not np.isnan(coef) else None,
        "se_robust": round(se, 4) if not np.isnan(se) else None,
        "pval": round(pval, 4) if not np.isnan(pval) else None,
        "status": status,
        "interpretation": "Fail to reject null of no manipulation" if pval > 0.05 else "Potential bunching detected",
    }


# ── 2. Covariate balance ────────────────────────────────────────────────

def covariate_balance(df: pd.DataFrame) -> list[dict]:
    """Test for discontinuities in pre-determined covariates at cutoff.

    Uses OLS local-linear within ±60d bandwidth for speed.
    """
    covariates = [
        ("accommodates", "Accommodates"),
        ("bedrooms", "Bedrooms"),
        ("bathrooms", "Bathrooms"),
        ("number_of_reviews", "Number of reviews"),
        ("review_scores_rating", "Review score"),
        ("host_is_superhost", "Superhost"),
        ("instant_bookable", "Instant bookable"),
        ("calculated_host_listings_count", "Host listing count"),
    ]

    bw = 60
    sub = df[(df["days_from_cutoff"] >= -bw) & (df["days_from_cutoff"] <= bw)].copy()
    x = sub["days_from_cutoff"].values.astype(float)
    post = (x >= 0).astype(float)
    X_base = np.column_stack([np.ones(len(x)), post, x, x * post])

    results = []
    for col, label in covariates:
        valid = sub[col].notna()
        if valid.sum() < 1000:
            results.append({"covariate": label, "status": "insufficient_data"})
            continue

        y = sub.loc[valid, col].values.astype(float)
        X_v = X_base[valid.values]
        clusters = sub.loc[valid, "listing_city"].values

        model = sm.OLS(y, X_v).fit(
            cov_type="cluster",
            cov_kwds={"groups": clusters},
        )
        r = {
            "covariate": label,
            "coef": round(float(model.params[1]), 4),
            "se_cluster": round(float(model.bse[1]), 4),
            "pval": round(float(model.pvalues[1]), 4),
            "status": "ok",
        }
        sig = "*" if r["pval"] < 0.10 else ""
        print(f"  {label}: τ={r['coef']:.4f}{sig}, p={r['pval']:.3f}")
        results.append(r)

    return results


# ── 3. Placebo outcomes ──────────────────────────────────────────────────

def placebo_outcomes(df: pd.DataFrame) -> list[dict]:
    """Test for discontinuities in outcomes that should NOT be affected.

    Uses OLS local-linear within ±60d bandwidth.
    """
    placebos = [
        ("minimum_nights", "Minimum nights"),
        ("available", "Calendar availability"),
    ]

    bw = 60
    sub = df[(df["days_from_cutoff"] >= -bw) & (df["days_from_cutoff"] <= bw)].copy()
    x = sub["days_from_cutoff"].values.astype(float)
    post = (x >= 0).astype(float)
    X_base = np.column_stack([np.ones(len(x)), post, x, x * post])

    results = []
    for col, label in placebos:
        valid = sub[col].notna()
        if valid.sum() < 1000:
            results.append({"outcome": label, "status": "insufficient_data"})
            continue

        y = sub.loc[valid, col].values.astype(float)
        X_v = X_base[valid.values]
        clusters = sub.loc[valid, "listing_city"].values

        model = sm.OLS(y, X_v).fit(
            cov_type="cluster",
            cov_kwds={"groups": clusters},
        )
        r = {
            "outcome": label,
            "coef": round(float(model.params[1]), 4),
            "se_cluster": round(float(model.bse[1]), 4),
            "pval": round(float(model.pvalues[1]), 4),
            "status": "ok",
        }
        sig = "*" if r["pval"] < 0.10 else ""
        print(f"  {label}: τ={r['coef']:.4f}{sig}, p={r['pval']:.3f}")
        results.append(r)

    return results


# ── 4. Leave-one-city-out ────────────────────────────────────────────────

def leave_one_city_out(df: pd.DataFrame) -> list[dict]:
    """Re-estimate dropping each city in turn. OLS ±60d."""
    cities = sorted(df["city_slug"].unique())
    bw = 60
    results = []

    for drop_city in cities:
        sub = df[(df["city_slug"] != drop_city) &
                 (df["days_from_cutoff_resid"] >= -bw) &
                 (df["days_from_cutoff_resid"] <= bw)].copy()

        y = sub["log_price_resid"].values
        x = sub["days_from_cutoff_resid"].values.astype(float)
        post = (x >= 0).astype(float)
        X = np.column_stack([np.ones(len(y)), post, x, x * post])

        model = sm.OLS(y, X).fit(
            cov_type="cluster",
            cov_kwds={"groups": sub["listing_city"].values},
        )

        r = {
            "dropped_city": drop_city,
            "coef": round(float(model.params[1]), 6),
            "se_cluster": round(float(model.bse[1]), 6),
            "pval": round(float(model.pvalues[1]), 4),
            "n": int(len(sub)),
            "status": "ok",
        }
        print(f"  Drop {drop_city}: τ={r['coef']:.4f}, p={r['pval']:.3f}, N={r['n']:,}")
        results.append(r)

    return results


# ── 5. Power analysis / MDE ──────────────────────────────────────────────

def power_analysis(df: pd.DataFrame, primary_se: float) -> dict:
    """Compute minimum detectable effect at 80% and 95% power.

    MDE = (z_alpha/2 + z_beta) * SE
    """
    z_alpha = 1.96  # 5% two-sided
    z_80 = 0.842    # 80% power
    z_95 = 1.645    # 95% power

    mde_80 = (z_alpha + z_80) * primary_se
    mde_95 = (z_alpha + z_95) * primary_se

    # Convert to percentage price effect
    mde_80_pct = (np.exp(mde_80) - 1) * 100
    mde_95_pct = (np.exp(mde_95) - 1) * 100

    print(f"  Primary SE: {primary_se:.6f}")
    print(f"  MDE at 80% power: {mde_80:.4f} log points ({mde_80_pct:.2f}%)")
    print(f"  MDE at 95% power: {mde_95:.4f} log points ({mde_95_pct:.2f}%)")

    # Power curve
    effects = np.linspace(0, 0.10, 200)
    power_vals = []
    for e in effects:
        z = e / primary_se - z_alpha
        power_vals.append(stats.norm.cdf(z))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(effects * 100, power_vals, color="#2166ac", linewidth=2)
    ax.axhline(0.80, color="gray", linewidth=0.8, linestyle="--", label="80% power")
    ax.axhline(0.95, color="gray", linewidth=0.8, linestyle=":", label="95% power")
    ax.axvline(mde_80_pct, color="#b2182b", linewidth=1, linestyle="--", alpha=0.7)
    ax.axvline(mde_95_pct, color="#b2182b", linewidth=1, linestyle=":", alpha=0.7)
    ax.set_xlabel("True effect size (% price change)")
    ax.set_ylabel("Power")
    ax.set_title("Power Curve: Minimum Detectable Effect")
    ax.legend(fontsize=9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.02)
    fig.savefig(FIG_DIR / "mde_power.pdf")
    fig.savefig(FIG_DIR / "mde_power.png")
    plt.close()

    return {
        "se": round(primary_se, 6),
        "mde_80_logpts": round(mde_80, 6),
        "mde_80_pct": round(mde_80_pct, 2),
        "mde_95_logpts": round(mde_95, 6),
        "mde_95_pct": round(mde_95_pct, 2),
    }


def main():
    print("[1/6] Loading residualized panel...")
    df = pd.read_parquet(DATA_DIR / "analysis_panel_residualized.parquet")
    print(f"  {len(df):,} rows")

    # Use residualized panel for covariate balance too (it has all raw cols)
    raw_panel = df  # already ±3m window

    all_results = {}

    print("\n[2/6] Density test...")
    all_results["density"] = density_test(raw_panel)

    print("\n[3/6] Covariate balance...")
    all_results["covariate_balance"] = covariate_balance(raw_panel)

    print("\n[4/6] Placebo outcomes...")
    all_results["placebo_outcomes"] = placebo_outcomes(raw_panel)

    print("\n[5/6] Leave-one-city-out...")
    all_results["leave_one_out"] = leave_one_city_out(df)

    print("\n[6/6] Power analysis...")
    # Load primary SE from ITT results
    itt_path = DATA_DIR / "itt_rdd_results.json"
    if itt_path.exists():
        itt = json.loads(itt_path.read_text())
        # Find the residualized ±60d estimate (our primary spec)
        resid_60 = [r for r in itt["pooled"] if "Residualized" in r.get("label", "") and "60" in r.get("label", "")]
        if resid_60 and resid_60[0]["status"] == "ok":
            primary_se = resid_60[0]["se_cluster"]
        else:
            ok = [r for r in itt["pooled"] if r["status"] == "ok"]
            primary_se = ok[0].get("se_cluster", ok[0].get("se_robust", 0.01)) if ok else 0.01
    else:
        print("  Warning: ITT results not found, using placeholder SE=0.01")
        primary_se = 0.01

    all_results["power"] = power_analysis(df, primary_se)

    # Save all results
    print("\nSaving outputs...")

    # Covariate balance markdown table
    cov_lines = [
        "### Covariate Balance at Cutoff",
        "",
        "| Covariate | τ_BC | SE_rob | p-val |",
        "|---|---:|---:|---:|",
    ]
    for r in all_results["covariate_balance"]:
        if r.get("status") == "ok":
            cov_lines.append(f"| {r['covariate']} | {r['coef']:.4f} | {r['se_cluster']:.4f} | {r['pval']:.3f} |")
        else:
            cov_lines.append(f"| {r['covariate']} | — | — | — |")
    (TABLE_DIR / "covariate_balance.md").write_text("\n".join(cov_lines))

    # Leave-one-out table
    loo_lines = [
        "### Leave-One-City-Out Robustness",
        "",
        "| Dropped City | τ_BC | SE_rob | p-val | N_eff |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in all_results["leave_one_out"]:
        if r.get("status") == "ok":
            loo_lines.append(f"| {r['dropped_city']} | {r['coef']:.4f} | {r['se_cluster']:.6f} | {r['pval']:.3f} | {r['n']:,} |")
    (TABLE_DIR / "leave_one_out.md").write_text("\n".join(loo_lines))

    # JSON
    (DATA_DIR / "falsification_results.json").write_text(
        json.dumps(all_results, indent=2, default=str)
    )

    print("Done.")
    print(f"  Tables → {TABLE_DIR}/{{covariate_balance,leave_one_out}}.md")
    print(f"  Figures → {FIG_DIR}/{{density_test,mde_power}}.{{pdf,png}}")


if __name__ == "__main__":
    main()
