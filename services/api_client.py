"""
API client for communicating with the backend
"""
import requests
from typing import Dict, Any, Optional
import config


class PriceCalculatorAPI:
    """Client for Price Calculator API"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.API_BASE_URL
    
    def calculate_price(self, sku: str, region: str, time_range: str, partner: str = "Walmart") -> Dict[str, Any]:
        """
        Calculate price prediction from LSTM backend
        
        Args:
            sku: SKU identifier
            region: Region identifier
            time_range: Time range for prediction
            partner: Partner name
            
        Returns:
            Dict with prediction results
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/predict",
                json={
                    "sku": sku,
                    "region": region,
                    "time_range": time_range,
                    "partner": partner
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Fallback to mock response if backend unavailable
            return self._mock_response(sku, region, time_range, partner)
    
    def get_history(self, limit: int = 10) -> list:
        """
        Get price prediction history
        
        Args:
            limit: Maximum number of records
            
        Returns:
            List of history records
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/history",
                params={"limit": limit},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Fallback to empty list if backend unavailable
            return []
    
    def _mock_response(self, sku: str, region: str, time_range: str, partner: str) -> Dict[str, Any]:
        """Fallback mock response if backend is unavailable"""
        import random
        return {
            "sku": sku,
            "region": region,
            "partner": partner,
            "price": round(random.uniform(100, 2000), 2),
            "release_date": "2024-01-15T10:30:00",
            "confidence": round(random.uniform(0.7, 0.95), 2)
        }

