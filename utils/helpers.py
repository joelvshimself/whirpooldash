"""
Helper utility functions
"""
from typing import Any
import streamlit as st


def format_currency(value: float) -> str:
    """Format value as currency"""
    return f"${value:,.0f}"


def format_number(value: int) -> str:
    """Format large numbers with suffixes"""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}m"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}k"
    return str(value)


def format_percentage(value: float) -> str:
    """Format value as percentage"""
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.0f}%"

