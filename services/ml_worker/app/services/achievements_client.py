import httpx
import logging
from typing import Dict, List, Optional, Any
import asyncio

logger = logging.getLogger(__name__)

class AchievementsServiceClient:
    """Client for communicating with the achievements microservice"""
    
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    async def process_species_detection(self, detection_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process a species detection and trigger relevant achievements
        
        Args:
            detection_data: Dictionary containing:
                - user_id: int
                - species_detected: str (species code)
                - confidence: float
                - location: Optional[Dict] with latitude/longitude
        
        Returns:
            List of triggered achievements
        """
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/achievements/species-detection",
                    json=detection_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Successfully processed species detection for user {detection_data.get('user_id')}")
                    return result.get('achievements', [])
                else:
                    logger.warning(f"Achievements service returned {response.status_code}: {response.text}")
                    return []
                    
            except Exception as e:
                logger.error(f"Failed to communicate with achievements service: {e}")
                return []
    
    async def process_species_detection_batch(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple species detections in batch
        
        Args:
            detections: List of detection dictionaries
        
        Returns:
            Dictionary with batch processing results
        """
        
        async with httpx.AsyncClient(timeout=self.timeout * 2) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/achievements/species-detection/batch",
                    json={"detections": detections}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Successfully processed {len(detections)} species detections in batch")
                    return result
                else:
                    logger.warning(f"Batch achievements processing returned {response.status_code}: {response.text}")
                    return {"success": False, "error": response.text}
                    
            except Exception as e:
                logger.error(f"Failed to process batch achievements: {e}")
                return {"success": False, "error": str(e)}
    
    async def get_user_achievements(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all achievements for a user"""
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/users/{user_id}/achievements")
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Failed to get user achievements: {response.status_code}")
                    return []
                    
            except Exception as e:
                logger.error(f"Error getting user achievements: {e}")
                return []
    
    async def health_check(self) -> bool:
        """Check if the achievements service is healthy"""
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
            except Exception:
                return False


class SightingsServiceClient:
    """Client for communicating with the sightings microservice"""
    
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    async def create_sighting(self, sighting_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new sighting record
        
        Args:
            sighting_data: Dictionary containing:
                - user_id: int
                - species_code: str
                - species_name: str
                - confidence: float
                - latitude: Optional[float]
                - longitude: Optional[float]
                - recorded_at: str (ISO datetime)
        
        Returns:
            Created sighting data or None if failed
        """
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/sightings",
                    json=sighting_data
                )
                
                if response.status_code == 201:
                    result = response.json()
                    logger.info(f"Successfully created sighting for user {sighting_data.get('user_id')}")
                    return result
                else:
                    logger.warning(f"Sightings service returned {response.status_code}: {response.text}")
                    return None
                    
            except Exception as e:
                logger.error(f"Failed to create sighting: {e}")
                return None
    
    async def create_sightings_batch(self, sightings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple sightings in batch
        
        Args:
            sightings: List of sighting dictionaries
        
        Returns:
            Dictionary with batch creation results
        """
        
        async with httpx.AsyncClient(timeout=self.timeout * 2) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/sightings/batch",
                    json={"sightings": sightings}
                )
                
                if response.status_code == 201:
                    result = response.json()
                    logger.info(f"Successfully created {len(sightings)} sightings in batch")
                    return result
                else:
                    logger.warning(f"Batch sightings creation returned {response.status_code}: {response.text}")
                    return {"success": False, "error": response.text}
                    
            except Exception as e:
                logger.error(f"Failed to create batch sightings: {e}")
                return {"success": False, "error": str(e)}
    
    async def get_user_sightings(self, user_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Get sightings for a user"""
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/users/{user_id}/sightings?limit={limit}")
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Failed to get user sightings: {response.status_code}")
                    return []
                    
            except Exception as e:
                logger.error(f"Error getting user sightings: {e}")
                return []
    
    async def health_check(self) -> bool:
        """Check if the sightings service is healthy"""
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
            except Exception:
                return False