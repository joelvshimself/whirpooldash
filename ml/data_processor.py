"""
Data preprocessing for LSTM model
"""
import numpy as np
from typing import List, Dict, Any
from sklearn.preprocessing import MinMaxScaler


class DataProcessor:
    """Processes data for LSTM training and prediction"""
    
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.sku_encoder = {}
        self.region_encoder = {}
        self._encoder_fitted = False
    
    def encode_sku(self, sku: str) -> int:
        """Encode SKU string to integer"""
        if not self._encoder_fitted:
            raise ValueError("Encoder must be fitted before encoding")
        return self.sku_encoder.get(sku, 0)
    
    def encode_region(self, region: str) -> int:
        """Encode region string to integer"""
        if not self._encoder_fitted:
            raise ValueError("Encoder must be fitted before encoding")
        return self.region_encoder.get(region, 0)
    
    def fit_encoders(self, skus: List[str], regions: List[str]):
        """Fit encoders with unique SKUs and regions"""
        unique_skus = sorted(set(skus))
        unique_regions = sorted(set(regions))
        
        self.sku_encoder = {sku: idx for idx, sku in enumerate(unique_skus)}
        self.region_encoder = {region: idx for idx, region in enumerate(unique_regions)}
        self._encoder_fitted = True
    
    def prepare_training_data(self, training_data: List[Dict[str, Any]], sequence_length: int = 10) -> tuple:
        """
        Prepare training data for LSTM
        
        Args:
            training_data: List of dicts with 'price', 'sku', 'region'
            sequence_length: Length of input sequences
            
        Returns:
            (X, y) tuple of numpy arrays
        """
        if not training_data:
            raise ValueError("Training data cannot be empty")
        
        # Extract prices
        prices = [item['price'] for item in training_data]
        
        # Fit scaler
        prices_array = np.array(prices).reshape(-1, 1)
        scaled_prices = self.scaler.fit_transform(prices_array)
        
        # Create sequences
        X, y = [], []
        for i in range(sequence_length, len(scaled_prices)):
            X.append(scaled_prices[i-sequence_length:i, 0])
            y.append(scaled_prices[i, 0])
        
        return np.array(X), np.array(y)
    
    def scale_price(self, price: float) -> float:
        """Scale a single price value"""
        return self.scaler.transform([[price]])[0][0]
    
    def inverse_scale_price(self, scaled_price: float) -> float:
        """Inverse scale a price value"""
        return self.scaler.inverse_transform([[scaled_price]])[0][0]
    
    def prepare_prediction_input(self, sku: str, region: str, historical_prices: List[float], sequence_length: int = 10) -> np.ndarray:
        """
        Prepare input for prediction
        
        Args:
            sku: SKU identifier
            region: Region identifier
            historical_prices: List of historical prices
            sequence_length: Length of input sequence
            
        Returns:
            Prepared input array
        """
        if len(historical_prices) < sequence_length:
            # Pad with last value if not enough history
            historical_prices = [historical_prices[0]] * (sequence_length - len(historical_prices)) + historical_prices
        
        # Scale prices
        prices_array = np.array(historical_prices[-sequence_length:]).reshape(-1, 1)
        scaled_prices = self.scaler.transform(prices_array)
        
        return scaled_prices.reshape(1, sequence_length, 1)

