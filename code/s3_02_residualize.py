#!/usr/bin/env python3
"""Session 3, Script 02: Cross-fitted residualization for RDiT.

Removes seasonal confounders from outcome and running variable before
RDD estimation, following Hausman & Rapson (2018) / Noack-Olma-Rothe (2025).

Approach: two-stage residualization
  Stage 1: Absorb high-dimensional FE via group demeaning (Frisch-Waugh)
    - City × month-of-year FE (captures city-specific seasonal patterns)
    - Day-of-week FE (captures weekly cycles)
  Stage 2: K-fold cross-fitted Ridge on remaining controls
    - Fourier terms (day-of-year harmonics)
    - Listing characteristics
    - Holiday indicators

This is more memory-efficient than full LASSO on 22M obs while achieving
the same goal: removing predictable seasonal variation.

Output: data/processed/analysis_panel_residualized.parquet
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "processed"
OUT_DIR = DATA_DIR

K_FOLDS = 5
SEED = 42
np.random.seed(SEED)


def absorb_fe(df: pd.DataFrame, y_col: str, fe_cols: list[str]) -> np.ndarray:
    """Absorb fixed effects via iterative group demeaning (Frisch-Waugh).

    Equivalent to including dummies but uses O(N) memory instead of O(N×K).
    Converges in ~3 iterations for non-overlapping FE groups.
    """
    residual = df[y_col].values.astype(np.float64).copy()

    for iteration in range(5):  # Usually converges in 2-3
        max_change = 0.0
        for fe_col in fe_cols:
            groups = df[fe_col].values
            # Compute group means efficiently
            unique_groups = np.unique(groups)
            group_means = pd.Series(residual).groupby(groups).transform("mean").values
            new_residual = residual - group_means
            max_change = max(max_change, np.abs(residual - new_residual).max())
            residual = new_residual

        if max_change < 1e-10:
            print(f"    FE absorption converged at iteration {iteration + 1}")
            break

    return residual


def build_continuous_features(df: pd.DataFrame) -> np.ndarray:
    """Build remaining features for Stage 2 (after FE absorption).

    Only continuous/low-dimensional features that aren't absorbed by FE.
    """
    parts = []

    # Fourier terms for day-of-year (smooth seasonality residual)
    doy = df["day_of_year"].values.astype(np.float64)
    for k in range(1, 4):
        parts.append(np.sin(2 * np.pi * k * doy / 365).reshape(-1, 1))
        parts.append(np.cos(2 * np.pi * k * doy / 365).reshape(-1, 1))

    # Holiday indicator
    parts.append(df["is_holiday"].values.reshape(-1, 1).astype(np.float64))

    # is_weekend (residual after DOW FE — mostly absorbed, but keep for interaction)
    parts.append(df["is_weekend"].values.reshape(-1, 1).astype(np.float64))

    # Listing characteristics
    cont_cols = ["accommodates", "bedrooms", "bathrooms", "beds", "amenities_count"]
    for col in cont_cols:
        vals = df[col].fillna(0).values.astype(np.float64).reshape(-1, 1)
        parts.append(vals)

    # Room type dummies (small: 3 dummies)
    rt_dummies = pd.get_dummies(df["room_type"], prefix="rt", drop_first=True, dtype=np.float64)
    parts.append(rt_dummies.values)

    X = np.hstack(parts)
    return X


def cross_fitted_residualize_stage2(
    y_absorbed: np.ndarray,
    X: np.ndarray,
    fold_ids: np.ndarray,
    k_folds: int,
) -> np.ndarray:
    """Stage 2: K-fold cross-fitted Ridge on continuous features."""
    residuals = np.empty_like(y_absorbed)

    for k in range(k_folds):
        mask_train = fold_ids != k
        mask_test = fold_ids == k

        ridge = RidgeCV(
            alphas=[0.01, 0.1, 1.0, 10.0, 100.0],
            cv=3,
        )
        ridge.fit(X[mask_train], y_absorbed[mask_train])
        yhat = ridge.predict(X[mask_test])
        residuals[mask_test] = y_absorbed[mask_test] - yhat

        r2 = ridge.score(X[mask_train], y_absorbed[mask_train])
        print(f"    Fold {k+1}/{k_folds}: alpha={ridge.alpha_:.2f}, R²_train={r2:.4f}")

    return residuals


def main():
    print("[1/6] Loading analysis panel (±3m window)...")
    panel_path = DATA_DIR / "analysis_panel.parquet"
    df = pd.read_parquet(panel_path)

    # Filter to ±3m window
    df = df[df["in_bw_3m"] == 1].copy()
    print(f"  {len(df):,} rows in ±3m window")

    # Drop rows with NaN in key variables
    key_cols = ["log_price", "days_from_cutoff", "city_month", "day_of_week"]
    n_before = len(df)
    df = df.dropna(subset=key_cols)
    print(f"  Dropped {n_before - len(df):,} rows with NaN in key columns")

    print("\n[2/6] Stage 1: Absorbing city×month and day-of-week FE...")
    fe_cols = ["city_month", "day_of_week"]

    # Residualize log_price
    print("  Absorbing FE from log_price...")
    df["log_price_absorbed"] = absorb_fe(df, "log_price", fe_cols)

    # Residualize running variable
    print("  Absorbing FE from days_from_cutoff...")
    df["days_from_cutoff_absorbed"] = absorb_fe(df, "days_from_cutoff", fe_cols)

    # Check how much variance FE absorbed
    var_orig = df["log_price"].var()
    var_absorbed = df["log_price_absorbed"].var()
    r2_fe = 1 - var_absorbed / var_orig
    print(f"  FE R² for log_price: {r2_fe:.4f} ({r2_fe*100:.1f}% variance absorbed)")

    print("\n[3/6] Building Stage 2 features...")
    X = build_continuous_features(df)
    print(f"  Feature matrix: {X.shape[0]:,} × {X.shape[1]}")

    # Handle remaining NaN
    nan_mask = np.isnan(X).any(axis=1)
    if nan_mask.sum() > 0:
        print(f"  Dropping {nan_mask.sum():,} rows with NaN in Stage 2 features")
        df = df[~nan_mask].copy()
        X = X[~nan_mask]

    print("\n[4/6] Assigning listing-level folds...")
    listings = df["listing_city"].unique()
    rng = np.random.RandomState(SEED)
    listing_folds = pd.Series(
        rng.randint(0, K_FOLDS, size=len(listings)),
        index=listings,
    )
    fold_ids = listing_folds[df["listing_city"].values].values

    for k in range(K_FOLDS):
        print(f"  Fold {k+1}: {(fold_ids == k).sum():,} obs")

    print("\n[5/6] Stage 2: Cross-fitted Ridge on residuals...")

    print("  Residualizing log_price_absorbed...")
    df["log_price_resid"] = cross_fitted_residualize_stage2(
        df["log_price_absorbed"].values, X, fold_ids, K_FOLDS
    )

    print("  Residualizing days_from_cutoff_absorbed...")
    df["days_from_cutoff_resid"] = cross_fitted_residualize_stage2(
        df["days_from_cutoff_absorbed"].values, X, fold_ids, K_FOLDS
    )

    # Final R² computation
    ss_total = np.sum((df["log_price"].values - df["log_price"].values.mean()) ** 2)
    ss_resid = np.sum(df["log_price_resid"].values ** 2)
    r2_total = 1 - ss_resid / ss_total
    print(f"\n  Total seasonal model R² (FE + Ridge, cross-fitted): {r2_total:.4f}")
    print(f"  → {r2_total*100:.1f}% of price variance explained by seasonality + controls")

    print("\n  Residual summary:")
    for col in ["log_price_resid", "days_from_cutoff_resid"]:
        vals = df[col].values
        print(f"    {col}: mean={vals.mean():.6f}, std={vals.std():.4f}")

    print("\n[6/6] Saving...")
    out_path = OUT_DIR / "analysis_panel_residualized.parquet"
    df.to_parquet(out_path, index=False, engine="pyarrow")
    print(f"  Panel → {out_path} ({out_path.stat().st_size / 1e9:.2f} GB)")

    meta = {
        "method": "two_stage_FE_absorption_plus_cross_fitted_ridge",
        "stage1_fe": fe_cols,
        "stage2_features": int(X.shape[1]),
        "k_folds": K_FOLDS,
        "seed": SEED,
        "n_obs": int(len(df)),
        "r2_fe_only": round(float(r2_fe), 6),
        "r2_total": round(float(r2_total), 6),
        "cutoff": "2023-09-01",
        "window": "±3m",
    }
    (OUT_DIR / "residualization_meta.json").write_text(json.dumps(meta, indent=2))
    print("Done.")


if __name__ == "__main__":
    main()
