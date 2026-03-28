#!/usr/bin/env python3
"""Session 3, Script 08: DDD price level estimation.

Year-over-year DiD with listing FE + week-of-year FE:
  log_price_it = α_i + γ_w + τ · year2023 + ε_it

And Oct 1 DDD:
  log_price_it = α_i + γ_w + τ · (year2023 × post_oct1) + ε_it

Uses Frisch-Waugh iterative demeaning for listing FE (94K groups).

Output:
  - output/tables/ddd_price_levels.{tex,md}
  - output/tables/ddd_price_city.{tex,md}
  - output/tables/ddd_oct_cutoff.{tex,md}
  - data/processed/ddd_price_results.json
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "processed"
TABLE_DIR = REPO / "output" / "tables"
TABLE_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42


def demean_twoway(df, y_col, fe1_col, fe2_col, max_iter=10, tol=1e-10):
    """Iterative Frisch-Waugh demeaning for two-way FE."""
    resid = df[y_col].values.astype(np.float64).copy()
    for iteration in range(max_iter):
        m1 = pd.Series(resid).groupby(df[fe1_col].values).transform("mean").values
        resid -= m1
        m2 = pd.Series(resid).groupby(df[fe2_col].values).transform("mean").values
        resid -= m2
        if np.abs(m1).max() < tol and np.abs(m2).max() < tol:
            break
    return resid


def run_did(df, y_col, treatment_cols, fe1, fe2, cluster_col, label):
    """Run DiD via Frisch-Waugh demeaning + OLS."""
    # Demean outcome
    y_dm = demean_twoway(df, y_col, fe1, fe2)

    # Demean treatment variable(s)
    X_parts = []
    col_names = []
    for tcol in treatment_cols:
        x_dm = demean_twoway(df, tcol, fe1, fe2)
        X_parts.append(x_dm)
        col_names.append(tcol)

    X = np.column_stack(X_parts)
    model = sm.OLS(y_dm, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": df[cluster_col].values},
    )

    results = []
    for i, cname in enumerate(col_names):
        results.append({
            "label": f"{label} [{cname}]" if len(col_names) > 1 else label,
            "var": cname,
            "coef": round(float(model.params[i]), 6),
            "se": round(float(model.bse[i]), 6),
            "ci_lower": round(float(model.conf_int()[i, 0]), 6),
            "ci_upper": round(float(model.conf_int()[i, 1]), 6),
            "pval": round(float(model.pvalues[i]), 6),
            "n_obs": int(model.nobs),
            "n_clusters": int(df[cluster_col].nunique()),
            "r2_within": round(float(1 - np.sum(model.resid ** 2) / np.sum(y_dm ** 2)), 6),
            "status": "ok",
        })
    return results


def format_stars(pval):
    if pval < 0.01: return "***"
    if pval < 0.05: return "**"
    if pval < 0.10: return "*"
    return ""


def results_to_markdown(results, title):
    lines = [f"### {title}", "",
             "| Specification | τ | SE | 95% CI | p-val | N | Clusters |",
             "|---|---:|---:|---|---:|---:|---:|"]
    for r in results:
        if r["status"] != "ok":
            lines.append(f"| {r['label']} | — | — | — | — | — | — |")
            continue
        s = format_stars(r["pval"])
        lines.append(f"| {r['label']} | {r['coef']:.4f}{s} | {r['se']:.4f} "
                     f"| [{r['ci_lower']:.4f}, {r['ci_upper']:.4f}] "
                     f"| {r['pval']:.3f} | {r['n_obs']:,} | {r['n_clusters']:,} |")
    return "\n".join(lines)


def results_to_latex(results, caption, label):
    lines = [
        r"\begin{table}[htbp]", r"\centering",
        f"\\caption{{{caption}}}", f"\\label{{{label}}}",
        r"\begin{tabular}{lcccccc}", r"\hline\hline",
        r" & $\hat{\tau}$ & SE & 95\% CI & $p$ & $N$ & Clusters \\",
        r"\hline",
    ]
    for r in results:
        if r["status"] != "ok": continue
        s = format_stars(r["pval"])
        lines.append(f"  {r['label']} & {r['coef']:.4f}{s} & ({r['se']:.4f}) "
                     f"& [{r['ci_lower']:.4f}, {r['ci_upper']:.4f}] "
                     f"& {r['pval']:.3f} & {r['n_obs']:,} & {r['n_clusters']:,} \\\\")
    lines += [r"\hline\hline", r"\end{tabular}",
              r"\begin{tablenotes}[flushleft]\footnotesize",
              r"\item Notes: Year-over-year DiD with listing FE and week-of-year FE.",
              r" Frisch-Waugh demeaning. Clustered SEs at listing level.",
              r" * $p<0.10$, ** $p<0.05$, *** $p<0.01$.",
              r"\end{tablenotes}", r"\end{table}"]
    return "\n".join(lines)


def main():
    print("[1/4] Loading DDD panel...")
    df = pd.read_parquet(DATA_DIR / "ddd_panel.parquet")
    print(f"  {len(df):,} rows, {df['listing_city'].nunique():,} listings")

    # ── Panel A: Year-over-year DiD at multiple windows ──────────────────

    print("\n[2/4] Year-over-year DiD (log_price ~ year2023)...")
    pooled_results = []

    windows = [
        ("Weeks 38-52 (full)", 38, 52),
        ("Weeks 38-48 (drop Dec)", 38, 48),
        ("Weeks 40-52 (post-only)", 40, 52),
    ]

    for wlabel, wmin, wmax in windows:
        sub = df[(df["week_of_year"] >= wmin) & (df["week_of_year"] <= wmax)]
        print(f"  {wlabel}: {len(sub):,} obs...")
        r = run_did(sub, "log_price", ["year2023"],
                    "listing_city", "week_of_year", "listing_city", wlabel)
        pooled_results.extend(r)

    print("\n  ═══ POOLED RESULTS ═══")
    for r in pooled_results:
        s = format_stars(r["pval"])
        print(f"  {r['label']}: τ={r['coef']:.4f}{s} (SE={r['se']:.4f}), p={r['pval']:.3f}")

    # ── Panel B: Oct 1 DDD ───────────────────────────────────────────────

    print("\n[3/4] Oct 1 cutoff DDD...")
    oct_results = []

    # Full interaction model: year2023 + year2023×post_oct1
    r = run_did(df, "log_price", ["year2023", "year2023_x_post_oct1"],
                "listing_city", "week_of_year", "listing_city",
                "Oct 1 DDD (full)")
    oct_results.extend(r)

    print("  ═══ OCT 1 DDD ═══")
    for r in oct_results:
        s = format_stars(r["pval"])
        print(f"  {r['label']}: τ={r['coef']:.4f}{s} (SE={r['se']:.4f}), p={r['pval']:.3f}")

    # ── Panel C: City-specific ───────────────────────────────────────────

    print("\n  City-specific (weeks 38-52)...")
    city_results = []
    for city in sorted(df["city_slug"].unique()):
        sub = df[df["city_slug"] == city]
        r = run_did(sub, "log_price", ["year2023"],
                    "listing_city", "week_of_year", "listing_city", city)
        city_results.extend(r)
        s = format_stars(r[0]["pval"])
        print(f"  {city}: τ={r[0]['coef']:.4f}{s} (SE={r[0]['se']:.4f})")

    # ── Save outputs ─────────────────────────────────────────────────────

    print("\n[4/4] Saving...")
    (TABLE_DIR / "ddd_price_levels.md").write_text(
        results_to_markdown(pooled_results, "Year-over-Year DiD: Log Price"))
    (TABLE_DIR / "ddd_price_levels.tex").write_text(
        results_to_latex(pooled_results, "Year-over-Year DiD: Effect on Log Prices", "tab:ddd_price"))
    (TABLE_DIR / "ddd_oct_cutoff.md").write_text(
        results_to_markdown(oct_results, "Oct 1 DDD: Log Price"))
    (TABLE_DIR / "ddd_oct_cutoff.tex").write_text(
        results_to_latex(oct_results, "Oct 1 DDD: Effect on Log Prices", "tab:ddd_oct"))
    (TABLE_DIR / "ddd_price_city.md").write_text(
        results_to_markdown(city_results, "City-Specific Year-over-Year DiD"))
    (TABLE_DIR / "ddd_price_city.tex").write_text(
        results_to_latex(city_results, "City-Specific Year-over-Year DiD", "tab:ddd_city"))

    all_results = {
        "pooled": pooled_results,
        "oct_ddd": oct_results,
        "city": city_results,
    }
    (DATA_DIR / "ddd_price_results.json").write_text(json.dumps(all_results, indent=2))
    print("Done.")


if __name__ == "__main__":
    main()
