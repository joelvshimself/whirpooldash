"""
Mock data source implementation
Code doesn't know this is mock - it's just another DataSource implementation
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from .data_source import DataSource
import sys
import os

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class MockDataSource(DataSource):
    """Mock implementation of DataSource - generates realistic sample data"""
    
    def __init__(self):
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize mock data structures"""
        self._price_history = []
        self._generate_initial_history()
    
    def _generate_initial_history(self):
        """Generate initial price history"""
        partners = config.DEFAULT_PARTNERS
        regions = config.DEFAULT_REGIONS
        skus = config.DEFAULT_SKUS
        
        for _ in range(20):
            self._price_history.append({
                "sku": random.choice(skus),
                "region": random.choice(regions),
                "partner": random.choice(partners),
                "release_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "price": round(random.uniform(100, 2000), 2)
            })
    
    def get_kpis(self) -> Dict[str, Any]:
        """Returns mock KPI metrics"""
        return {
            "todays_money": 53000,
            "todays_users": 2300,
            "money_change": 55,
            "users_change": 5
        }
    
    def get_sales_data(self) -> Dict[str, Any]:
        """Returns mock sales chart data"""
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Generate two series for the area chart
        series1 = [random.randint(100, 350) for _ in range(12)]
        series2 = [random.randint(150, 400) for _ in range(12)]
        
        return {
            "months": months,
            "values": [
                {"name": "Series 1", "data": series1},
                {"name": "Series 2", "data": series2}
            ]
        }
    
    def get_active_users(self) -> Dict[str, Any]:
        """Returns mock active users metrics"""
        return {
            "users": 32984,
            "clicks": 2420000,  # 2.42m
            "sales": 2400,
            "items": 320
        }
    
    def get_sku_table(self) -> List[Dict[str, Any]]:
        """Returns mock SKU table data"""
        companies = [
            {"name": "Xd Chakra Soft UI Version", "icon": "🎨"},
            {"name": "Add Progress Track", "icon": "📊"},
            {"name": "Fix Platform Errors", "icon": "🔧"},
            {"name": "Launch our Mobile App", "icon": "📱"},
            {"name": "Add the New Pricing Page", "icon": "💎"},
            {"name": "Redesign New Online Shop", "icon": "🛒"},
            {"name": "Optimize Dashboard", "icon": "📈"},
            {"name": "Update API Endpoints", "icon": "🔌"},
            {"name": "Enhance Security", "icon": "🔒"},
            {"name": "Improve Performance", "icon": "⚡"}
        ]
        
        budgets = [14000, 3000, None, 32000, 400, 7600, 12000, 5000, 8500, 9000]
        completions = [60, 10, 100, 100, 25, 40, 75, 50, 30, 90]
        
        sku_data = []
        for i, company in enumerate(companies):
            member_count = random.randint(1, 4)
            sku_data.append({
                "company": company["name"],
                "icon": company["icon"],
                "members": member_count,
                "budget": budgets[i] if budgets[i] else "Not set",
                "completion": completions[i]
            })
        
        return sku_data
    
    def get_price_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns price prediction history"""
        return sorted(self._price_history, key=lambda x: x["release_date"], reverse=True)[:limit]
    
    def add_price_prediction(self, sku: str, region: str, partner: str, price: float):
        """Add a new price prediction to history"""
        self._price_history.insert(0, {
            "sku": sku,
            "region": region,
            "partner": partner,
            "release_date": datetime.now().isoformat(),
            "price": price
        })
    
    def get_training_data(self, sku: str, region: str) -> List[Dict[str, Any]]:
        """Returns mock historical price data for LSTM training"""
        # Generate 100 days of historical data
        training_data = []
        base_price = random.uniform(100, 500)
        
        for i in range(100):
            date = datetime.now() - timedelta(days=100-i)
            # Add some trend and noise
            price = base_price + (i * 0.5) + random.uniform(-20, 20)
            training_data.append({
                "date": date.isoformat(),
                "price": round(price, 2),
                "sku": sku,
                "region": region
            })
        
        return training_data

