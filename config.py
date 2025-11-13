"""
Configuration file for Whirlpool Dashboard
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Data Source Configuration
DATA_SOURCE_TYPE = os.getenv("DATA_SOURCE_TYPE", "mock")  # "mock" or "database"

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
DEFAULT_PARTNERS = ["Walmart", "Target", "Best Buy", "Home Depot", "Lowes"]
DEFAULT_REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
DEFAULT_SKUS = [
    "WH-WF100A", "WH-WF200B", "WH-WF300C", "WH-WD400D", "WH-WD500E",
    "WH-RF600F", "WH-RF700G", "WH-MW800H", "WH-MW900I", "WH-DW100J"
]

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

