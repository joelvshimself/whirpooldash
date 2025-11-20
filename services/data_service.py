"""
Data service layer - provides data source to all components
Uses abstraction - doesn't know if data is mock or real
"""
from typing import Optional
from data.data_source import DataSource
from data.mock_data_source import MockDataSource
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
        data_source_type = config.DATA_SOURCE_TYPE.lower() if config.DATA_SOURCE_TYPE else "mock"
        
        if data_source_type == "mock":
            self._data_source = MockDataSource()
        elif data_source_type == "database":
            # Future: from data.database_data_source import DatabaseDataSource
            # self._data_source = DatabaseDataSource()
            # Fallback to mock if database is not implemented
            import warnings
            warnings.warn("Database data source not yet implemented. Falling back to mock data source.")
            self._data_source = MockDataSource()
        else:
            # Unknown type, fallback to mock
            import warnings
            warnings.warn(f"Unknown data source type: {config.DATA_SOURCE_TYPE}. Falling back to mock data source.")
            self._data_source = MockDataSource()
    
    def get_data_source(self) -> DataSource:
        """Get the current data source instance"""
        return self._data_source
    
    def get_kpis(self):
        """Get KPI metrics"""
        return self._data_source.get_kpis()
    
    def get_sales_data(self, year: Optional[int] = None, quarter: Optional[int] = None):
        """Get sales chart data"""
        return self._data_source.get_sales_data(year=year, quarter=quarter)
    
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
    
    def get_brand_category_prices(self):
        """Get price data by brand and category"""
        return self._data_source.get_brand_category_prices()
    
    def get_prediction_data(self, brand: Optional[str] = None):
        """Get prediction data with historical and forecast values"""
        return self._data_source.get_prediction_data(brand=brand)

