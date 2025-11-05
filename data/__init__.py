"""
Data source abstraction layer
"""
from .data_source import DataSource
from .mock_data_source import MockDataSource

__all__ = ["DataSource", "MockDataSource"]

