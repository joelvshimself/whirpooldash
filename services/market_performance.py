"""
Market performance service helpers.
"""
from typing import Dict, Optional

import numpy as np
import pandas as pd

from .db import run_query

WHIRLPOOL_FAMILY = ("WHIRLPOOL", "ACROS", "MAYTAG", "KITCHENAID")

BRAND_YEARLY_SQL = """
SELECT
    EXTRACT(YEAR FROM "DATE"::date)::INT AS year,
    "BRAND" AS brand,
    SUM("PRICE_SOLD") AS sales,
    COUNT(*) AS units
FROM iqsigma
GROUP BY 1, 2
ORDER BY 1, 2;
"""

CATEGORY_BRAND_UNITS_SQL = """
SELECT
    "CATEGORY" AS category,
    "BRAND" AS brand,
    COUNT(*) AS units
FROM iqsigma
WHERE EXTRACT(YEAR FROM "DATE"::date)::INT = :year
GROUP BY 1, 2
ORDER BY 1, 2;
"""


def get_brand_yearly_stats() -> pd.DataFrame:
    """Return yearly sales/units per brand."""
    df = run_query(BRAND_YEARLY_SQL)
    if df.empty:
        return df
    df["year"] = df["year"].astype(int)
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    df["avg_price"] = df["sales"] / df["units"].replace({0: np.nan})
    return df


def get_category_brand_units(year: int) -> pd.DataFrame:
    """Return units per category and brand for a given year."""
    df = run_query(CATEGORY_BRAND_UNITS_SQL, params={"year": year})
    if df.empty:
        return df
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    return df


def _relative_change(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    if current is None or previous is None or previous == 0:
        return None
    return (current - previous) / previous


def compute_latest_year_kpis(brand_df: pd.DataFrame) -> Optional[Dict[str, Optional[float]]]:
    """Return KPI values plus helper metadata for charts."""
    if brand_df.empty:
        return None

    latest_year = int(brand_df["year"].max())
    latest_mask = brand_df["year"] == latest_year
    prev_mask = brand_df["year"] == (latest_year - 1)

    latest_df = brand_df[latest_mask]
    prev_df = brand_df[prev_mask]

    whirlpool_latest = latest_df[latest_df["brand"].isin(WHIRLPOOL_FAMILY)]
    whirlpool_prev = prev_df[prev_df["brand"].isin(WHIRLPOOL_FAMILY)]

    total_sales_latest = latest_df["sales"].sum()
    total_sales_prev = prev_df["sales"].sum() if not prev_df.empty else None

    whirlpool_sales_latest = whirlpool_latest["sales"].sum()
    whirlpool_sales_prev = whirlpool_prev["sales"].sum() if not whirlpool_prev.empty else None

    whirlpool_units_latest = whirlpool_latest["units"].sum()
    whirlpool_avg_price = None
    if whirlpool_units_latest and whirlpool_units_latest != 0:
        whirlpool_avg_price = whirlpool_sales_latest / whirlpool_units_latest

    market_share_latest = None
    if total_sales_latest:
        market_share_latest = whirlpool_sales_latest / total_sales_latest

    market_share_prev = None
    if total_sales_prev:
        market_share_prev = (whirlpool_sales_prev or 0) / total_sales_prev

    market_share_delta = (
        None if market_share_prev is None else market_share_latest - market_share_prev
    )
    whirlpool_sales_delta = _relative_change(whirlpool_sales_latest, whirlpool_sales_prev)

    competitor_sales = (
        latest_df.groupby("brand")["sales"].sum().sort_values(ascending=False)
    )
    whirlpool_total_vs_comp = float(whirlpool_sales_latest or 0.0)
    higher_competitors = competitor_sales.drop(
        labels=[b for b in competitor_sales.index if b in WHIRLPOOL_FAMILY],
        errors="ignore",
    )
    position = None
    if whirlpool_total_vs_comp > 0:
        position = int((higher_competitors > whirlpool_total_vs_comp).sum() + 1)

    top_brands_units = (
        latest_df.sort_values("units", ascending=False)["brand"]
        .drop_duplicates()
        .head(5)
        .tolist()
    )

    line_brands = sorted(
        set(top_brands_units).union(
            {brand for brand in WHIRLPOOL_FAMILY if brand in latest_df["brand"].unique()}
        )
    )

    return {
        "latest_year": latest_year,
        "previous_year": latest_year - 1 if not prev_df.empty else None,
        "market_share": market_share_latest,
        "market_share_prev": market_share_prev,
        "market_share_delta": market_share_delta,
        "whp_sales": whirlpool_sales_latest,
        "whp_sales_prev": whirlpool_sales_prev,
        "whp_sales_delta": whirlpool_sales_delta,
        "avg_price": whirlpool_avg_price,
        "position": position,
        "top_brands_units": top_brands_units,
        "line_brands": line_brands if line_brands else top_brands_units,
    }

