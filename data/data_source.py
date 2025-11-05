"""
Abstract base class for data sources
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime


class DataSource(ABC):
    """Abstract interface for data sources. Implementations should not be aware if data is mock or real."""
    
    @abstractmethod
    def get_kpis(self) -> Dict[str, Any]:
        """
        Returns KPI metrics for the dashboard.
        
        Returns:
            Dict with keys: 'todays_money', 'todays_users', 'money_change', 'users_change'
        """
        pass
    
    @abstractmethod
    def get_sales_data(self) -> Dict[str, Any]:
        """
        Returns sales chart data.
        
        Returns:
            Dict with 'months' (list) and 'values' (list of dicts with series data)
        """
        pass
    
    @abstractmethod
    def get_active_users(self) -> Dict[str, Any]:
        """
        Returns active users metrics.
        
        Returns:
            Dict with keys: 'users', 'clicks', 'sales', 'items'
        """
        pass
    
    @abstractmethod
    def get_sku_table(self) -> List[Dict[str, Any]]:
        """
        Returns SKU table data.
        
        Returns:
            List of dicts with keys: 'company', 'members', 'budget', 'completion', 'icon'
        """
        pass
    
    @abstractmethod
    def get_price_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returns price prediction history.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of dicts with keys: 'sku', 'region', 'partner', 'release_date', 'price'
        """
        pass
    
    @abstractmethod
    def get_training_data(self, sku: str, region: str) -> List[Dict[str, Any]]:
        """
        Returns historical price data for LSTM training.
        
        Args:
            sku: SKU identifier
            region: Region identifier
            
        Returns:
            List of dicts with historical price data
        """
        pass

