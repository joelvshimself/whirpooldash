"""
Data service layer - provides data source to all components
Uses abstraction - doesn't know if data is mock or real
"""
from typing import Optional
from data.data_source import DataSource
from data.mock_data_source import MockDataSource
from data.database_data_source import DatabaseDataSource
import config


class DataService:
    """Singleton service that provides data source instance"""
    
    _instance: Optional['DataService'] = None
    _data_source: Optional[DataSource] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._data_source is None:
            self._initialize_data_source()
    
    def _initialize_data_source(self):
        """Initialize the appropriate data source based on configuration"""
        if config.DATA_SOURCE_TYPE == "mock":
            self._data_source = MockDataSource()
        elif config.DATA_SOURCE_TYPE == "database":
            self._data_source = DatabaseDataSource()
        else:
            raise ValueError(f"Unknown data source type: {config.DATA_SOURCE_TYPE}")
    
    def get_data_source(self) -> DataSource:
        """Get the current data source instance"""
        return self._data_source
    
    def get_kpis(self):
        """Get KPI metrics"""
        return self._data_source.get_kpis()
    
    def get_sales_data(self):
        """Get sales chart data"""
        return self._data_source.get_sales_data()
    
    def get_active_users(self):
        """Get active users metrics"""
        return self._data_source.get_active_users()
    
    def get_sku_table(self):
        """Get SKU table data"""
        return self._data_source.get_sku_table()
    
    def get_price_history(self, limit: int = 10):
        """Get price prediction history"""
        return self._data_source.get_price_history(limit)
    
    def get_training_data(self, sku: str, region: str):
        """Get training data for LSTM"""
        return self._data_source.get_training_data(sku, region)

