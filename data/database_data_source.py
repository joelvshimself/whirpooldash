"""
Database data source implementation using PostgreSQL
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
from .data_source import DataSource
from .models import SessionLocal, User, PriceHistory, KPI, SKU
from sqlalchemy import func, desc
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class DatabaseDataSource(DataSource):
    """Database implementation of DataSource using PostgreSQL with SQLAlchemy"""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def get_kpis(self) -> Dict[str, Any]:
        """Returns KPI metrics from database"""
        latest_kpi = self.session.query(KPI).order_by(desc(KPI.date)).first()
        
        if latest_kpi:
            return {
                "todays_money": latest_kpi.todays_money,
                "todays_users": latest_kpi.todays_users,
                "money_change": latest_kpi.money_change,
                "users_change": latest_kpi.users_change
            }
        
        return {
            "todays_money": 0,
            "todays_users": 0,
            "money_change": 0,
            "users_change": 0
        }
    
    def get_sales_data(self) -> Dict[str, Any]:
        """Returns sales chart data aggregated from price history"""
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Aggregate price history by month
        current_year = datetime.now().year
        series1_data = []
        series2_data = []
        
        for month_idx in range(1, 13):
            # Count price predictions for this month
            count = self.session.query(func.count(PriceHistory.id)).filter(
                func.extract('year', PriceHistory.created_at) == current_year,
                func.extract('month', PriceHistory.created_at) == month_idx
            ).scalar()
            
            series1_data.append(count or 0)
            
            # Average price for this month
            avg_price = self.session.query(func.avg(PriceHistory.price)).filter(
                func.extract('year', PriceHistory.created_at) == current_year,
                func.extract('month', PriceHistory.created_at) == month_idx
            ).scalar()
            
            series2_data.append(int(avg_price) if avg_price else 0)
        
        return {
            "months": months,
            "values": [
                {"name": "Predictions", "data": series1_data},
                {"name": "Avg Price", "data": series2_data}
            ]
        }
    
    def get_active_users(self) -> Dict[str, Any]:
        """Returns active users metrics calculated from data"""
        # Count total users
        users_count = self.session.query(func.count(User.id)).scalar() or 0
        
        # Count total price predictions as "clicks"
        clicks_count = self.session.query(func.count(PriceHistory.id)).scalar() or 0
        
        # Sum total revenue from price history
        total_sales = self.session.query(func.sum(PriceHistory.price)).scalar() or 0
        
        # Count unique SKUs
        unique_skus = self.session.query(func.count(func.distinct(SKU.id))).scalar() or 0
        
        return {
            "users": users_count * 10000,  # Scale for display
            "clicks": clicks_count * 1000,
            "sales": int(total_sales / 100) if total_sales > 0 else 0,
            "items": unique_skus * 30
        }
    
    def get_sku_table(self) -> List[Dict[str, Any]]:
        """Returns SKU table data from database"""
        skus = self.session.query(SKU).limit(10).all()
        
        sku_data = []
        for sku in skus:
            sku_data.append({
                "company": sku.company,
                "icon": sku.icon,
                "members": sku.members,
                "budget": sku.budget if sku.budget else "Not set",
                "completion": sku.completion
            })
        
        return sku_data
    
    def get_price_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns price prediction history from database"""
        history = self.session.query(PriceHistory).order_by(
            desc(PriceHistory.created_at)
        ).limit(limit).all()
        
        history_data = []
        for record in history:
            history_data.append({
                "sku": record.sku,
                "region": record.region,
                "partner": record.partner,
                "release_date": record.release_date.isoformat(),
                "price": record.price
            })
        
        return history_data
    
    def add_price_prediction(self, sku: str, region: str, partner: str, price: float):
        """Add a new price prediction to history"""
        new_prediction = PriceHistory(
            sku=sku,
            region=region,
            partner=partner,
            release_date=datetime.now(),
            price=price
        )
        self.session.add(new_prediction)
        self.session.commit()
    
    def get_training_data(self, sku: str, region: str) -> List[Dict[str, Any]]:
        """Returns historical price data for LSTM training"""
        # Get last 100 records for this SKU/region
        training_records = self.session.query(PriceHistory).filter(
            PriceHistory.sku == sku,
            PriceHistory.region == region
        ).order_by(PriceHistory.created_at).limit(100).all()
        
        training_data = []
        for record in training_records:
            training_data.append({
                "date": record.created_at.isoformat(),
                "price": record.price,
                "sku": record.sku,
                "region": record.region
            })
        
        return training_data
    
    def __del__(self):
        """Close database session on cleanup"""
        if hasattr(self, 'session'):
            self.session.close()

