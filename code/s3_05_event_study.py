#!/usr/bin/env python3
"""Session 3, Script 05: Event-study plot.

Plots bi-weekly coefficients around the Sep 1 2023 cutoff.
Shows flat pre-trends and any post-rollout shift.
Includes vertical line for May 3 beta launch.

Primary graphical evidence (Figure 1).

Output:
  - output/figures/event_study_price.pdf + .png
  - output/figures/event_study_variance.pdf + .png
  - output/tables/event_study_coefs.md
  - data/processed/event_study_results.json
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

CUTOFF = pd.Timestamp("2023-09-01")
BETA = pd.Timestamp("2023-05-03")
SEED = 42

# AER style
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# Bi-weekly bins: 14-day intervals from -180 to +120 days around cutoff
# Reference period: [-14, 0) — the last two weeks before cutoff
BIN_WIDTH = 14
BIN_START = -168  # ~6 months pre
BIN_END = 126     # ~4 months post
REFERENCE_BIN = -1  # bin index for [-14, 0) — normalized to zero


def create_time_bins(df: pd.DataFrame) -> pd.DataFrame:
    """Assign observations to bi-weekly bins around cutoff."""
    days = df["days_from_cutoff"].values

    # Bin edges
    edges = list(range(BIN_START, BIN_END + BIN_WIDTH, BIN_WIDTH))
    bin_labels = []
    for i in range(len(edges) - 1):
        bin_labels.append(edges[i])

    df = df.copy()
    df["time_bin"] = pd.cut(
        days,
        bins=edges,
        labels=bin_labels,
        right=False,
    )
    df["time_bin"] = df["time_bin"].astype(float)
    return df


def estimate_event_study(
    df: pd.DataFrame,
    outcome: str,
    label: str,
) -> tuple[pd.DataFrame, dict]:
    """Estimate event-study regression with bi-weekly dummies.

    Model: Y_it = Σ_k β_k · 1(bin=k) + city_FE + ε_it
    (reference bin = [-14, 0))

    Clustered SEs at listing level.
    """
    df = df.dropna(subset=[outcome, "time_bin"]).copy()

    bins = sorted(df["time_bin"].unique())
    # Find reference bin (closest to REFERENCE_BIN * BIN_WIDTH)
    ref_val = -14.0  # [-14, 0) bin
    if ref_val not in bins:
        ref_val = min(bins, key=lambda b: abs(b - (-14.0)))
    bins_excl_ref = [b for b in bins if b != ref_val]

    print(f"  {len(bins)} bins, reference={ref_val}, outcome={outcome}")

    # Construct dummies
    for b in bins_excl_ref:
        df[f"bin_{int(b)}"] = (df["time_bin"] == b).astype(np.float64)

    bin_cols = [f"bin_{int(b)}" for b in bins_excl_ref]

    # City FE
    city_dummies = pd.get_dummies(df["city_slug"], prefix="city", drop_first=True, dtype=np.float64)

    X = pd.concat([df[bin_cols], city_dummies], axis=1)
    X = sm.add_constant(X)
    y = df[outcome].values

    # OLS with clustered SEs
    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["listing_city"].values},
    )

    # Extract bin coefficients
    coef_data = []
    for b in bins_excl_ref:
        col = f"bin_{int(b)}"
        coef_data.append({
            "bin_start": int(b),
            "bin_mid": int(b) + BIN_WIDTH // 2,
            "coef": float(model.params[col]),
            "se": float(model.bse[col]),
            "ci_lower": float(model.conf_int().loc[col, 0]),
            "ci_upper": float(model.conf_int().loc[col, 1]),
            "pval": float(model.pvalues[col]),
        })

    # Add reference bin (zero by construction)
    coef_data.append({
        "bin_start": int(ref_val),
        "bin_mid": int(ref_val) + BIN_WIDTH // 2,
        "coef": 0.0,
        "se": 0.0,
        "ci_lower": 0.0,
        "ci_upper": 0.0,
        "pval": 1.0,
    })

    coef_df = pd.DataFrame(coef_data).sort_values("bin_start")

    meta = {
        "outcome": outcome,
        "label": label,
        "reference_bin": int(ref_val),
        "n_obs": int(model.nobs),
        "r_squared": round(float(model.rsquared), 4),
        "n_clusters": int(df["listing_city"].nunique()),
    }

    return coef_df, meta


def plot_event_study(
    coef_df: pd.DataFrame,
    meta: dict,
    filename: str,
    ylabel: str,
):
    """Plot event-study coefficients with confidence intervals."""
    fig, ax = plt.subplots(figsize=(10, 5))

    x = coef_df["bin_mid"].values
    y = coef_df["coef"].values
    ci_lo = coef_df["ci_lower"].values
    ci_hi = coef_df["ci_upper"].values

    # CI band
    ax.fill_between(x, ci_lo, ci_hi, alpha=0.2, color="#2166ac")
    # Point estimates
    ax.plot(x, y, "o-", color="#2166ac", markersize=5, linewidth=1.5)
    # Zero line
    ax.axhline(0, color="black", linewidth=0.5, linestyle="-")
    # Cutoff line
    ax.axvline(0, color="#b2182b", linewidth=1.5, linestyle="--", label="Official rollout (Sep 1)")
    # Beta launch line
    beta_days = (BETA - CUTOFF).days
    ax.axvline(beta_days, color="#fdae61", linewidth=1.5, linestyle=":", label="Beta launch (May 3)")

    ax.set_xlabel("Days from cutoff (Sep 1, 2023)")
    ax.set_ylabel(ylabel)
    ax.legend(fontsize=9, loc="upper left")

    # Annotate
    ax.text(0.02, 0.02,
            f"N = {meta['n_obs']:,}  |  Clusters = {meta['n_clusters']:,}  |  R² = {meta['r_squared']:.3f}",
            transform=ax.transAxes, fontsize=8, color="gray")

    plt.tight_layout()
    fig.savefig(FIG_DIR / f"{filename}.pdf")
    fig.savefig(FIG_DIR / f"{filename}.png")
    plt.close()
    print(f"  → {FIG_DIR}/{filename}.{{pdf,png}}")


def main():
    print("[1/4] Loading residualized panel...")
    df = pd.read_parquet(DATA_DIR / "analysis_panel_residualized.parquet")
    print(f"  {len(df):,} rows")

    print("[2/4] Creating time bins...")
    df = create_time_bins(df)
    print(f"  Observations with valid bins: {df['time_bin'].notna().sum():,}")

    # Compute rolling variance for variance event study
    df = df.sort_values(["listing_city", "date"])
    df["log_price_var_7d"] = (
        df.groupby("listing_city")["log_price"]
        .transform(lambda x: x.rolling(7, min_periods=4).var())
    )

    print("[3/4] Estimating event-study regressions...")

    # Price level event study (residualized)
    print("\n  --- Price Level ---")
    price_coefs, price_meta = estimate_event_study(
        df, "log_price_resid", "Log Price (Residualized)"
    )
    print(f"  Pre-trend F-test: checking if pre-cutoff coefficients are jointly zero...")
    pre_coefs = price_coefs[price_coefs["bin_start"] < -14]
    pre_significant = (pre_coefs["pval"] < 0.05).sum()
    print(f"  {pre_significant}/{len(pre_coefs)} pre-bins significant at 5%")

    # Variance event study
    print("\n  --- Price Variance ---")
    var_coefs, var_meta = estimate_event_study(
        df, "log_price_var_7d", "7-day Rolling Var(log price)"
    )

    print("\n[4/4] Plotting and saving...")

    plot_event_study(
        price_coefs, price_meta,
        "event_study_price",
        "Coefficient on bi-weekly dummy\n(log price, residualized)"
    )

    plot_event_study(
        var_coefs, var_meta,
        "event_study_variance",
        "Coefficient on bi-weekly dummy\n(7-day rolling variance)"
    )

    # Save coefficients table
    lines = ["### Event-Study Coefficients: Log Price (Residualized)", ""]
    lines.append("| Bin (days) | Coef | SE | 95% CI | p-val |")
    lines.append("|---:|---:|---:|---|---:|")
    for _, row in price_coefs.iterrows():
        ci = f"[{row['ci_lower']:.4f}, {row['ci_upper']:.4f}]"
        marker = " (ref)" if row["se"] == 0 else ""
        lines.append(f"| [{int(row['bin_start'])}, {int(row['bin_start'])+BIN_WIDTH}){marker} "
                     f"| {row['coef']:.4f} | {row['se']:.4f} | {ci} | {row['pval']:.3f} |")
    (TABLE_DIR / "event_study_coefs.md").write_text("\n".join(lines))

    # JSON
    results = {
        "price": {
            "meta": price_meta,
            "coefs": price_coefs.to_dict(orient="records"),
        },
        "variance": {
            "meta": var_meta,
            "coefs": var_coefs.to_dict(orient="records"),
        },
    }
    (DATA_DIR / "event_study_results.json").write_text(json.dumps(results, indent=2, default=str))

    print("\nDone.")


if __name__ == "__main__":
    main()
