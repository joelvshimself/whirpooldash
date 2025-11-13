"""
FastAPI backend server for price prediction
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from services.data_service import DataService
from services.azure_model_service import AzureModelService
from ml.lstm_model import LSTMModel
import config

app = FastAPI(title="Whirlpool Price Prediction API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_service = DataService()
azure_model_service = AzureModelService()
lstm_model = LSTMModel()  # Fallback model


class PredictionRequest(BaseModel):
    sku: str
    region: str
    time_range: str
    partner: str = "Walmart"


class PredictionResponse(BaseModel):
    sku: str
    region: str
    partner: str
    price: float
    release_date: str
    confidence: float = 0.85


@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Whirlpool Price Prediction API"}


@app.post("/api/predict", response_model=PredictionResponse)
def predict_price(request: PredictionRequest):
    """
    Predict price using partner-specific LSTM model from Azure
    
    Args:
        request: Prediction request with SKU, region, time_range, partner
        
    Returns:
        Prediction response with price and metadata
    """
    try:
        # Get training data for this SKU/region
        training_data = data_service.get_training_data(request.sku, request.region)
        
        if not training_data:
            raise HTTPException(status_code=404, detail="No training data available")
        
        # Extract historical prices
        historical_prices = [item['price'] for item in training_data]
        
        # Try to load partner-specific model from Azure
        predicted_price = None
        try:
            partner_model = azure_model_service.load_model(request.partner)
            
            # Use the loaded model for prediction
            if hasattr(partner_model, 'predict'):
                predicted_price = partner_model.predict(request.sku, request.region, historical_prices)
            else:
                # If model doesn't have predict method, use fallback
                predicted_price = lstm_model.predict(request.sku, request.region, historical_prices)
        except Exception as azure_error:
            # Fallback to local LSTM model if Azure model fails
            if len(historical_prices) >= 10:
                lstm_model.train(training_data)
            predicted_price = lstm_model.predict(request.sku, request.region, historical_prices)
        
        # Add to history
        if hasattr(data_service.get_data_source(), 'add_price_prediction'):
            data_service.get_data_source().add_price_prediction(
                request.sku,
                request.region,
                request.partner,
                predicted_price
            )
        
        return PredictionResponse(
            sku=request.sku,
            region=request.region,
            partner=request.partner,
            price=round(predicted_price, 2),
            release_date=training_data[-1]['date'] if training_data else "2024-01-15T10:30:00",
            confidence=0.85
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
def get_history(limit: int = 10):
    """
    Get price prediction history
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of prediction history records
    """
    try:
        history = data_service.get_price_history(limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/partners")
def get_available_partners():
    """
    Get list of available training partners with models
    
    Returns:
        List of partner names
    """
    try:
        partners = azure_model_service.list_available_partners()
        return {"partners": partners}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reload-model")
def reload_partner_model(partner: str):
    """
    Reload a partner's model from Azure (clears cache)
    
    Args:
        partner: Partner name
        
    Returns:
        Reload status
    """
    try:
        azure_model_service.reload_model(partner)
        return {"status": "success", "message": f"Model for {partner} reloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/train")
def train_model(sku: Optional[str] = None, region: Optional[str] = None):
    """
    Train/retrain local fallback LSTM model
    
    Args:
        sku: Optional SKU to train on
        region: Optional region to train on
        
    Returns:
        Training status
    """
    try:
        if sku and region:
            training_data = data_service.get_training_data(sku, region)
            lstm_model.train(training_data)
            return {"status": "success", "message": f"Model trained on {sku}/{region}"}
        else:
            return {"status": "success", "message": "Model training initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_server():
    """Run the FastAPI server"""
    uvicorn.run(app, host="0.0.0.0", port=config.API_PORT)


if __name__ == "__main__":
    run_server()

