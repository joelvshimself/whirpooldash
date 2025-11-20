"""
Mock data source implementation
Code doesn't know this is mock - it's just another DataSource implementation
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
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
    
    def get_sales_data(self, year: Optional[int] = None, quarter: Optional[int] = None) -> Dict[str, Any]:
        """Returns mock sales chart data for 5 brands"""
        all_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Define quarter month ranges (0-indexed)
        quarter_months = {
            1: (0, 3),   # Q1: Jan, Feb, Mar (indices 0-2)
            2: (3, 6),   # Q2: Apr, May, Jun (indices 3-5)
            3: (6, 9),   # Q3: Jul, Aug, Sep (indices 6-8)
            4: (9, 12)   # Q4: Oct, Nov, Dec (indices 9-11)
        }
        
        # Filter months based on year and quarter
        if year and quarter and quarter in quarter_months:
            start_idx, end_idx = quarter_months[quarter]
            months = all_months[start_idx:end_idx]
            month_indices = list(range(start_idx, end_idx))
        elif year:
            # Full year selected
            months = all_months
            month_indices = list(range(12))
        else:
            # Default: show all months
            months = all_months
            month_indices = list(range(12))
        
        # Generate 5 series for the line chart with varied patterns for brands
        # Create more realistic data with peaks and valleys
        base_values_full = [
            [120, 180, 250, 220, 200, 190, 210, 230, 200, 180, 160, 140],  # GE - peaks early
            [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260],  # LG - steady growth
            [200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310],  # MABE - higher steady
            [180, 200, 190, 210, 230, 220, 240, 250, 230, 210, 200, 190],  # MAYTAG - fluctuating
            [250, 280, 300, 320, 310, 290, 270, 250, 230, 210, 200, 180]   # WHIRLPOOL - declining
        ]
        
        brands = ["GE", "LG", "MABE", "MAYTAG", "WHIRLPOOL"]
        
        # Filter data based on selected months
        series_data = []
        for base in base_values_full:
            filtered_data = [base[i] for i in month_indices]
            # Add some randomness to make it more realistic
            series = [int(v + random.uniform(-15, 15)) for v in filtered_data]
            series_data.append(series)
        
        return {
            "months": months,
            "values": [
                {"name": brands[0], "data": series_data[0]},
                {"name": brands[1], "data": series_data[1]},
                {"name": brands[2], "data": series_data[2]},
                {"name": brands[3], "data": series_data[3]},
                {"name": brands[4], "data": series_data[4]}
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
    
    def get_brand_category_prices(self) -> Dict[str, Any]:
        """Returns price data by brand and category"""
        brands = ["MABE", "WHIRLPOOL", "GE", "MAYTAG", "LG", "HISENSE", "TEKA", "MIDEA", "PANASONIC", "SAMSUNG"]
        categories = ["RANGE HOOD", "RANGES", "REFRIGERATORS", "WASHING MACHINE", "WATER COOLERS", "WINE COOLERS"]
        
        # Generate realistic price data (in millions)
        # Base prices vary by category
        base_prices = {
            "RANGE HOOD": 500,
            "RANGES": 800,
            "REFRIGERATORS": 1200,
            "WASHING MACHINE": 900,
            "WATER COOLERS": 400,
            "WINE COOLERS": 600
        }
        
        # Brand multipliers (some brands are more expensive)
        brand_multipliers = {
            "MABE": 1.0,
            "WHIRLPOOL": 1.2,
            "GE": 1.15,
            "MAYTAG": 1.3,
            "LG": 1.1,
            "HISENSE": 0.9,
            "TEKA": 1.25,
            "MIDEA": 0.85,
            "PANASONIC": 1.05,
            "SAMSUNG": 1.15
        }
        
        data = []
        for brand in brands:
            for category in categories:
                # Some combinations might not have data (None)
                if random.random() > 0.15:  # 85% chance of having data
                    base = base_prices[category]
                    multiplier = brand_multipliers[brand]
                    price = base * multiplier * random.uniform(0.8, 1.2)  # Add some variation
                    data.append({
                        "brand": brand,
                        "category": category,
                        "price": round(price, 2)
                    })
                else:
                    data.append({
                        "brand": brand,
                        "category": category,
                        "price": None
                    })
        
        return {
            "brands": brands,
            "categories": categories,
            "data": data
        }
    
    def get_prediction_data(self, brand: Optional[str] = None) -> Dict[str, Any]:
        """Returns prediction data with historical and forecast values"""
        brands = ["GE", "LG", "MABE", "MAYTAG", "WHIRLPOOL"]
        
        # Historical months (past 9 months)
        historical_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
        # Prediction months (next 3 months)
        prediction_months = ["Oct", "Nov", "Dec"]
        all_months = historical_months + prediction_months
        
        # Base historical values for each brand
        base_historical = {
            "GE": [120, 180, 250, 220, 200, 190, 210, 230, 200],
            "LG": [150, 160, 170, 180, 190, 200, 210, 220, 230],
            "MABE": [200, 210, 220, 230, 240, 250, 260, 270, 280],
            "MAYTAG": [180, 200, 190, 210, 230, 220, 240, 250, 230],
            "WHIRLPOOL": [250, 280, 300, 320, 310, 290, 270, 250, 230]
        }
        
        historical_data = {}
        prediction_data = {}
        upper_bound_data = {}
        lower_bound_data = {}
        
        for brand_name in brands:
            if brand and brand_name != brand:
                continue
            
            # Historical values with some randomness
            hist_values = [int(v + random.uniform(-10, 10)) for v in base_historical[brand_name]]
            
            # Prediction: continue trend from last value
            last_value = hist_values[-1]
            trend = (hist_values[-1] - hist_values[-3]) / 2  # Average trend from last 3 months
            
            pred_values = []
            upper_values = []
            lower_values = []
            
            for i in range(3):  # 3 months prediction
                # Predicted value with trend
                pred_val = last_value + trend * (i + 1) + random.uniform(-5, 5)
                # Confidence interval: ±10% with some randomness
                confidence_width = pred_val * 0.1 + random.uniform(5, 15)
                upper_val = pred_val + confidence_width
                lower_val = pred_val - confidence_width
                
                pred_values.append(int(pred_val))
                upper_values.append(int(upper_val))
                lower_values.append(int(lower_val))
            
            historical_data[brand_name] = hist_values
            prediction_data[brand_name] = pred_values
            upper_bound_data[brand_name] = upper_values
            lower_bound_data[brand_name] = lower_values
        
        return {
            "months": all_months,
            "historical_months": historical_months,
            "prediction_months": prediction_months,
            "historical": historical_data,
            "prediction": prediction_data,
            "upper_bound": upper_bound_data,
            "lower_bound": lower_bound_data
        }

