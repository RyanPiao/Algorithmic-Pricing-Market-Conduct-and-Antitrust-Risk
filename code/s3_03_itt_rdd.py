#!/usr/bin/env python3
"""Session 3, Script 03: ITT reduced-form sharp RDD estimation.

Primary specification:
  log_price_resid_it = α + τ·1(date >= cutoff) + f(days_from_cutoff) + ε_it

Two estimation approaches:
  A) OLS local linear with manual bandwidth — fast, handles full data,
     clustered SEs at listing level
  B) rdrobust CCT bandwidth selection on listing-day collapsed data
     (daily means) for proper bias-corrected CIs

Reports pooled + city-specific estimates.

Output:
  - output/tables/itt_rdd_pooled.tex + .md
  - output/tables/itt_rdd_city.tex + .md
  - data/processed/itt_rdd_results.json
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from rdrobust import rdrobust

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "processed"
TABLE_DIR = REPO / "output" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
BANDWIDTHS = [30, 45, 60, 90]  # days


def ols_rdd(
    df: pd.DataFrame,
    y_col: str,
    x_col: str,
    bw: int,
    cluster_col: str,
    label: str,
) -> dict:
    """Local linear OLS RDD within bandwidth, clustered SEs."""
    sub = df[(df[x_col] >= -bw) & (df[x_col] <= bw)].copy()
    if len(sub) < 100:
        return {"label": label, "status": "insufficient_data"}

    y = sub[y_col].values
    post = (sub[x_col] >= 0).astype(float).values
    x = sub[x_col].values.astype(float)

    # Local linear: Y = α + τ·post + β₁·x + β₂·x·post + ε
    X = np.column_stack([
        np.ones(len(y)),
        post,
        x,
        x * post,
    ])

    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": sub[cluster_col].values},
    )

    tau = model.params[1]
    se = model.bse[1]
    ci = model.conf_int()[1]
    pval = model.pvalues[1]

    return {
        "label": label,
        "bw": bw,
        "coef": round(float(tau), 6),
        "se_cluster": round(float(se), 6),
        "ci_lower": round(float(ci[0]), 6),
        "ci_upper": round(float(ci[1]), 6),
        "pval": round(float(pval), 6),
        "n_obs": int(len(sub)),
        "n_clusters": int(sub[cluster_col].nunique()),
        "n_pre": int((post == 0).sum()),
        "n_post": int((post == 1).sum()),
        "r_squared": round(float(model.rsquared), 6),
        "status": "ok",
    }


def rdrobust_on_collapsed(
    df: pd.DataFrame,
    y_col: str,
    x_col: str,
    label: str,
) -> dict:
    """Run rdrobust on daily-collapsed data (manageable size)."""
    # Collapse to daily means
    daily = (
        df.groupby(x_col)
        .agg(
            y_mean=(y_col, "mean"),
            n_listings=("listing_city", "nunique"),
        )
        .reset_index()
    )

    try:
        result = rdrobust(
            y=daily["y_mean"].values,
            x=daily[x_col].values.astype(float),
            p=1,
            bwselect="mserd",
        )

        return {
            "label": label,
            "coef_conv": round(float(result.coef.iloc[0]), 6),
            "coef_bc": round(float(result.coef.iloc[1]), 6),
            "se_conv": round(float(result.se.iloc[0]), 6),
            "se_robust": round(float(result.se.iloc[2]), 6),
            "ci_rb_lower": round(float(result.ci.iloc[2, 0]), 6),
            "ci_rb_upper": round(float(result.ci.iloc[2, 1]), 6),
            "pval_robust": round(float(result.pv.iloc[2]), 6),
            "bw_left": round(float(result.bws.iloc[0, 0]), 2),
            "bw_right": round(float(result.bws.iloc[0, 1]), 2),
            "n_days_left": int(result.N_h[0]),
            "n_days_right": int(result.N_h[1]),
            "status": "ok",
        }
    except Exception as e:
        print(f"  Warning: rdrobust failed for {label}: {e}")
        return {"label": label, "status": "failed", "error": str(e)}


def format_stars(pval: float) -> str:
    if pval < 0.01:
        return "***"
    elif pval < 0.05:
        return "**"
    elif pval < 0.10:
        return "*"
    return ""


def results_to_markdown(results: list[dict], title: str) -> str:
    lines = [f"### {title}", "",
             "| Specification | τ | SE | 95% CI | p-val | BW | N |",
             "|---|---:|---:|---|---:|---:|---:|"]
    for r in results:
        if r["status"] != "ok":
            lines.append(f"| {r['label']} | — | — | — | — | — | — |")
            continue
        stars = format_stars(r.get("pval", r.get("pval_robust", 1.0)))
        coef = r.get("coef", r.get("coef_bc", 0))
        se = r.get("se_cluster", r.get("se_robust", 0))
        pval = r.get("pval", r.get("pval_robust", 1.0))
        ci_lo = r.get("ci_lower", r.get("ci_rb_lower", 0))
        ci_hi = r.get("ci_upper", r.get("ci_rb_upper", 0))
        bw = r.get("bw", f"{r.get('bw_left', '?')}/{r.get('bw_right', '?')}")
        n = r.get("n_obs", r.get("n_days_left", 0) + r.get("n_days_right", 0))
        lines.append(f"| {r['label']} | {coef:.4f}{stars} | {se:.4f} | [{ci_lo:.4f}, {ci_hi:.4f}] | {pval:.3f} | {bw} | {n:,} |")
    return "\n".join(lines)


def results_to_latex(results: list[dict], caption: str, label: str) -> str:
    lines = [
        r"\begin{table}[htbp]", r"\centering",
        f"\\caption{{{caption}}}", f"\\label{{{label}}}",
        r"\begin{tabular}{lcccccc}", r"\hline\hline",
        r" & $\hat{\tau}$ & SE & 95\% CI & $p$ & BW & $N$ \\",
        r"\hline",
    ]
    for r in results:
        if r["status"] != "ok":
            lines.append(f"  {r['label']} & \\multicolumn{{6}}{{c}}{{—}} \\\\")
            continue
        stars = format_stars(r.get("pval", r.get("pval_robust", 1.0)))
        coef = r.get("coef", r.get("coef_bc", 0))
        se = r.get("se_cluster", r.get("se_robust", 0))
        pval = r.get("pval", r.get("pval_robust", 1.0))
        ci_lo = r.get("ci_lower", r.get("ci_rb_lower", 0))
        ci_hi = r.get("ci_upper", r.get("ci_rb_upper", 0))
        bw = r.get("bw", f"{r.get('bw_left', '?')}/{r.get('bw_right', '?')}")
        n = r.get("n_obs", r.get("n_days_left", 0) + r.get("n_days_right", 0))
        lines.append(f"  {r['label']} & {coef:.4f}{stars} & ({se:.4f}) & [{ci_lo:.4f}, {ci_hi:.4f}] & {pval:.3f} & {bw} & {n:,} \\\\")
    lines += [r"\hline\hline", r"\end{tabular}",
              r"\begin{tablenotes}[flushleft]\footnotesize",
              r"\item Notes: Local linear RDD. Clustered SEs at listing level (OLS rows) or robust SEs (rdrobust rows).",
              r" * $p<0.10$, ** $p<0.05$, *** $p<0.01$.",
              r"\end{tablenotes}", r"\end{table}"]
    return "\n".join(lines)


def main():
    print("[1/4] Loading residualized panel...")
    df = pd.read_parquet(DATA_DIR / "analysis_panel_residualized.parquet")
    print(f"  {len(df):,} rows")

    # ── Panel A: Pooled OLS estimates at multiple bandwidths ─────────────

    print("\n[2/4] Pooled estimates...")
    pooled_results = []

    # A1: OLS on raw log_price (no residualization) — baseline
    for bw in BANDWIDTHS:
        print(f"  Raw log_price, BW=±{bw}d...")
        r = ols_rdd(df, "log_price", "days_from_cutoff", bw, "listing_city",
                    f"Raw, ±{bw}d")
        pooled_results.append(r)

    # A2: OLS on residualized log_price — primary
    # NOTE: Filter on RAW days_from_cutoff for bandwidth (not residualized),
    # but use residualized outcome. Residualizing the running variable
    # destroys the bandwidth window (all BWs capture entire sample).
    for bw in BANDWIDTHS:
        print(f"  Residualized, BW=±{bw}d...")
        r = ols_rdd(df, "log_price_resid", "days_from_cutoff", bw, "listing_city",
                    f"Residualized, ±{bw}d")
        pooled_results.append(r)

    # A3: rdrobust on daily-collapsed data (CCT bandwidth)
    print("  rdrobust on daily means (raw)...")
    r = rdrobust_on_collapsed(df, "log_price", "days_from_cutoff",
                               "rdrobust daily means, raw")
    pooled_results.append(r)

    print("  rdrobust on daily means (residualized)...")
    r = rdrobust_on_collapsed(df, "log_price_resid", "days_from_cutoff",
                               "rdrobust daily means, resid")
    pooled_results.append(r)

    print("\n  ═══ POOLED RESULTS ═══")
    for r in pooled_results:
        if r["status"] == "ok":
            coef = r.get("coef", r.get("coef_bc", 0))
            se = r.get("se_cluster", r.get("se_robust", 0))
            pval = r.get("pval", r.get("pval_robust", 1.0))
            stars = format_stars(pval)
            print(f"  {r['label']}: τ={coef:.4f}{stars} (SE={se:.4f}), p={pval:.3f}")

    # ── Panel B: City-specific estimates (±60d, residualized) ────────────

    print("\n[3/4] City-specific estimates (±60d, residualized)...")
    city_results = []

    for city in sorted(df["city_slug"].unique()):
        sub = df[df["city_slug"] == city]
        r = ols_rdd(sub, "log_price_resid", "days_from_cutoff", 60,
                    "listing_city", city)
        city_results.append(r)
        if r["status"] == "ok":
            stars = format_stars(r["pval"])
            print(f"  {city}: τ={r['coef']:.4f}{stars} (SE={r['se_cluster']:.4f}), p={r['pval']:.3f}, N={r['n_obs']:,}")

    # ── Panel C: Balanced-panel RDD (composition robustness) ────────────

    print("\n[3b/4] Balanced-panel RDD (listings present both sides)...")
    balanced_results = []

    for bw in BANDWIDTHS:
        # Identify listings with observations on BOTH sides of cutoff
        in_window = df[(df["days_from_cutoff"] >= -bw) & (df["days_from_cutoff"] <= bw)]
        has_pre = set(in_window[in_window["days_from_cutoff"] < 0]["listing_city"].unique())
        has_post = set(in_window[in_window["days_from_cutoff"] >= 0]["listing_city"].unique())
        balanced_ids = has_pre & has_post
        balanced_df = in_window[in_window["listing_city"].isin(balanced_ids)]

        n_total = in_window["listing_city"].nunique()
        n_balanced = len(balanced_ids)
        pct = 100 * n_balanced / n_total if n_total > 0 else 0

        print(f"  ±{bw}d: {n_balanced:,}/{n_total:,} listings ({pct:.1f}%) in balanced panel")

        r = ols_rdd(balanced_df, "log_price_resid", "days_from_cutoff", bw,
                    "listing_city", f"Balanced, ±{bw}d")
        r["n_listings_balanced"] = n_balanced
        r["n_listings_total"] = n_total
        r["pct_balanced"] = round(pct, 1)
        balanced_results.append(r)

        if r["status"] == "ok":
            stars = format_stars(r["pval"])
            print(f"    τ={r['coef']:.4f}{stars} (SE={r['se_cluster']:.4f}), N={r['n_obs']:,}")

    # ── Panel D: With minimum_nights control ─────────────────────────────

    print("\n[3c/4] RDD with minimum_nights control...")
    controlled_results = []

    for bw in BANDWIDTHS:
        sub = df[(df["days_from_cutoff"] >= -bw) & (df["days_from_cutoff"] <= bw)].copy()
        if len(sub) < 100:
            controlled_results.append({"label": f"Controlled, ±{bw}d", "status": "insufficient_data"})
            continue

        y = sub["log_price_resid"].values
        post = (sub["days_from_cutoff"] >= 0).astype(float).values
        x = sub["days_from_cutoff"].values.astype(float)
        min_n = sub["minimum_nights"].fillna(sub["minimum_nights"].median()).values.astype(float)

        # Local linear with minimum_nights control:
        # Y = α + τ·post + β₁·x + β₂·x·post + β₃·min_nights + ε
        X = np.column_stack([
            np.ones(len(y)), post, x, x * post, min_n,
        ])

        model = sm.OLS(y, X).fit(
            cov_type="cluster",
            cov_kwds={"groups": sub["listing_city"].values},
        )

        tau = model.params[1]
        se = model.bse[1]
        ci = model.conf_int()[1]
        pval = model.pvalues[1]

        r = {
            "label": f"Controlled, ±{bw}d",
            "bw": bw,
            "coef": round(float(tau), 6),
            "se_cluster": round(float(se), 6),
            "ci_lower": round(float(ci[0]), 6),
            "ci_upper": round(float(ci[1]), 6),
            "pval": round(float(pval), 6),
            "n_obs": int(len(sub)),
            "status": "ok",
        }
        controlled_results.append(r)

        stars = format_stars(pval)
        print(f"  ±{bw}d: τ={tau:.4f}{stars} (SE={se:.4f}), N={len(sub):,}")

    # ── Save outputs ─────────────────────────────────────────────────────

    print("\n[4/4] Saving tables...")

    # Markdown
    (TABLE_DIR / "itt_rdd_pooled.md").write_text(
        results_to_markdown(pooled_results, "Pooled ITT RDD Estimates"))
    (TABLE_DIR / "itt_rdd_city.md").write_text(
        results_to_markdown(city_results, "City-Specific ITT RDD Estimates (±60d, Residualized)"))

    # LaTeX
    (TABLE_DIR / "itt_rdd_pooled.tex").write_text(
        results_to_latex(pooled_results,
                         "ITT Reduced-Form RDD: Effect of Pricing Tool Rollout on Log Prices",
                         "tab:itt_pooled"))
    (TABLE_DIR / "itt_rdd_city.tex").write_text(
        results_to_latex(city_results,
                         "City-Specific ITT Estimates",
                         "tab:itt_city"))

    # Balanced panel + controlled tables
    (TABLE_DIR / "itt_rdd_balanced.md").write_text(
        results_to_markdown(balanced_results, "Balanced-Panel ITT RDD Estimates (listings present both sides)"))
    (TABLE_DIR / "itt_rdd_controlled.md").write_text(
        results_to_markdown(controlled_results, "ITT RDD with Minimum-Nights Control"))

    # JSON
    all_results = {
        "pooled": pooled_results,
        "city": city_results,
        "balanced": balanced_results,
        "controlled": controlled_results,
        "cutoff": "2023-09-01",
        "treatment": "Airbnb 2023 Summer Release: Compare Similar Listings + Redesigned Pricing Tools",
        "outcome": "log_price",
        "residualization": "city×month FE + DOW FE + cross-fitted Ridge (listing chars, Fourier)",
        "clustering": "listing_city",
    }
    (DATA_DIR / "itt_rdd_results.json").write_text(json.dumps(all_results, indent=2))

    print("Done.")
    print(f"  Tables → {TABLE_DIR}/itt_rdd_*.{{tex,md}}")


if __name__ == "__main__":
    main()
