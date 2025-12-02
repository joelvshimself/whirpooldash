"""
Sellout KPIs service - provides KPI metrics from the sellout table
"""
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from .db import run_query


def get_sellout_kpis() -> Dict[str, Any]:
    """
    Get sellout KPIs from the database.
    
    Returns:
        Dict with keys:
        - articles_this_year: Total QTY for current year
        - sales_this_year: Total QTY * Real_price for current year
        - articles_delta: Percentage change in QTY vs previous year
        - sales_delta: Percentage change in GROSS_SALES vs previous year
    """
    current_year = datetime.now().year
    previous_year = current_year - 1
    
    # Query 1: Total articles sold this year (sum of QTY)
    articles_query = """
    SELECT COALESCE(SUM("QTY"), 0) AS total_qty
    FROM sellout
    WHERE EXTRACT(YEAR FROM "DATE"::date) = :current_year;
    """
    
    # Query 2: Total sales this year (sum of QTY * Real_price)
    sales_query = """
    SELECT COALESCE(SUM("QTY" * "Real_price"), 0) AS total_sales
    FROM sellout
    WHERE EXTRACT(YEAR FROM "DATE"::date) = :current_year;
    """
    
    # Query 3: Articles delta (QTY comparison between years)
    articles_delta_query = """
    WITH current_year_data AS (
        SELECT COALESCE(SUM("QTY"), 0) AS qty
        FROM sellout
        WHERE EXTRACT(YEAR FROM "DATE"::date) = :current_year
    ),
    previous_year_data AS (
        SELECT COALESCE(SUM("QTY"), 0) AS qty
        FROM sellout
        WHERE EXTRACT(YEAR FROM "DATE"::date) = :previous_year
    )
    SELECT 
        c.qty AS current_qty,
        p.qty AS previous_qty,
        CASE 
            WHEN p.qty = 0 THEN NULL
            ELSE ((c.qty - p.qty)::float / p.qty::float) * 100
        END AS delta_percentage
    FROM current_year_data c
    CROSS JOIN previous_year_data p;
    """
    
    # Query 4: Sales delta (GROSS_SALES comparison between years)
    sales_delta_query = """
    WITH current_year_data AS (
        SELECT COALESCE(SUM("GROSS_SALES"), 0) AS sales
        FROM sellout
        WHERE EXTRACT(YEAR FROM "DATE"::date) = :current_year
    ),
    previous_year_data AS (
        SELECT COALESCE(SUM("GROSS_SALES"), 0) AS sales
        FROM sellout
        WHERE EXTRACT(YEAR FROM "DATE"::date) = :previous_year
    )
    SELECT 
        c.sales AS current_sales,
        p.sales AS previous_sales,
        CASE 
            WHEN p.sales = 0 THEN NULL
            ELSE ((c.sales - p.sales)::float / p.sales::float) * 100
        END AS delta_percentage
    FROM current_year_data c
    CROSS JOIN previous_year_data p;
    """
    
    try:
        # Execute queries
        articles_df = run_query(articles_query, {"current_year": current_year})
        sales_df = run_query(sales_query, {"current_year": current_year})
        articles_delta_df = run_query(
            articles_delta_query, 
            {"current_year": current_year, "previous_year": previous_year}
        )
        sales_delta_df = run_query(
            sales_delta_query,
            {"current_year": current_year, "previous_year": previous_year}
        )
        
        # Extract values
        articles_this_year = int(articles_df.iloc[0]["total_qty"]) if not articles_df.empty else 0
        sales_this_year = float(sales_df.iloc[0]["total_sales"]) if not sales_df.empty else 0.0
        
        # Extract delta values (absolute differences and percentages)
        if not articles_delta_df.empty:
            current_qty = float(articles_delta_df.iloc[0]["current_qty"])
            previous_qty = float(articles_delta_df.iloc[0]["previous_qty"])
            articles_delta_absolute = current_qty - previous_qty
            if articles_delta_df.iloc[0]["delta_percentage"] is not None:
                articles_delta_percentage = float(articles_delta_df.iloc[0]["delta_percentage"])
            else:
                articles_delta_percentage = 0.0
        else:
            articles_delta_absolute = 0
            articles_delta_percentage = 0.0
        
        if not sales_delta_df.empty:
            current_sales = float(sales_delta_df.iloc[0]["current_sales"])
            previous_sales = float(sales_delta_df.iloc[0]["previous_sales"])
            sales_delta_absolute = current_sales - previous_sales
            if sales_delta_df.iloc[0]["delta_percentage"] is not None:
                sales_delta_percentage = float(sales_delta_df.iloc[0]["delta_percentage"])
            else:
                sales_delta_percentage = 0.0
        else:
            sales_delta_absolute = 0.0
            sales_delta_percentage = 0.0
        
        return {
            "articles_this_year": articles_this_year,
            "sales_this_year": sales_this_year,
            "articles_delta_absolute": articles_delta_absolute,
            "articles_delta_percentage": articles_delta_percentage,
            "sales_delta_absolute": sales_delta_absolute,
            "sales_delta_percentage": sales_delta_percentage,
            "current_year": current_year,
            "previous_year": previous_year
        }
        
    except Exception as e:
        # Return default values on error
        return {
            "articles_this_year": 0,
            "sales_this_year": 0.0,
            "articles_delta_absolute": 0,
            "articles_delta_percentage": 0.0,
            "sales_delta_absolute": 0.0,
            "sales_delta_percentage": 0.0,
            "current_year": current_year,
            "previous_year": previous_year,
            "error": str(e)
        }

