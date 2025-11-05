"""
LSTM model for price prediction
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from typing import List, Dict, Any, Optional
import os
from .data_processor import DataProcessor


class LSTMModel:
    """LSTM model for price prediction"""
    
    def __init__(self, sequence_length: int = 10):
        self.sequence_length = sequence_length
        self.model: Optional[keras.Model] = None
        self.processor = DataProcessor()
        self.model_path = "models/lstm_price_model.h5"
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create new one"""
        if os.path.exists(self.model_path):
            try:
                self.model = keras.models.load_model(self.model_path)
                print(f"Loaded existing model from {self.model_path}")
            except Exception as e:
                print(f"Error loading model: {e}. Creating new model.")
                self._create_model()
        else:
            self._create_model()
    
    def _create_model(self):
        """Create a new LSTM model architecture"""
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(self.sequence_length, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        print("Created new LSTM model")
    
    def train(self, training_data: List[Dict[str, Any]]):
        """
        Train the LSTM model
        
        Args:
            training_data: List of dicts with 'price', 'sku', 'region', 'date'
        """
        if not training_data:
            print("No training data provided")
            return
        
        # Extract SKUs and regions for encoding
        skus = [item['sku'] for item in training_data]
        regions = [item['region'] for item in training_data]
        self.processor.fit_encoders(skus, regions)
        
        # Prepare training data
        X, y = self.processor.prepare_training_data(training_data, self.sequence_length)
        
        if len(X) == 0:
            print("Not enough data to create sequences")
            return
        
        # Reshape for LSTM input (samples, timesteps, features)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        # Train model
        self.model.fit(X, y, batch_size=32, epochs=10, verbose=0, validation_split=0.2)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        print(f"Model trained and saved to {self.model_path}")
    
    def predict(self, sku: str, region: str, historical_prices: List[float]) -> float:
        """
        Predict price for given SKU and region
        
        Args:
            sku: SKU identifier
            region: Region identifier
            historical_prices: List of historical prices
            
        Returns:
            Predicted price
        """
        if self.model is None:
            raise ValueError("Model not initialized")
        
        if len(historical_prices) < self.sequence_length:
            # Use average if not enough history
            return np.mean(historical_prices) if historical_prices else 500.0
        
        # Prepare input
        X = self.processor.prepare_prediction_input(sku, region, historical_prices, self.sequence_length)
        
        # Predict
        scaled_prediction = self.model.predict(X, verbose=0)[0][0]
        
        # Inverse scale
        prediction = self.processor.inverse_scale_price(scaled_prediction)
        
        return float(prediction)

