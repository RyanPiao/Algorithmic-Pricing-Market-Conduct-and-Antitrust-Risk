#!/usr/bin/env python3
"""Session 3, Script 14: Wild cluster bootstrap for city-level inference.

Referees' concern: the paper clusters SEs at the listing level, but there
are only 8 cities. With few clusters, standard cluster-robust SEs can be
severely downward-biased (Cameron, Gelbach & Miller 2008). The wild cluster
bootstrap provides valid inference with a small number of clusters.

Procedure (Cameron, Gelbach & Miller 2008; Roodman et al. 2019):
  1. Estimate the main specification under H₀: τ = 0 (restricted model).
  2. Compute residuals from the restricted model.
  3. For each of B = 999 bootstrap iterations:
     a. Draw Rademacher weights w_g ∈ {-1, +1} for each of G = 8 cities.
     b. Construct bootstrap outcome: y*_i = ŷ_i(restricted) + w_{g(i)} · ê_i
     c. Re-estimate the full (unrestricted) model on y* to get τ*.
     d. Compute the bootstrap t-statistic: t* = τ* / SE*(τ*).
  4. Bootstrap p-value = fraction of |t*| ≥ |t_original|.

Main specification (from s3_03_itt_rdd.py):
  log_price_resid = α + τ·1(date ≥ cutoff) + β₁·x + β₂·x·1(x≥0) + ε
  within ±60d bandwidth, listing-level clustered SEs.

Output: output/tables/wild_bootstrap.md

Usage:
  python code/s3_14_wild_bootstrap.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

# ── Config ───────────────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "processed"
TABLE_DIR = REPO / "output" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
B_ITERATIONS = 999   # Bootstrap replications
BW = 60              # Main specification bandwidth (days)

# ── OLS helpers ──────────────────────────────────────────────────────────────


def build_rdd_design(df: pd.DataFrame, x_col: str) -> np.ndarray:
    """Build the local linear RDD design matrix.

    Returns X = [1, post, x, x*post] — same as s3_03_itt_rdd.py.
    """
    x = df[x_col].values.astype(np.float64)
    post = (x >= 0).astype(np.float64)
    return np.column_stack([
        np.ones(len(x)),
        post,
        x,
        x * post,
    ])


def ols_with_cluster_se(
    y: np.ndarray,
    X: np.ndarray,
    cluster_ids: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """OLS with cluster-robust SEs. Returns (coefs, SEs, t-stats)."""
    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": cluster_ids},
    )
    return model.params, model.bse, model.tvalues, model.pvalues


def format_stars(pval: float) -> str:
    if pval < 0.01:
        return "***"
    elif pval < 0.05:
        return "**"
    elif pval < 0.10:
        return "*"
    return ""


# ── Wild cluster bootstrap ───────────────────────────────────────────────────


def wild_cluster_bootstrap(
    df: pd.DataFrame,
    y_col: str,
    x_col: str,
    cluster_col: str,
    city_col: str,
    bw: int,
    n_boot: int,
    seed: int,
) -> dict:
    """Wild cluster bootstrap at the city level with Rademacher weights.

    Parameters
    ----------
    df : DataFrame
        Analysis panel.
    y_col : str
        Outcome column (e.g. "log_price_resid").
    x_col : str
        Running variable column (e.g. "days_from_cutoff").
    cluster_col : str
        Listing-level cluster column (for original SE comparison).
    city_col : str
        City-level cluster column (the wild bootstrap cluster level).
    bw : int
        Bandwidth in days (symmetric around cutoff).
    n_boot : int
        Number of bootstrap iterations.
    seed : int
        Random seed.

    Returns
    -------
    dict with original estimates and bootstrap p-values.
    """
    rng = np.random.RandomState(seed)

    # ── Filter to bandwidth window ───────────────────────────────────────
    sub = df[(df[x_col] >= -bw) & (df[x_col] <= bw)].copy()
    n_obs = len(sub)
    print(f"  Observations in ±{bw}d window: {n_obs:,}")

    # Design matrix
    X_full = build_rdd_design(sub, x_col)
    y = sub[y_col].values.astype(np.float64)

    # City assignments for each observation
    cities = sub[city_col].values
    unique_cities = np.unique(cities)
    n_cities = len(unique_cities)
    print(f"  Number of city-level clusters: {n_cities}")

    # Create city index for fast lookup
    city_to_idx = {c: i for i, c in enumerate(unique_cities)}
    city_idx = np.array([city_to_idx[c] for c in cities])

    # ── Step 1: Original (unrestricted) model ────────────────────────────
    # Full model: Y = α + τ·post + β₁·x + β₂·x·post + ε
    params_full, se_listing, t_listing, pval_listing = ols_with_cluster_se(
        y, X_full, sub[cluster_col].values
    )
    tau_orig = params_full[1]
    se_orig_listing = se_listing[1]
    t_orig_listing = t_listing[1]
    p_orig_listing = pval_listing[1]

    # Also get city-clustered SE for comparison
    _, se_city, t_city, pval_city = ols_with_cluster_se(
        y, X_full, cities
    )
    t_orig_city = t_city[1]
    p_orig_city = pval_city[1]

    print(f"\n  Original estimate:")
    print(f"    τ = {tau_orig:.6f}")
    print(f"    Listing-clustered: SE={se_listing[1]:.6f}, t={t_orig_listing:.3f}, p={p_orig_listing:.4f}")
    print(f"    City-clustered:    SE={se_city[1]:.6f}, t={t_orig_city:.3f}, p={p_orig_city:.4f}")

    # ── Step 2: Restricted model (impose H₀: τ = 0) ─────────────────────
    # Remove the post column (col 1) from the design matrix
    X_restricted = X_full[:, [0, 2, 3]]  # [intercept, x, x*post]
    model_r = sm.OLS(y, X_restricted).fit()
    y_hat_restricted = model_r.fittedvalues
    residuals_restricted = model_r.resid

    # ── Step 3: Bootstrap loop ───────────────────────────────────────────
    print(f"\n  Running {n_boot} wild cluster bootstrap iterations...")
    t0 = time.time()

    boot_t_stats = np.empty(n_boot)

    for b in range(n_boot):
        # (a) Draw Rademacher weights: one per city
        rademacher = rng.choice([-1.0, 1.0], size=n_cities)

        # (b) Assign city-level weight to each observation
        weights = rademacher[city_idx]

        # (c) Construct bootstrap outcome
        y_boot = y_hat_restricted + weights * residuals_restricted

        # (d) Re-estimate full model with city-clustered SEs
        model_boot = sm.OLS(y_boot, X_full).fit(
            cov_type="cluster",
            cov_kwds={"groups": cities},
        )
        boot_t_stats[b] = model_boot.tvalues[1]

        if (b + 1) % 200 == 0:
            elapsed = time.time() - t0
            rate = (b + 1) / elapsed
            remaining = (n_boot - b - 1) / rate
            print(f"    Iteration {b+1}/{n_boot} "
                  f"({elapsed:.0f}s elapsed, ~{remaining:.0f}s remaining)")

    elapsed_total = time.time() - t0
    print(f"  Bootstrap complete in {elapsed_total:.1f}s")

    # ── Step 4: Compute bootstrap p-value ────────────────────────────────
    # Two-sided: p = fraction of |t*| >= |t_original|
    # Use the city-clustered t-stat as the reference (consistent with
    # bootstrapping at the city level)
    boot_p_value = np.mean(np.abs(boot_t_stats) >= np.abs(t_orig_city))

    print(f"\n  Bootstrap results:")
    print(f"    Original city-clustered t-stat:  {t_orig_city:.4f}")
    print(f"    Bootstrap t-stat distribution:   "
          f"mean={boot_t_stats.mean():.4f}, std={boot_t_stats.std():.4f}")
    print(f"    Bootstrap p-value (two-sided):   {boot_p_value:.4f}")
    print(f"    Listing-clustered p-value:       {p_orig_listing:.4f}")
    print(f"    City-clustered (analytical) p:   {p_orig_city:.4f}")

    return {
        "tau": round(float(tau_orig), 6),
        "se_listing_cluster": round(float(se_orig_listing), 6),
        "t_listing_cluster": round(float(t_orig_listing), 4),
        "p_listing_cluster": round(float(p_orig_listing), 4),
        "se_city_cluster": round(float(se_city[1]), 6),
        "t_city_cluster": round(float(t_orig_city), 4),
        "p_city_cluster": round(float(p_orig_city), 4),
        "p_wild_bootstrap": round(float(boot_p_value), 4),
        "n_boot": n_boot,
        "n_cities": n_cities,
        "n_obs": n_obs,
        "n_listings": int(sub[cluster_col].nunique()),
        "bw": bw,
        "boot_t_mean": round(float(boot_t_stats.mean()), 4),
        "boot_t_std": round(float(boot_t_stats.std()), 4),
        "boot_t_p05": round(float(np.percentile(boot_t_stats, 5)), 4),
        "boot_t_p95": round(float(np.percentile(boot_t_stats, 95)), 4),
        "seed": seed,
    }


# ── Output formatting ────────────────────────────────────────────────────────


def results_to_markdown(results: dict) -> str:
    """Format wild bootstrap results as a markdown table."""
    tau = results["tau"]
    lines = [
        "### Wild Cluster Bootstrap: City-Level Inference",
        "",
        "Main specification: `log_price_resid = α + τ·post + β₁·x + β₂·x·post + ε`",
        f"within ±{results['bw']}d bandwidth.",
        "",
        f"**Point estimate:** τ = {tau:.4f} ({tau*100:.2f}% effect on prices)",
        "",
        "| Inference Method | SE | t-stat | p-value | Clusters |",
        "|---|---:|---:|---:|---:|",
    ]

    # Listing-clustered
    stars_l = format_stars(results["p_listing_cluster"])
    lines.append(
        f"| Listing-clustered (analytical) | {results['se_listing_cluster']:.4f} | "
        f"{results['t_listing_cluster']:.3f} | {results['p_listing_cluster']:.4f}{stars_l} | "
        f"{results['n_listings']:,} |"
    )

    # City-clustered (analytical)
    stars_c = format_stars(results["p_city_cluster"])
    lines.append(
        f"| City-clustered (analytical) | {results['se_city_cluster']:.4f} | "
        f"{results['t_city_cluster']:.3f} | {results['p_city_cluster']:.4f}{stars_c} | "
        f"{results['n_cities']} |"
    )

    # Wild cluster bootstrap
    stars_b = format_stars(results["p_wild_bootstrap"])
    lines.append(
        f"| Wild cluster bootstrap (city) | — | — | {results['p_wild_bootstrap']:.4f}{stars_b} | "
        f"{results['n_cities']} |"
    )

    lines += [
        "",
        f"N = {results['n_obs']:,} listing-day observations.",
        f"Wild cluster bootstrap: {results['n_boot']} iterations, Rademacher weights,",
        f"seed = {results['seed']}.",
        "",
        "Bootstrap t-statistic distribution:",
        f"  - Mean: {results['boot_t_mean']:.4f}",
        f"  - Std:  {results['boot_t_std']:.4f}",
        f"  - 5th percentile: {results['boot_t_p05']:.4f}",
        f"  - 95th percentile: {results['boot_t_p95']:.4f}",
        "",
        "Reference: Cameron, Gelbach & Miller (2008), 'Bootstrap-Based",
        "Improvements for Inference with Clustered Errors', REStat.",
    ]

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    print("[1/3] Loading residualized panel...")
    df = pd.read_parquet(DATA_DIR / "analysis_panel_residualized.parquet")
    print(f"  {len(df):,} rows, {df['listing_city'].nunique():,} listings, "
          f"{df['city_slug'].nunique()} cities")

    print(f"\n[2/3] Wild cluster bootstrap (±{BW}d, residualized outcome)...")
    results = wild_cluster_bootstrap(
        df=df,
        y_col="log_price_resid",
        x_col="days_from_cutoff",
        cluster_col="listing_city",
        city_col="city_slug",
        bw=BW,
        n_boot=B_ITERATIONS,
        seed=SEED,
    )

    print(f"\n[3/3] Saving outputs...")

    # Markdown table
    md = results_to_markdown(results)
    md_path = TABLE_DIR / "wild_bootstrap.md"
    md_path.write_text(md)
    print(f"  Table → {md_path}")

    # JSON results
    json_path = DATA_DIR / "wild_bootstrap_results.json"
    json_path.write_text(json.dumps(results, indent=2))
    print(f"  JSON  → {json_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
