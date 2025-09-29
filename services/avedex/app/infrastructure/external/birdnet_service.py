"""
BirdNet integration service for species identification.
"""

import httpx
import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class BirdNetService:
    """Service for integrating with BirdNet ML worker."""
    
    def __init__(self):
        self.ml_worker_url = os.getenv("ML_WORKER_URL", "http://ml_worker:8003")
        self.timeout = 30.0
    
    async def identify_species(
        self, 
        audio_url: str, 
        location_lat: Optional[float] = None,
        location_lng: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Identify bird species from audio using BirdNet.
        
        Args:
            audio_url: URL to the audio file
            location_lat: Latitude for location-based filtering
            location_lng: Longitude for location-based filtering
            
        Returns:
            Dictionary with identification results or None if failed
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "audio_url": audio_url
                }
                
                if location_lat is not None and location_lng is not None:
                    payload["location"] = {
                        "lat": location_lat,
                        "lng": location_lng
                    }
                
                response = await client.post(
                    f"{self.ml_worker_url}/api/v1/identify",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"BirdNet identification successful: {result}")
                    return result
                else:
                    logger.error(f"BirdNet identification failed: {response.status_code} - {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("BirdNet identification timed out")
            return None
        except Exception as e:
            logger.error(f"Error calling BirdNet service: {e}")
            return None
    
    async def get_species_info(self, scientific_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed species information from BirdNet.
        
        Args:
            scientific_name: Scientific name of the species
            
        Returns:
            Dictionary with species information or None if not found
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.ml_worker_url}/api/v1/species/{scientific_name}"
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Species info retrieved: {scientific_name}")
                    return result
                elif response.status_code == 404:
                    logger.warning(f"Species not found: {scientific_name}")
                    return None
                else:
                    logger.error(f"Error getting species info: {response.status_code} - {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("Species info request timed out")
            return None
        except Exception as e:
            logger.error(f"Error calling BirdNet service for species info: {e}")
            return None
    
    async def health_check(self) -> bool:
        """
        Check if BirdNet ML worker is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.ml_worker_url}/health")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"BirdNet health check failed: {e}")
            return False
    
    def parse_identification_result(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse BirdNet identification result into standardized format.
        
        Args:
            result: Raw result from BirdNet
            
        Returns:
            Parsed result with standardized fields
        """
        if not result or "predictions" not in result:
            return None
        
        predictions = result["predictions"]
        if not predictions:
            return None
        
        # Get the top prediction
        top_prediction = predictions[0]
        
        return {
            "scientific_name": top_prediction.get("scientific_name"),
            "common_name": top_prediction.get("common_name"),
            "confidence_score": top_prediction.get("confidence", 0.0),
            "all_predictions": predictions[:5],  # Top 5 predictions
            "processing_time": result.get("processing_time"),
            "model_version": result.get("model_version")
        }