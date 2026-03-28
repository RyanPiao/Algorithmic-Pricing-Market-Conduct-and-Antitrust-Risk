#!/usr/bin/env python3
"""Session 3, Script 13: Placebo bandwidth profiles at Sep 1, 2022.

Referees' concern: the bandwidth-declining pattern (τ shrinks as BW narrows)
could be seasonal confounding rather than a treatment effect. If the SAME
specification run at Sep 1, 2022 — where no treatment occurred — also shows
a significant discontinuity, the main result is suspect.

Approach:
  1. Load the residualized analysis panel (which spans ~Jun–Dec 2023).
  2. Separately load the RAW analysis panel to get 2022 observations
     (the residualized panel only contains the ±3m window around Sep 2023).
  3. For the 2022 placebo: re-center the running variable at Sep 1, 2022,
     filter to 2022 data within each bandwidth, run the same OLS local
     linear RDD specification from s3_03_itt_rdd.py.
  4. Report a bandwidth-declining table comparable to the main results.

Output: output/tables/placebo_bandwidth_2022.md

Usage:
  python code/s3_13_placebo_bandwidth.py
"""

from __future__ import annotations

import json
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
np.random.seed(SEED)

BANDWIDTHS = [30, 45, 60, 90]  # days — same as main spec

# Placebo cutoff: same calendar date, prior year
PLACEBO_CUTOFF_2022 = pd.Timestamp("2022-09-01")

# Main cutoff for reference
MAIN_CUTOFF = pd.Timestamp("2023-09-01")


# ── OLS RDD (identical to s3_03_itt_rdd.py) ──────────────────────────────────

def ols_rdd(
    df: pd.DataFrame,
    y_col: str,
    x_col: str,
    bw: int,
    cluster_col: str,
    label: str,
) -> dict:
    """Local linear OLS RDD within bandwidth, clustered SEs.

    Specification: Y = α + τ·1(x≥0) + β₁·x + β₂·x·1(x≥0) + ε
    This is the SAME specification as s3_03_itt_rdd.ols_rdd().
    """
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


# ── Formatting helpers ───────────────────────────────────────────────────────

def format_stars(pval: float) -> str:
    if pval < 0.01:
        return "***"
    elif pval < 0.05:
        return "**"
    elif pval < 0.10:
        return "*"
    return ""


def results_to_markdown(main_results: list[dict], placebo_results: list[dict],
                        title: str) -> str:
    """Side-by-side table: main vs. placebo at each bandwidth."""
    lines = [
        f"### {title}",
        "",
        "Placebo test: identical RDD specification run at Sep 1, 2022 (no treatment).",
        "If the placebo shows a similar pattern, the main result reflects seasonality,",
        "not a causal effect.",
        "",
        "| BW (days) | Main τ (2023) | SE | p-val | Placebo τ (2022) | SE | p-val | N (main) | N (placebo) |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for m_r, p_r in zip(main_results, placebo_results):
        bw = m_r.get("bw", "?")

        if m_r["status"] == "ok":
            m_coef = m_r["coef"]
            m_se = m_r["se_cluster"]
            m_pval = m_r["pval"]
            m_stars = format_stars(m_pval)
            m_n = m_r["n_obs"]
            m_str = f"{m_coef:.4f}{m_stars}"
            m_se_str = f"{m_se:.4f}"
            m_p_str = f"{m_pval:.3f}"
            m_n_str = f"{m_n:,}"
        else:
            m_str = m_se_str = m_p_str = m_n_str = "—"

        if p_r["status"] == "ok":
            p_coef = p_r["coef"]
            p_se = p_r["se_cluster"]
            p_pval = p_r["pval"]
            p_stars = format_stars(p_pval)
            p_n = p_r["n_obs"]
            p_str = f"{p_coef:.4f}{p_stars}"
            p_se_str = f"{p_se:.4f}"
            p_p_str = f"{p_pval:.3f}"
            p_n_str = f"{p_n:,}"
        else:
            p_str = p_se_str = p_p_str = p_n_str = "—"

        lines.append(
            f"| ±{bw}d | {m_str} | {m_se_str} | {m_p_str} | "
            f"{p_str} | {p_se_str} | {p_p_str} | {m_n_str} | {p_n_str} |"
        )

    lines += [
        "",
        "Notes: Local linear RDD with listing-clustered SEs. Main cutoff = Sep 1, 2023.",
        "Placebo cutoff = Sep 1, 2022. Outcome = log(price). * p<0.10, ** p<0.05, *** p<0.01.",
    ]
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # ── Load the full analysis panel (has both 2022 and 2023 data) ───────
    print("[1/5] Loading analysis panel...")
    panel_path = DATA_DIR / "analysis_panel.parquet"
    df_full = pd.read_parquet(panel_path)
    df_full["date"] = pd.to_datetime(df_full["date"])
    print(f"  Full panel: {len(df_full):,} rows")
    print(f"  Date range: {df_full['date'].min().date()} to {df_full['date'].max().date()}")

    # ── Load residualized panel for main spec reference ──────────────────
    print("\n[2/5] Loading residualized panel (main spec reference)...")
    df_resid = pd.read_parquet(DATA_DIR / "analysis_panel_residualized.parquet")
    print(f"  Residualized panel: {len(df_resid):,} rows")

    # ── Main spec: bandwidth profile at Sep 1, 2023 (residualized) ──────
    print("\n[3/5] Main specification: bandwidth profile at Sep 1, 2023...")
    main_results = []
    for bw in BANDWIDTHS:
        r = ols_rdd(df_resid, "log_price_resid", "days_from_cutoff", bw,
                    "listing_city", f"Main 2023, ±{bw}d")
        main_results.append(r)
        if r["status"] == "ok":
            stars = format_stars(r["pval"])
            print(f"  ±{bw}d: τ={r['coef']:.4f}{stars} (SE={r['se_cluster']:.4f}), "
                  f"p={r['pval']:.3f}, N={r['n_obs']:,}")

    # ── Placebo: Sep 1, 2022 (on RAW log_price, 2022 data only) ─────────
    # NOTE: The residualized panel only covers ±3m around Sep 2023, so
    # we use the raw analysis panel filtered to 2022 for the placebo.
    # This is methodologically appropriate: the placebo tests whether the
    # calendar date itself creates a discontinuity in raw prices.

    print("\n[4/5] Placebo specification: bandwidth profile at Sep 1, 2022...")

    # Filter to 2022 data and re-center running variable at Sep 1, 2022
    df_2022 = df_full[df_full["date"].dt.year == 2022].copy()
    df_2022["days_from_placebo"] = (df_2022["date"] - PLACEBO_CUTOFF_2022).dt.days
    print(f"  2022 observations: {len(df_2022):,}")
    print(f"  2022 date range: {df_2022['date'].min().date()} to {df_2022['date'].max().date()}")

    placebo_results_2022 = []
    for bw in BANDWIDTHS:
        r = ols_rdd(df_2022, "log_price", "days_from_placebo", bw,
                    "listing_city", f"Placebo 2022, ±{bw}d")
        placebo_results_2022.append(r)
        if r["status"] == "ok":
            stars = format_stars(r["pval"])
            print(f"  ±{bw}d: τ={r['coef']:.4f}{stars} (SE={r['se_cluster']:.4f}), "
                  f"p={r['pval']:.3f}, N={r['n_obs']:,}")
        else:
            print(f"  ±{bw}d: {r['status']}")

    # ── Also run on RAW 2023 for apples-to-apples comparison ─────────────
    # (The main spec uses residualized outcome; for a fair placebo comparison,
    # we also report the raw 2023 spec.)
    print("\n  Raw 2023 specification (for comparison)...")
    df_2023 = df_full[df_full["date"].dt.year >= 2023].copy()
    df_2023["days_from_cutoff"] = (df_2023["date"] - MAIN_CUTOFF).dt.days

    raw_2023_results = []
    for bw in BANDWIDTHS:
        r = ols_rdd(df_2023, "log_price", "days_from_cutoff", bw,
                    "listing_city", f"Raw 2023, ±{bw}d")
        raw_2023_results.append(r)
        if r["status"] == "ok":
            stars = format_stars(r["pval"])
            print(f"  ±{bw}d: τ={r['coef']:.4f}{stars} (SE={r['se_cluster']:.4f}), "
                  f"p={r['pval']:.3f}, N={r['n_obs']:,}")

    # ── Save outputs ─────────────────────────────────────────────────────
    print("\n[5/5] Saving tables...")

    # Side-by-side markdown: residualized main vs. raw placebo
    md_resid = results_to_markdown(
        main_results, placebo_results_2022,
        "Placebo Bandwidth Profile: Main (Residualized, 2023) vs. Placebo (Raw, 2022)"
    )

    # Also add raw 2023 vs raw 2022 for strict apples-to-apples
    md_raw = results_to_markdown(
        raw_2023_results, placebo_results_2022,
        "Placebo Bandwidth Profile: Raw 2023 vs. Raw 2022 (apples-to-apples)"
    )

    full_md = md_resid + "\n\n---\n\n" + md_raw

    out_path = TABLE_DIR / "placebo_bandwidth_2022.md"
    out_path.write_text(full_md)
    print(f"  Table → {out_path}")

    # JSON results for downstream use
    json_results = {
        "main_residualized_2023": main_results,
        "placebo_raw_2022": placebo_results_2022,
        "raw_2023": raw_2023_results,
        "main_cutoff": "2023-09-01",
        "placebo_cutoff": "2022-09-01",
        "bandwidths": BANDWIDTHS,
        "interpretation": (
            "If the placebo (2022) shows similar magnitude/significance as the "
            "main (2023), the bandwidth-declining pattern is seasonal, not causal."
        ),
    }
    json_path = DATA_DIR / "placebo_bandwidth_results.json"
    json_path.write_text(json.dumps(json_results, indent=2))
    print(f"  JSON  → {json_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
