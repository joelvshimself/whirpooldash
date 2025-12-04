"""
Market Performance page component.
"""
from typing import Optional

import pandas as pd
import plotly.express as px
import streamlit as st

from services.market_performance import (
WHIRLPOOL_FAMILY,
    compute_latest_year_kpis,
    get_brand_yearly_stats,
    get_category_brand_units,
)
from utils.helpers import format_currency
from components.dashboard import render_kpi_chip


def _format_percentage(value: Optional[float], decimals: int = 1, with_sign: bool = False) -> str:
    """Format a decimal ratio as percentage text."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "N/A"
    pct = value * 100
    sign = ""
    if with_sign:
        sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.{decimals}f}%"


def _format_currency_or_na(value: Optional[float]) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "N/A"
    return format_currency(value)


def _delta_value_and_text(value: Optional[float], default_text: str) -> tuple[float, str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return 0.0, default_text
    return value, _format_percentage(value, decimals=1, with_sign=True)


def _render_kpis(kpis: dict) -> None:
    """Render the four KPI cards requested."""
    prev_label = (
        f"vs {kpis['previous_year']}" if kpis.get("previous_year") else "vs año previo"
    )
    
    share_delta_value, share_delta_text = _delta_value_and_text(
        kpis.get("market_share_delta"),
        f"{prev_label} N/A",
    )
    sales_delta_value, sales_delta_text = _delta_value_and_text(
        kpis.get("whp_sales_delta"),
        f"{prev_label} N/A",
    )
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        render_kpi_chip(
            label="% Whirlpool Market Share",
            value_text=_format_percentage(kpis.get("market_share")),
            delta_value=share_delta_value,
            delta_text=share_delta_text,
            icon_name="users",
        )
    
    with col2:
        render_kpi_chip(
            label="$ Whirlpool Sales",
            value_text=_format_currency_or_na(kpis.get("whp_sales")),
            delta_value=sales_delta_value,
            delta_text=sales_delta_text,
            icon_name="money",
        )
    
    with col3:
        render_kpi_chip(
            label="Average Price (Whirlpool)",
            value_text=_format_currency_or_na(kpis.get("avg_price")),
            delta_value=0.0,
            delta_text=f"{kpis['latest_year']}",
            icon_name="money",
        )
    
    with col4:
        position = kpis.get("position")
        position_text = f"#{int(position)}" if position else "N/A"
        render_kpi_chip(
            label="Whirlpool Position",
            value_text=position_text,
            delta_value=0.0,
            delta_text="vs competitors",
            icon_name="users",
        )


def _render_units_trend_chart(brand_df: pd.DataFrame, brands: list[str]) -> None:
    if not brands:
        st.info("No hay suficientes marcas para mostrar la tendencia de unidades.")
        return
    
    chart_df = brand_df[brand_df["brand"].isin(brands)].copy()
    if chart_df.empty:
        st.info("Sin datos de unidades para las marcas seleccionadas.")
        return
    
    chart_df = chart_df.sort_values("year")
    whirlpool_brands = [b for b in WHIRLPOOL_FAMILY if b in chart_df["brand"].unique()]
    orange_palette = ["#FF6B35", "#FF844C", "#FF9D63", "#FFB67A"]
    whirlpool_colors = {
        brand: orange_palette[i % len(orange_palette)]
        for i, brand in enumerate(whirlpool_brands)
    }
    competitor_palette = ["#C4C4C4", "#B0B0B0", "#9C9C9C", "#888888", "#747474"]
    color_map = {}
    competitor_idx = 0
    for brand in chart_df["brand"].unique():
        if brand in whirlpool_colors:
            color_map[brand] = whirlpool_colors[brand]
        else:
            color_map[brand] = competitor_palette[competitor_idx % len(competitor_palette)]
            competitor_idx += 1
    
    fig = px.line(
        chart_df,
        x="year",
        y="units",
        color="brand",
        markers=True,
        title="Units sold by brand",
        color_discrete_map=color_map,
    )
    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Año",
        yaxis_title="Unidades",
        hovermode="x unified",
        legend_title="Marca",
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.1)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.1)")
    st.plotly_chart(fig, use_container_width=True)


def _render_category_histogram(category_df: pd.DataFrame, top_brands: list[str], latest_year: int) -> None:
    if category_df.empty:
        st.info("No hay datos de categorías para el último año.")
        return
    
    filtered = category_df[category_df["brand"].isin(top_brands)].copy()
    if filtered.empty:
        st.info("Las 5 marcas principales no tienen datos por categoría.")
        return
    
    color_map = {
        brand: "#FF6B35" if brand in WHIRLPOOL_FAMILY else "#9CA3AF"
        for brand in filtered["brand"].unique()
    }
    
    fig = px.bar(
        filtered,
        x="category",
        y="units",
        color="brand",
        barmode="group",
        title=f"Top 5 brands by category · {latest_year}",
        color_discrete_map=color_map,
    )
    fig.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Categoría",
        yaxis_title="Unidades",
        legend_title="Marca",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.1)")
    st.plotly_chart(fig, use_container_width=True)


def render_market_performance(
    brand_df: Optional[pd.DataFrame] = None,
    category_df: Optional[pd.DataFrame] = None,
) -> None:
    """Public entry point for the Market Performance page."""
    st.title("Market Performance")
    st.header("Home Appliances - Market Overview")
    
    local_brand_df = brand_df
    if local_brand_df is None:
        try:
            local_brand_df = get_brand_yearly_stats()
        except Exception as exc:
            st.error(f"No se pudieron cargar las métricas de mercado: {exc}")
            return
    
    if local_brand_df.empty:
        st.info("No hay datos disponibles en la tabla iqsigma.")
        return
    
    kpis = compute_latest_year_kpis(local_brand_df)
    if not kpis:
        st.info("No hay KPIs disponibles para mostrar.")
        return
    
    local_category_df = category_df
    if local_category_df is None:
        local_category_df = get_category_brand_units(kpis["latest_year"])
    
    _render_kpis(kpis)
    st.markdown("---")
    _render_units_trend_chart(local_brand_df, kpis.get("line_brands", []))
    st.markdown("---")
    _render_category_histogram(local_category_df, kpis.get("top_brands_units", []), kpis["latest_year"])

