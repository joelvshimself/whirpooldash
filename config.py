"""
Configuration file for Whirlpool Dashboard
"""
import os
from typing import List

# Data Source Configuration
DATA_SOURCE_TYPE = os.getenv("DATA_SOURCE_TYPE", "mock")  # "mock" or "database"

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_PORT = int(os.getenv("API_PORT", "8000"))

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

