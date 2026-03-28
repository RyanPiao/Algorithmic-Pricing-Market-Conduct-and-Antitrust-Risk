#!/usr/bin/env python3
"""Session 3, Script 04: Variance / dispersion analysis.

Tests whether the pricing tool rollout increased within-listing temporal
price variance — the promoted co-equal core finding.

Under Hazledine (2006), optimal discriminatory prices have the same
weighted average as the optimal uniform price but HIGHER variance.
An algorithm enabling finer time segmentation increases variance
without changing the mean.

Approach:
  1. Compute within-listing rolling price variance (7-day and 14-day)
  2. RDD on variance outcome
  3. Decompose into systematic vs residual variance
  4. Pre/post comparison by city

Output:
  - output/tables/variance_rdd.tex + .md
  - output/figures/variance_pre_post.pdf + .png
  - data/processed/variance_results.json
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rdrobust import rdrobust

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "processed"
TABLE_DIR = REPO / "output" / "tables"
FIG_DIR = REPO / "output" / "figures"
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42

# ── AER-style plot defaults ──────────────────────────────────────────────

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def compute_listing_variance(df: pd.DataFrame) -> pd.DataFrame:
    """Compute within-listing rolling price variance.

    Uses vectorized rolling on sorted data for speed.
    """
    df = df.sort_values(["listing_city", "date"]).reset_index(drop=True)

    # Use pandas built-in groupby rolling (much faster than transform+lambda)
    grp = df.groupby("listing_city")["log_price"]

    print("    Computing 7-day rolling variance...")
    df["log_price_var_7d"] = grp.rolling(7, min_periods=4).var().reset_index(level=0, drop=True)

    print("    Computing 14-day rolling variance...")
    df["log_price_var_14d"] = grp.rolling(14, min_periods=7).var().reset_index(level=0, drop=True)

    return df


def compute_listing_period_variance(df: pd.DataFrame) -> pd.DataFrame:
    """Compute listing-level pre/post variance for the collapsed analysis."""
    results = []
    for (listing, post), g in df.groupby(["listing_city", "post_cutoff"]):
        if len(g) < 7:  # Need minimum observations
            continue
        results.append({
            "listing_city": listing,
            "city_slug": g["city_slug"].iloc[0],
            "post_cutoff": post,
            "log_price_var": g["log_price"].var(),
            "log_price_std": g["log_price"].std(),
            "log_price_mean": g["log_price"].mean(),
            "price_range": g["price_usd"].max() - g["price_usd"].min(),
            "n_price_changes": (g["price_usd"].diff().abs() > 0).sum(),
            "n_days": len(g),
        })
    return pd.DataFrame(results)


def run_variance_rdd(df: pd.DataFrame, var_col: str, label: str) -> dict:
    """Run OLS local-linear RDD on a variance outcome (±60d bandwidth)."""
    valid = df[var_col].notna()
    sub = df.loc[valid].copy()
    bw = 60
    sub = sub[(sub["days_from_cutoff"] >= -bw) & (sub["days_from_cutoff"] <= bw)]

    if len(sub) < 100:
        return {"label": label, "status": "insufficient_data"}

    y = sub[var_col].values
    x = sub["days_from_cutoff"].values.astype(float)
    post = (x >= 0).astype(float)

    X = np.column_stack([np.ones(len(y)), post, x, x * post])

    import statsmodels.api as sm
    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": sub["listing_city"].values},
    )

    tau = model.params[1]
    se = model.bse[1]
    ci = model.conf_int()[1]

    return {
        "label": label,
        "coef": round(float(tau), 6),
        "se_cluster": round(float(se), 6),
        "ci_lower": round(float(ci[0]), 6),
        "ci_upper": round(float(ci[1]), 6),
        "pval": round(float(model.pvalues[1]), 6),
        "bw": bw,
        "n_obs": int(len(sub)),
        "status": "ok",
    }


def plot_variance_pre_post(listing_var: pd.DataFrame):
    """Plot pre vs post listing-level variance by city."""
    fig, axes = plt.subplots(2, 4, figsize=(14, 7), sharey=True)
    cities = sorted(listing_var["city_slug"].unique())

    for ax, city in zip(axes.flat, cities):
        city_data = listing_var[listing_var["city_slug"] == city]
        pre = city_data[city_data["post_cutoff"] == 0]["log_price_var"]
        post = city_data[city_data["post_cutoff"] == 1]["log_price_var"]

        ax.hist(pre, bins=50, alpha=0.6, label="Pre", color="#2166ac", density=True)
        ax.hist(post, bins=50, alpha=0.6, label="Post", color="#b2182b", density=True)
        ax.set_title(city.replace("-", " ").title(), fontsize=9)
        ax.set_xlim(0, 0.5)
        if ax in axes[:, 0]:
            ax.set_ylabel("Density")

    axes.flat[0].legend(fontsize=8)
    fig.suptitle("Within-Listing Log Price Variance: Pre vs Post Rollout", fontsize=12)
    fig.supxlabel("Var(log price)")
    plt.tight_layout()

    fig.savefig(FIG_DIR / "variance_pre_post.pdf")
    fig.savefig(FIG_DIR / "variance_pre_post.png")
    plt.close()
    print(f"  Figure → {FIG_DIR}/variance_pre_post.{{pdf,png}}")


def main():
    print("[1/5] Loading panel...")
    panel_path = DATA_DIR / "analysis_panel_residualized.parquet"
    df = pd.read_parquet(panel_path)
    print(f"  {len(df):,} rows")

    print("[2/5] Computing within-listing rolling variance...")
    df = compute_listing_variance(df)

    print("[3/5] RDD on variance outcomes...")
    var_results = []

    for var_col, label in [
        ("log_price_var_7d", "7-day rolling Var(log price)"),
        ("log_price_var_14d", "14-day rolling Var(log price)"),
    ]:
        print(f"  {label}...")
        r = run_variance_rdd(df, var_col, label)
        var_results.append(r)
        if r["status"] == "ok":
            stars = "***" if r["pval"] < 0.01 else "**" if r["pval"] < 0.05 else "*" if r["pval"] < 0.10 else ""
            print(f"    τ={r['coef']:.6f}{stars}, SE={r['se_cluster']:.6f}, p={r['pval']:.4f}")

    print("[4/5] Listing-level pre/post variance comparison...")
    listing_var = compute_listing_period_variance(df)
    print(f"  {len(listing_var):,} listing-period observations")

    # Summary stats
    for post in [0, 1]:
        sub = listing_var[listing_var["post_cutoff"] == post]
        period = "Post" if post else "Pre"
        print(f"  {period}: mean Var(log price)={sub['log_price_var'].mean():.6f}, "
              f"median={sub['log_price_var'].median():.6f}, "
              f"mean price changes/period={sub['n_price_changes'].mean():.1f}")

    # City-level pre/post means
    city_summary = []
    for city in sorted(listing_var["city_slug"].unique()):
        city_data = listing_var[listing_var["city_slug"] == city]
        pre_var = city_data.loc[city_data["post_cutoff"] == 0, "log_price_var"].mean()
        post_var = city_data.loc[city_data["post_cutoff"] == 1, "log_price_var"].mean()
        change = post_var - pre_var
        pct_change = (change / pre_var * 100) if pre_var > 0 else np.nan
        city_summary.append({
            "city": city,
            "pre_var": round(pre_var, 6),
            "post_var": round(post_var, 6),
            "change": round(change, 6),
            "pct_change": round(pct_change, 2),
        })
        print(f"  {city}: pre={pre_var:.6f}, post={post_var:.6f}, Δ={change:+.6f} ({pct_change:+.1f}%)")

    print("[5/5] Saving outputs...")

    # Plot
    plot_variance_pre_post(listing_var)

    # Tables — OLS estimates (correctly labeled)
    lines_md = [
        "### Variance RDD Estimates (OLS, ±60d, listing-clustered SEs)",
        "",
        "| Outcome | τ_OLS | SE_cluster | 95% CI | p-val | N |",
        "|---|---:|---:|---|---:|---:|",
    ]
    for r in var_results:
        if r["status"] == "ok":
            ci = f"[{r['ci_lower']:.6f}, {r['ci_upper']:.6f}]"
            lines_md.append(f"| {r['label']} | {r['coef']:.6f} | {r['se_cluster']:.6f} | {ci} | {r['pval']:.4f} | {r['n_obs']:,} |")
    (TABLE_DIR / "variance_rdd.md").write_text("\n".join(lines_md))

    # rdrobust estimates on daily-collapsed variance means
    print("  rdrobust on daily variance means...")
    from rdrobust import rdrobust
    rdr_lines = [
        "### Variance RDD Estimates (rdrobust, CCT bandwidth)",
        "",
        "| Outcome | τ_BC | SE_rob | 95% CI | p-val | BW |",
        "|---|---:|---:|---|---:|---:|",
    ]
    for var_col, label in [
        ("log_price_var_7d", "7-day rolling Var(log price)"),
        ("log_price_var_14d", "14-day rolling Var(log price)"),
    ]:
        valid = df[var_col].notna() & df["days_from_cutoff"].notna()
        sub = df.loc[valid]
        # Collapse to daily means for rdrobust
        daily = sub.groupby("days_from_cutoff").agg(
            y_mean=(var_col, "mean"),
        ).reset_index()
        daily = daily.dropna()
        try:
            y_arr = daily["y_mean"].to_numpy(dtype=np.float64)
            x_arr = daily["days_from_cutoff"].to_numpy(dtype=np.float64)
            # Remove any remaining NaN
            mask = ~(np.isnan(y_arr) | np.isnan(x_arr))
            rdr = rdrobust(y_arr[mask], x_arr[mask])
            tau_bc = float(rdr.coef.iloc[1])  # bias-corrected
            se_rob = float(rdr.se.iloc[2])    # robust SE
            ci_l = float(rdr.ci.iloc[2, 0])
            ci_r = float(rdr.ci.iloc[2, 1])
            pval = float(rdr.pv.iloc[2])
            bw_l = float(rdr.bws.iloc[0, 0])
            ci_str = f"[{ci_l:.6f}, {ci_r:.6f}]"
            stars = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.10 else ""
            rdr_lines.append(f"| {label} | {tau_bc:.6f} | {se_rob:.6f} | {ci_str} | {pval:.4f} | {bw_l:.0f} |")
            print(f"    {label}: τ_BC={tau_bc:.6f}{stars}, SE_rob={se_rob:.6f}, BW={bw_l:.0f}d")
        except Exception as e:
            rdr_lines.append(f"| {label} | — | — | — | — | — |")
            print(f"    {label}: rdrobust failed: {e}")
    (TABLE_DIR / "variance_rdd_rdrobust.md").write_text("\n".join(rdr_lines))

    # City summary table
    city_md = [
        "### Within-Listing Variance: Pre vs Post by City",
        "",
        "| City | Pre Var | Post Var | Change | % Change |",
        "|---|---:|---:|---:|---:|",
    ]
    for cs in city_summary:
        city_md.append(f"| {cs['city']} | {cs['pre_var']:.6f} | {cs['post_var']:.6f} | {cs['change']:+.6f} | {cs['pct_change']:+.1f}% |")
    (TABLE_DIR / "variance_city_prepost.md").write_text("\n".join(city_md))

    # JSON
    all_results = {
        "rdd_estimates": var_results,
        "city_prepost": city_summary,
        "listing_period_obs": len(listing_var),
    }
    (DATA_DIR / "variance_results.json").write_text(json.dumps(all_results, indent=2))

    print("Done.")


if __name__ == "__main__":
    main()
