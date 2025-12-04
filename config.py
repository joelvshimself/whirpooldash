"""
Configuration file for Whirlpool Dashboard
"""
import os
from functools import lru_cache
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Data Source Configuration
DATA_SOURCE_TYPE = os.getenv("DATA_SOURCE_TYPE", "mock")  # "mock" or "database"
POSTGRES_CONNECTION_STRING = os.getenv(
    "POSTGRES_CONNECTION_STRING",
    "postgresql://postgres:postgres@streamlit-postgres.postgres.database.azure.com/postgres?sslmode=require"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Azure Blob Storage Configuration
AZURE_BLOB_BASE_URL = os.getenv(
    "AZURE_BLOB_BASE_URL", 
    "https://modelstoragest.blob.core.windows.net/models"
)
AZURE_BLOB_SAS_TOKEN = os.getenv(
    "AZURE_BLOB_SAS_TOKEN",
    "sp=r&st=2025-11-12T16:57:51Z&se=2026-09-17T01:12:51Z&sv=2024-11-04&sr=c&sig=YskSjKCiHsrn1CIJX9wQP8mH1oBVMNuUyAwjUR69M0Y%3D"
)

# Default Values
DEFAULT_PARTNERS = [
    "CHEDRAUI",
    "PALACIO DE HIERRO",
    "LIVERPOOL",
    "ELEKTRA",
    "HOME DEPOT",
    "SEARS",
    "WALMART",
]
DEFAULT_REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]

# Load SKUs from unique_skus.txt file
def load_skus_from_file(file_path: str = "unique_skus.txt") -> List[str]:
    """
    Load SKUs from a text file (one SKU per line).
    
    Args:
        file_path: Path to the SKU file (relative to project root)
    
    Returns:
        List of SKU strings
    """
    import os
    # Get the project root directory (where config.py is located)
    project_root = os.path.dirname(os.path.abspath(__file__))
    sku_file_path = os.path.join(project_root, file_path)
    
    try:
        with open(sku_file_path, 'r', encoding='utf-8') as f:
            skus = [line.strip() for line in f if line.strip()]
        return skus
    except FileNotFoundError:
        # Fallback to default SKUs if file not found
        return [
            "7KFCB519MPA"]


def get_sku_categories(skus: List[str]) -> Dict[str, str]:
    """
    Get categories for SKUs from the database.
    
    Args:
        skus: List of SKU strings
    
    Returns:
        Dictionary mapping SKU to category (or "Unknown" if not found)
    """
    try:
        from services.db import run_query
        import pandas as pd
        
        if not skus:
            return {}
        
        # Create a query to get unique SKU-Category pairs using parameterized query
        # Build placeholders for IN clause
        placeholders = ','.join([f':sku_{i}' for i in range(len(skus))])
        query = f"""
        SELECT DISTINCT "SKU", "CATEGORY"
        FROM iqsigma
        WHERE "SKU" IN ({placeholders})
        """
        
        # Create parameters dictionary
        params = {f'sku_{i}': sku for i, sku in enumerate(skus)}
        
        df = run_query(query, params=params)
        
        # Create dictionary mapping SKU to Category
        sku_category_map = {}
        if not df.empty:
            for _, row in df.iterrows():
                sku = str(row['SKU']).strip()
                category = str(row['CATEGORY']).strip() if pd.notna(row['CATEGORY']) else "Unknown"
                sku_category_map[sku] = category
        
        # Fill in missing SKUs with "Unknown"
        for sku in skus:
            if sku not in sku_category_map:
                sku_category_map[sku] = "Unknown"
        
        return sku_category_map
    except Exception as e:
        # If database query fails, return all as "Unknown"
        import warnings
        warnings.warn(f"Could not fetch SKU categories from database: {e}")
        return {sku: "Unknown" for sku in skus}


def get_skus_with_categories() -> Dict[str, str]:
    """
    Get SKUs with their categories for display in selectbox.
    
    Returns:
        Dictionary mapping display string (SKU - Category or just SKU) to SKU value
    """
    skus = load_skus_from_file("unique_skus.txt")
    categories = get_sku_categories(skus)
    
    # Create mapping: "SKU - Category" -> "SKU" (or just "SKU" if category is Unknown)
    sku_display_map = {}
    for sku in skus:
        category = categories.get(sku, "Unknown")
        # Only show category if it's not "Unknown"
        if category and category != "Unknown":
            display_text = f"{sku} - {category}"
        else:
            display_text = sku
        sku_display_map[display_text] = sku
    
    return sku_display_map


@lru_cache(maxsize=1)
def get_training_partners() -> List[str]:
    """
    Get distinct trading partners from sellout table, fallback to defaults.
    """
    try:
        from services.db import run_query

        query = """
        SELECT DISTINCT TRIM("TP") AS tp
        FROM sellout
        WHERE "TP" IS NOT NULL
          AND TRIM("TP") <> ''
        ORDER BY tp
        """
        df = run_query(query)
        if not df.empty and "tp" in df.columns:
            partners = [str(tp).strip() for tp in df["tp"].tolist() if str(tp).strip()]
            if partners:
                return partners
    except Exception as exc:
        import warnings
        warnings.warn(f"Could not fetch training partners from sellout: {exc}")

    return DEFAULT_PARTNERS


# Load SKUs from unique_skus.txt
DEFAULT_SKUS = load_skus_from_file("unique_skus.txt")

# Time Range Options
TIME_RANGE_OPTIONS = ["1 week", "2 weeks", "1 month", "3 months", "6 months", "1 year"]

# Chart Configuration
CHART_COLORS = {
    "primary": "#FF6B35",  # Orange
    "secondary": "#F7931E",  # Light orange
    "background": "#F5F5F5",
    "text": "#2D2D2D"
}

# UI Configuration
SIDEBAR_WIDTH = 250
MAIN_CONTENT_WIDTH = 900
CALCULATOR_WIDTH = 350

