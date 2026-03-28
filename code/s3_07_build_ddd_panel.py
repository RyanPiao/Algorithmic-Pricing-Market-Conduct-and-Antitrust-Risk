#!/usr/bin/env python3
"""Session 3, Script 07: Build DDD (year-over-year DiD) panel.

Constructs a balanced panel of listings observed in Sep-Dec of BOTH
2022 and 2023, with year-over-year treatment indicators.

Design:
  - 2022 Sep-Dec: control year (no pricing tool)
  - 2023 Sep-Dec: treatment year (pricing tool rolled out Sep 1)
  - Listing FE + week-of-year FE absorb composition and seasonality

Output: data/processed/ddd_panel.parquet
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "processed"
OUT_DIR = DATA_DIR

SEED = 42
np.random.seed(SEED)

# Weeks 38-52 are available in all cities for both years.
# Week 38 starts ~Sep 18 (2022) / ~Sep 18 (2023).
WEEK_MIN = 38
WEEK_MAX = 52
OCT1_WEEK = 40  # Week 40 starts ~Oct 2


def main():
    print("[1/5] Loading analysis panel...")
    cols = [
        "listing_city", "city_slug", "date", "listing_id", "host_id",
        "log_price", "price_usd", "available", "minimum_nights",
        "day_of_week", "month", "is_weekend", "is_holiday",
        "week_of_year", "neighbourhood_cleansed", "property_type",
        "room_type", "accommodates", "bedrooms", "bathrooms",
        "host_is_superhost", "number_of_reviews", "instant_bookable",
        "calculated_host_listings_count",
    ]
    df = pd.read_parquet(DATA_DIR / "analysis_panel.parquet", columns=cols)
    print(f"  Loaded {len(df):,} rows, {df['listing_city'].nunique():,} listings")

    print("[2/5] Creating year variables...")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year.astype(np.int16)
    df["year2023"] = (df["year"] == 2023).astype(np.int8)

    # Week of year (ISO)
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(np.int8)

    # Post Oct 1 indicator (within each year)
    df["post_oct1"] = (df["week_of_year"] >= OCT1_WEEK).astype(np.int8)

    # DDD interaction
    df["year2023_x_post_oct1"] = (df["year2023"] * df["post_oct1"]).astype(np.int8)

    print("[3/5] Identifying balanced panel...")
    # Listings present in weeks 38-52 of BOTH years
    in_window = df[(df["week_of_year"] >= WEEK_MIN) & (df["week_of_year"] <= WEEK_MAX)]

    listings_2022 = set(in_window[in_window["year"] == 2022]["listing_city"].unique())
    listings_2023 = set(in_window[in_window["year"] == 2023]["listing_city"].unique())
    balanced_listings = listings_2022 & listings_2023

    print(f"  Listings in 2022 weeks {WEEK_MIN}-{WEEK_MAX}: {len(listings_2022):,}")
    print(f"  Listings in 2023 weeks {WEEK_MIN}-{WEEK_MAX}: {len(listings_2023):,}")
    print(f"  Balanced panel (both years): {len(balanced_listings):,}")

    # Filter to balanced panel + week window
    df = in_window[in_window["listing_city"].isin(balanced_listings)].copy()
    print(f"  Panel rows: {len(df):,}")

    # Relative week (0 = week 38)
    df["week_relative"] = (df["week_of_year"] - WEEK_MIN).astype(np.int8)

    print("[4/5] Panel summary...")
    for year in [2022, 2023]:
        yr_data = df[df["year"] == year]
        print(f"  {year}: {len(yr_data):,} rows, {yr_data['listing_city'].nunique():,} listings, "
              f"weeks {yr_data['week_of_year'].min()}-{yr_data['week_of_year'].max()}, "
              f"mean log_price={yr_data['log_price'].mean():.4f}")

    # City breakdown
    for city in sorted(df["city_slug"].unique()):
        cdata = df[df["city_slug"] == city]
        n22 = len(cdata[cdata["year"] == 2022])
        n23 = len(cdata[cdata["year"] == 2023])
        nl = cdata["listing_city"].nunique()
        print(f"  {city}: {nl:,} listings, {n22:,} obs (2022) + {n23:,} obs (2023)")

    print("[5/5] Saving DDD panel...")
    out_path = OUT_DIR / "ddd_panel.parquet"
    df.to_parquet(out_path, index=False, engine="pyarrow")
    print(f"  → {out_path} ({out_path.stat().st_size / 1e9:.2f} GB)")

    meta = {
        "n_obs": int(len(df)),
        "n_listings": int(len(balanced_listings)),
        "n_cities": int(df["city_slug"].nunique()),
        "week_range": [int(WEEK_MIN), int(WEEK_MAX)],
        "oct1_week": int(OCT1_WEEK),
        "obs_2022": int((df["year"] == 2022).sum()),
        "obs_2023": int((df["year"] == 2023).sum()),
        "mean_log_price_2022": round(float(df.loc[df["year"] == 2022, "log_price"].mean()), 6),
        "mean_log_price_2023": round(float(df.loc[df["year"] == 2023, "log_price"].mean()), 6),
    }
    (OUT_DIR / "ddd_panel_meta.json").write_text(json.dumps(meta, indent=2))
    print("Done.")


if __name__ == "__main__":
    main()
