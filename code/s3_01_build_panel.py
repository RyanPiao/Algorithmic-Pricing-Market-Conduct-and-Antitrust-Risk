#!/usr/bin/env python3
"""Session 3, Script 01: Build analysis panel from merged city data.

Loads merged listing-day data for 8 US cities from external drive,
applies cutoff = 2023-09-01 (official rollout of Airbnb's redesigned
pricing tools / "Compare Similar Listings" feature from 2023 Summer Release),
constructs running variable, bandwidth windows, and seasonal controls.

Treatment event:
  - May 3, 2023: Beta / Early Access launch (2023 Summer Release)
  - Sep 1, 2023: Official rollout to all hosts

Output: data/processed/analysis_panel.parquet
"""

from __future__ import annotations

import gc
import json
from pathlib import Path

import numpy as np
import pandas as pd

# ── Config ──────────────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
DATA_MERGE = REPO / "data" / "merge"
OUT_DIR = REPO / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CITIES = [
    "boston",
    "new-york-city",
    "los-angeles",
    "san-francisco",
    "austin",
    "chicago",
    "seattle",
    "washington-dc",
]

# Treatment cutoff: official rollout date
CUTOFF = pd.Timestamp("2023-09-01")
BETA_DATE = pd.Timestamp("2023-05-03")

# Bandwidth windows (months before/after cutoff)
BW_MONTHS = [1, 2, 3]

# US federal holidays 2022-2023 (observed dates)
US_HOLIDAYS = [
    # 2022
    "2022-09-05",  # Labor Day
    "2022-10-10",  # Columbus Day
    "2022-11-11",  # Veterans Day
    "2022-11-24",  # Thanksgiving
    "2022-12-25",  # Christmas (observed 12/26)
    "2022-12-26",
    # 2023
    "2023-01-01",  # New Year
    "2023-01-02",  # NY observed
    "2023-01-16",  # MLK Day
    "2023-02-20",  # Presidents Day
    "2023-05-29",  # Memorial Day
    "2023-07-04",  # Independence Day
    "2023-09-04",  # Labor Day
    "2023-10-09",  # Columbus Day
    "2023-11-10",  # Veterans Day observed
    "2023-11-23",  # Thanksgiving
    "2023-12-25",  # Christmas
]
HOLIDAY_SET = set(pd.to_datetime(US_HOLIDAYS).date)

SEED = 42
np.random.seed(SEED)


def load_city(city_slug: str) -> pd.DataFrame:
    """Load a single city's merged data with minimal columns."""
    path = DATA_MERGE / f"merged_{city_slug}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing: {path}")

    usecols = [
        "listing_id",
        "date",
        "available",
        "price",
        "price_usd",
        "is_weekend",
        "minimum_nights",
        "maximum_nights",
        "price_change_count",
        "host_id",
        "host_is_superhost",
        "host_response_rate",
        "host_acceptance_rate",
        "host_identity_verified",
        "neighbourhood_cleansed",
        "property_type",
        "room_type",
        "accommodates",
        "bathrooms",
        "bedrooms",
        "beds",
        "amenities_count",
        "number_of_reviews",
        "review_scores_rating",
        "instant_bookable",
        "calculated_host_listings_count",
        "availability_365",
    ]

    df = pd.read_csv(path, usecols=usecols, low_memory=False)
    df["city_slug"] = city_slug
    return df


def build_panel(df: pd.DataFrame) -> pd.DataFrame:
    """Add RDD variables and seasonal controls."""

    # Parse dates
    df["date"] = pd.to_datetime(df["date"])

    # Filter to valid prices
    df = df[(df["price_usd"] > 0) & (df["price_usd"] < 10_000)].copy()

    # Core outcome
    df["log_price"] = np.log(df["price_usd"])

    # Running variable and treatment indicator
    df["days_from_cutoff"] = (df["date"] - CUTOFF).dt.days
    df["post_cutoff"] = (df["date"] >= CUTOFF).astype(np.int8)

    # Beta period indicator (May 3 - Aug 31, 2023)
    df["beta_period"] = (
        (df["date"] >= BETA_DATE) & (df["date"] < CUTOFF)
    ).astype(np.int8)

    # Bandwidth windows
    for m in BW_MONTHS:
        pre = CUTOFF - pd.DateOffset(months=m)
        post = CUTOFF + pd.DateOffset(months=m)
        df[f"in_bw_{m}m"] = (
            (df["date"] >= pre) & (df["date"] <= post)
        ).astype(np.int8)

    # Seasonal controls
    df["month"] = df["date"].dt.month.astype(np.int8)
    df["day_of_week"] = df["date"].dt.dayofweek.astype(np.int8)  # 0=Mon
    df["day_of_year"] = df["date"].dt.dayofyear.astype(np.int16)
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(np.int8)
    df["is_holiday"] = df["date"].dt.date.isin(HOLIDAY_SET).astype(np.int8)

    # City × month interaction (for FE)
    df["city_month"] = df["city_slug"] + "_" + df["month"].astype(str)

    # Parse host_acceptance_rate (string with %)
    df["host_acceptance_rate"] = (
        df["host_acceptance_rate"]
        .astype(str)
        .str.rstrip("%")
        .replace({"nan": np.nan, "": np.nan})
        .astype(float)
        / 100.0
    )

    # Listing-level identifier for clustering
    df["listing_city"] = df["city_slug"] + "_" + df["listing_id"].astype(str)

    return df


def compute_summary(df: pd.DataFrame) -> dict:
    """Panel summary statistics."""
    summary = {
        "total_rows": int(len(df)),
        "n_cities": int(df["city_slug"].nunique()),
        "n_listings": int(df["listing_city"].nunique()),
        "date_range": [str(df["date"].min().date()), str(df["date"].max().date())],
        "cutoff": str(CUTOFF.date()),
        "beta_date": str(BETA_DATE.date()),
    }

    # Per-city counts
    city_stats = []
    for city, g in df.groupby("city_slug"):
        city_stats.append({
            "city": city,
            "rows": int(len(g)),
            "listings": int(g["listing_city"].nunique()),
            "date_min": str(g["date"].min().date()),
            "date_max": str(g["date"].max().date()),
            "pre_rows": int((g["post_cutoff"] == 0).sum()),
            "post_rows": int((g["post_cutoff"] == 1).sum()),
            "mean_price": round(float(g["price_usd"].mean()), 2),
            "median_price": round(float(g["price_usd"].median()), 2),
        })
    summary["cities"] = city_stats

    # Bandwidth window sizes
    for m in BW_MONTHS:
        col = f"in_bw_{m}m"
        sub = df[df[col] == 1]
        summary[f"bw_{m}m_rows"] = int(len(sub))
        summary[f"bw_{m}m_pre"] = int((sub["post_cutoff"] == 0).sum())
        summary[f"bw_{m}m_post"] = int((sub["post_cutoff"] == 1).sum())

    return summary


def main():
    print("[1/4] Loading city data...")
    frames = []
    for city in CITIES:
        print(f"  Loading {city}...")
        frames.append(load_city(city))

    print("[2/4] Concatenating and building panel...")
    df = pd.concat(frames, ignore_index=True)
    del frames
    gc.collect()

    df = build_panel(df)

    print("[3/4] Computing summary stats...")
    summary = compute_summary(df)
    print(f"  Total: {summary['total_rows']:,} rows, {summary['n_listings']:,} listings")
    for cs in summary["cities"]:
        print(f"  {cs['city']}: {cs['rows']:,} rows ({cs['pre_rows']:,} pre / {cs['post_rows']:,} post)")

    for m in BW_MONTHS:
        print(f"  ±{m}m window: {summary[f'bw_{m}m_rows']:,} rows ({summary[f'bw_{m}m_pre']:,} pre / {summary[f'bw_{m}m_post']:,} post)")

    # Save summary
    summary_path = OUT_DIR / "panel_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"  Summary → {summary_path}")

    print("[4/4] Saving panel to parquet...")
    out_path = OUT_DIR / "analysis_panel.parquet"
    df.to_parquet(out_path, index=False, engine="pyarrow")
    print(f"  Panel → {out_path} ({out_path.stat().st_size / 1e9:.2f} GB)")

    print("Done.")


if __name__ == "__main__":
    main()
