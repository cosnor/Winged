import httpx
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio

from ..services.achievements_client import AchievementsServiceClient, SightingsServiceClient
from ..models.species_mapping import get_species_info

logger = logging.getLogger(__name__)

class BirdNetServiceClient:
    """Client for communicating with BirdNet HTTP API service"""
    
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def health_check(self) -> bool:
        """Check if BirdNet API service is healthy"""
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
            except Exception as e:
                logger.error(f"BirdNet API health check failed: {e}")
                return False
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data from BirdNet API
        
        Args:
            session_id: The session ID to retrieve
            
        Returns:
            Session data dictionary or None if not found
        """
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/sessions/{session_id}")
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(f"Session {session_id} not found in BirdNet API")
                    return None
                else:
                    logger.error(f"BirdNet API returned {response.status_code} for session {session_id}")
                    return None
                    
            except Exception as e:
                logger.error(f"Failed to get session {session_id} from BirdNet API: {e}")
                return None
    
    async def get_recent_sessions(self, limit: int = 10, hours_back: int = 24) -> List[Dict[str, Any]]:
        """
        Get recent sessions from BirdNet API
        
        Args:
            limit: Maximum number of sessions to retrieve
            hours_back: How many hours back to look
            
        Returns:
            List of session dictionaries
        """
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = {
                    "limit": limit,
                    "hours_back": hours_back
                }
                
                response = await client.get(f"{self.base_url}/sessions/recent", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("sessions", [])
                else:
                    logger.error(f"BirdNet API returned {response.status_code} for recent sessions")
                    return []
                    
            except Exception as e:
                logger.error(f"Failed to get recent sessions from BirdNet API: {e}")
                return []
    
    async def get_session_detections(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get detections for a specific session
        
        Args:
            session_id: The session ID
            
        Returns:
            List of detection dictionaries
        """
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/sessions/{session_id}/detections")
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("detections", [])
                else:
                    logger.error(f"BirdNet API returned {response.status_code} for session {session_id} detections")
                    return []
                    
            except Exception as e:
                logger.error(f"Failed to get detections for session {session_id}: {e}")
                return []
    
    async def get_user_sessions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get sessions for a specific user
        
        Args:
            user_id: The BirdNet user ID
            limit: Maximum number of sessions
            
        Returns:
            List of session dictionaries
        """
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = {"limit": limit}
                response = await client.get(f"{self.base_url}/users/{user_id}/sessions", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("sessions", [])
                else:
                    logger.error(f"BirdNet API returned {response.status_code} for user {user_id} sessions")
                    return []
                    
            except Exception as e:
                logger.error(f"Failed to get sessions for user {user_id}: {e}")
                return []


class BirdNetToWingedIntegrator:
    """Integrates BirdNet session data with Winged achievements and sightings"""
    
    def __init__(self, achievements_client: AchievementsServiceClient, sightings_client: SightingsServiceClient):
        self.achievements_client = achievements_client
        self.sightings_client = sightings_client
    
    async def process_birdnet_session(self, session_data: Dict[str, Any], default_user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Process a BirdNet session and create corresponding Winged records
        
        Args:
            session_data: BirdNet session data
            default_user_id: Default Winged user ID if no mapping exists
            
        Returns:
            Dictionary with processing results
        """
        
        session_id = session_data.get("session_id", "unknown")
        birdnet_user_id = session_data.get("user_id")
        detections = session_data.get("detections", [])
        
        if not detections:
            return {
                "session_id": session_id,
                "success": False,
                "error": "No detections in session"
            }
        
        # Map BirdNet user to Winged user (this would typically involve a user mapping service)
        winged_user_id = self._map_birdnet_user_to_winged(birdnet_user_id, default_user_id)
        
        if not winged_user_id:
            return {
                "session_id": session_id,
                "success": False,
                "error": "Could not map BirdNet user to Winged user"
            }
        
        # Process detections
        sightings_created = []
        achievements_triggered = []
        errors = []
        
        for detection in detections:
            try:
                # Create sighting
                sighting_result = await self._create_sighting_from_detection(
                    detection, winged_user_id, session_data
                )
                
                if sighting_result:
                    sightings_created.append(sighting_result)
                    
                    # Process achievements for this detection
                    achievement_result = await self._process_achievements_for_detection(
                        detection, winged_user_id, session_data
                    )
                    
                    if achievement_result:
                        achievements_triggered.extend(achievement_result)
                
            except Exception as e:
                logger.error(f"Error processing detection in session {session_id}: {e}")
                errors.append(str(e))
        
        return {
            "session_id": session_id,
            "success": True,
            "winged_user_id": winged_user_id,
            "birdnet_user_id": birdnet_user_id,
            "sightings_created": len(sightings_created),
            "achievements_triggered": len(achievements_triggered),
            "unique_species_detected": len(set(d.get("species_code", "") for d in detections)),
            "errors": errors
        }
    
    async def _create_sighting_from_detection(self, detection: Dict[str, Any], user_id: int, session_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a Winged sighting from a BirdNet detection"""
        
        species_code = detection.get("species_code")
        if not species_code:
            return None
        
        # Get enhanced species information
        species_info = get_species_info(species_code)
        
        sighting_data = {
            "user_id": user_id,
            "species_code": species_code,
            "species_name": species_info.get("common_name", detection.get("species_name", "Unknown")),
            "confidence": detection.get("confidence", 0.0),
            "latitude": detection.get("latitude") or session_data.get("latitude"),
            "longitude": detection.get("longitude") or session_data.get("longitude"),
            "recorded_at": detection.get("timestamp") or session_data.get("created_at", datetime.utcnow().isoformat()),
            "detection_metadata": {
                "birdnet_session_id": session_data.get("session_id"),
                "start_time": detection.get("start_time"),
                "end_time": detection.get("end_time"),
                "scientific_name": species_info.get("scientific_name"),
                "family": species_info.get("family"),
                "source": "birdnet_api"
            }
        }
        
        return await self.sightings_client.create_sighting(sighting_data)
    
    async def _process_achievements_for_detection(self, detection: Dict[str, Any], user_id: int, session_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process achievements for a BirdNet detection"""
        
        species_code = detection.get("species_code")
        if not species_code:
            return []
        
        # Get species information for achievement processing
        species_info = get_species_info(species_code)
        
        achievement_data = {
            "user_id": user_id,
            "species_detected": species_code,
            "confidence": detection.get("confidence", 0.0),
            "location": {
                "latitude": detection.get("latitude") or session_data.get("latitude"),
                "longitude": detection.get("longitude") or session_data.get("longitude")
            } if (detection.get("latitude") or session_data.get("latitude")) else None,
            "detection_metadata": {
                "family": species_info.get("family"),
                "conservation_status": species_info.get("conservation_status"),
                "endemic_to_colombia": species_info.get("endemic_to_colombia", False),
                "migration": species_info.get("migration"),
                "source": "birdnet_api",
                "session_id": session_data.get("session_id")
            }
        }
        
        return await self.achievements_client.process_species_detection(achievement_data)
    
    def _map_birdnet_user_to_winged(self, birdnet_user_id: Optional[str], default_user_id: Optional[int]) -> Optional[int]:
        """
        Map BirdNet user ID to Winged user ID
        
        In a real implementation, this would:
        1. Query a user mapping database
        2. Use OAuth connections
        3. Use email matching
        4. Fall back to default user
        
        For now, we use the default user or a simple mapping
        """
        
        if not birdnet_user_id and default_user_id:
            return default_user_id
        
        # Simple mapping logic (in production, this would be more sophisticated)
        if birdnet_user_id:
            # Try to extract numeric ID or use hash
            try:
                # If birdnet_user_id is numeric, use it directly
                return int(birdnet_user_id)
            except ValueError:
                # If not numeric, use hash-based mapping or default
                if default_user_id:
                    return default_user_id
                # Use a simple hash-based mapping as fallback
                return hash(birdnet_user_id) % 10000 + 1
        
        return default_user_id
    
    async def process_multiple_sessions(self, sessions: List[Dict[str, Any]], default_user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Process multiple BirdNet sessions in batch
        
        Args:
            sessions: List of BirdNet session data
            default_user_id: Default Winged user ID
            
        Returns:
            Dictionary with batch processing results
        """
        
        results = []
        total_sightings = 0
        total_achievements = 0
        total_errors = 0
        
        for session in sessions:
            try:
                result = await self.process_birdnet_session(session, default_user_id)
                results.append(result)
                
                if result.get("success"):
                    total_sightings += result.get("sightings_created", 0)
                    total_achievements += result.get("achievements_triggered", 0)
                
                total_errors += len(result.get("errors", []))
                
            except Exception as e:
                logger.error(f"Failed to process session {session.get('session_id', 'unknown')}: {e}")
                results.append({
                    "session_id": session.get("session_id", "unknown"),
                    "success": False,
                    "error": str(e)
                })
                total_errors += 1
        
        return {
            "sessions_processed": len(sessions),
            "successful_sessions": sum(1 for r in results if r.get("success")),
            "total_sightings_created": total_sightings,
            "total_achievements_triggered": total_achievements,
            "total_errors": total_errors,
            "results": results
        }