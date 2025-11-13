"""
Azure Blob Storage service for loading ML models
"""
import requests
import pickle
from io import BytesIO
from typing import Dict, Any, Optional
import config


class AzureModelService:
    """Service for loading ML models from Azure Blob Storage"""
    
    def __init__(self):
        self.loaded_models: Dict[str, Any] = {}
        self.base_url = config.AZURE_BLOB_BASE_URL
        self.sas_token = config.AZURE_BLOB_SAS_TOKEN
    
    def get_model_url(self, partner: str) -> str:
        """
        Get the Azure Blob URL for a partner's model
        
        Args:
            partner: Training partner name
            
        Returns:
            Full URL with SAS token
        """
        model_filename = f"{partner.lower().replace(' ', '_')}_model.pkl"
        return f"{self.base_url}/{model_filename}?{self.sas_token}"
    
    def load_model(self, partner: str) -> Any:
        """
        Load ML model from Azure Blob Storage for a specific partner
        
        Args:
            partner: Training partner name
            
        Returns:
            Loaded model object
        """
        # Check if already loaded
        if partner in self.loaded_models:
            return self.loaded_models[partner]
        
        # Download and load model
        url = self.get_model_url(partner)
        
        response = requests.get(url)
        response.raise_for_status()
        
        model = pickle.load(BytesIO(response.content))
        
        # Cache the loaded model
        self.loaded_models[partner] = model
        
        return model
    
    def list_available_partners(self) -> list:
        """
        Get list of available training partners
        For now returns configured partners
        Could be enhanced to query Azure Blob Storage
        
        Returns:
            List of partner names
        """
        return config.DEFAULT_PARTNERS
    
    def clear_cache(self):
        """Clear cached models to free memory"""
        self.loaded_models.clear()
    
    def reload_model(self, partner: str) -> Any:
        """
        Force reload a model from Azure
        
        Args:
            partner: Training partner name
            
        Returns:
            Reloaded model object
        """
        if partner in self.loaded_models:
            del self.loaded_models[partner]
        return self.load_model(partner)

