import motor.motor_asyncio
import pymongo
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import asyncio

from ..services.achievements_client import AchievementsServiceClient, SightingsServiceClient
from ..models.species_mapping import get_species_info

logger = logging.getLogger(__name__)

class BirdNetDatabaseClient:
    """Client for direct MongoDB database access to BirdNet data"""
    
    def __init__(self, mongodb_url: str, database_name: str, sessions_collection: str = "sessions", detections_collection: str = "detections"):
        self.mongodb_url = mongodb_url
        self.database_name = database_name
        self.sessions_collection_name = sessions_collection
        self.detections_collection_name = detections_collection
        self.client = None
        self.db = None
        self.sessions_collection = None
        self.detections_collection = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongodb_url)
            self.db = self.client[self.database_name]
            self.sessions_collection = self.db[self.sessions_collection_name]
            self.detections_collection = self.db[self.detections_collection_name]
            
            # Test connection
            await self.client.admin.command('ismaster')
            logger.info(f"Connected to BirdNet MongoDB database: {self.database_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to BirdNet MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from BirdNet MongoDB")
    
    async def is_connected(self) -> bool:
        """Check if connected to MongoDB"""
        try:
            if self.client:
                await self.client.admin.command('ismaster')
                return True
            return False
        except Exception:
            return False
    
    async def get_recent_sessions(self, limit: int = 10, hours_back: int = 24) -> List[Dict[str, Any]]:
        """
        Get recent sessions from the database
        
        Args:
            limit: Maximum number of sessions to return
            hours_back: How many hours back to look
            
        Returns:
            List of session documents
        """
        
        if not self.sessions_collection:
            raise RuntimeError("Not connected to database")
        
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
            
            cursor = self.sessions_collection.find(
                {"created_at": {"$gte": cutoff_time}}
            ).sort("created_at", -1).limit(limit)
            
            sessions = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string for JSON serialization
            for session in sessions:
                if "_id" in session:
                    session["_id"] = str(session["_id"])
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting recent sessions: {e}")
            return []
    
    async def get_session_with_detections(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a session with its detections
        
        Args:
            session_id: The session ID to retrieve
            
        Returns:
            Dictionary with session and detections data
        """
        
        if not self.sessions_collection or not self.detections_collection:
            raise RuntimeError("Not connected to database")
        
        try:
            # Get session
            session = await self.sessions_collection.find_one({"session_id": session_id})
            
            if not session:
                return None
            
            # Convert ObjectId to string
            if "_id" in session:
                session["_id"] = str(session["_id"])
            
            # Get detections for this session
            cursor = self.detections_collection.find({"session_id": session_id})
            detections = await cursor.to_list(length=None)
            
            # Convert ObjectIds to strings
            for detection in detections:
                if "_id" in detection:
                    detection["_id"] = str(detection["_id"])
            
            return {
                "session": session,
                "detections": detections
            }
            
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {e}")
            return None
    
    async def get_user_sessions(self, user_id: str, limit: int = 50, processed_only: bool = False) -> List[Dict[str, Any]]:
        """
        Get sessions for a specific user
        
        Args:
            user_id: The BirdNet user ID
            limit: Maximum number of sessions
            processed_only: If True, only return already processed sessions
            
        Returns:
            List of session documents
        """
        
        if not self.sessions_collection:
            raise RuntimeError("Not connected to database")
        
        try:
            query = {"user_id": user_id}
            
            if processed_only:
                query["winged_processed"] = True
            
            cursor = self.sessions_collection.find(query).sort("created_at", -1).limit(limit)
            sessions = await cursor.to_list(length=limit)
            
            # Convert ObjectIds to strings
            for session in sessions:
                if "_id" in session:
                    session["_id"] = str(session["_id"])
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting sessions for user {user_id}: {e}")
            return []
    
    async def mark_session_processed(self, session_id: str, winged_data: Dict[str, Any] = None):
        """
        Mark a session as processed by Winged
        
        Args:
            session_id: The session ID
            winged_data: Optional data about the Winged processing
        """
        
        if not self.sessions_collection:
            raise RuntimeError("Not connected to database")
        
        try:
            update_data = {
                "winged_processed": True,
                "winged_processed_at": datetime.utcnow()
            }
            
            if winged_data:
                update_data["winged_data"] = winged_data
            
            result = await self.sessions_collection.update_one(
                {"session_id": session_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"Marked session {session_id} as processed")
            else:
                logger.warning(f"No session found with ID {session_id} to mark as processed")
            
        except Exception as e:
            logger.error(f"Error marking session {session_id} as processed: {e}")


class BirdNetDataSyncer:
    """Syncs BirdNet database data with Winged achievements and sightings"""
    
    def __init__(self, database_client: BirdNetDatabaseClient, achievements_client: AchievementsServiceClient, sightings_client: SightingsServiceClient):
        self.db_client = database_client
        self.achievements_client = achievements_client
        self.sightings_client = sightings_client
    
    async def get_unprocessed_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get sessions that haven't been processed by Winged yet
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of unprocessed session documents
        """
        
        if not self.db_client.sessions_collection:
            raise RuntimeError("Database not connected")
        
        try:
            # Find sessions that haven't been processed by Winged
            cursor = self.db_client.sessions_collection.find(
                {"$or": [
                    {"winged_processed": {"$exists": False}},
                    {"winged_processed": False}
                ]}
            ).sort("created_at", 1).limit(limit)  # Oldest first
            
            sessions = await cursor.to_list(length=limit)
            
            # Convert ObjectIds and add summary statistics
            for session in sessions:
                if "_id" in session:
                    session["_id"] = str(session["_id"])
                
                # Add detection count for this session
                session_id = session.get("session_id")
                if session_id:
                    detection_count = await self.db_client.detections_collection.count_documents(
                        {"session_id": session_id}
                    )
                    session["total_detections"] = detection_count
                    
                    # Get unique species count
                    species_pipeline = [
                        {"$match": {"session_id": session_id}},
                        {"$group": {"_id": "$species_code"}},
                        {"$count": "unique_species"}
                    ]
                    
                    species_result = await self.db_client.detections_collection.aggregate(species_pipeline).to_list(1)
                    session["unique_species"] = species_result[0]["unique_species"] if species_result else 0
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting unprocessed sessions: {e}")
            return []
    
    async def get_unprocessed_sessions_count(self) -> int:
        """Get count of unprocessed sessions"""
        
        if not self.db_client.sessions_collection:
            return 0
        
        try:
            count = await self.db_client.sessions_collection.count_documents(
                {"$or": [
                    {"winged_processed": {"$exists": False}},
                    {"winged_processed": False}
                ]}
            )
            return count
            
        except Exception as e:
            logger.error(f"Error getting unprocessed sessions count: {e}")
            return 0
    
    async def sync_unprocessed_sessions(self, limit: int = 50, min_confidence: float = 0.7, default_user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Sync unprocessed sessions with Winged
        
        Args:
            limit: Maximum number of sessions to process
            min_confidence: Minimum confidence threshold for detections
            default_user_id: Default Winged user ID for unmapped BirdNet users
            
        Returns:
            Dictionary with sync results
        """
        
        try:
            # Get unprocessed sessions
            sessions = await self.get_unprocessed_sessions(limit)
            
            if not sessions:
                return {
                    "sessions_found": 0,
                    "sessions_processed": 0,
                    "total_sightings_created": 0,
                    "unique_species_detected": 0,
                    "species_list": [],
                    "errors": []
                }
            
            # Process each session
            total_sightings = 0
            species_detected = set()
            errors = []
            sessions_processed = 0
            
            for session in sessions:
                try:
                    result = await self._process_single_session(session, min_confidence, default_user_id)
                    
                    if result["success"]:
                        sessions_processed += 1
                        total_sightings += result["sightings_created"]
                        species_detected.update(result["species_detected"])
                        
                        # Mark session as processed
                        await self.db_client.mark_session_processed(
                            session["session_id"],
                            {
                                "sightings_created": result["sightings_created"],
                                "species_detected": list(result["species_detected"]),
                                "winged_user_id": result["winged_user_id"]
                            }
                        )
                    else:
                        errors.append({
                            "session_id": session["session_id"],
                            "error": result["error"]
                        })
                
                except Exception as e:
                    logger.error(f"Error processing session {session.get('session_id', 'unknown')}: {e}")
                    errors.append({
                        "session_id": session.get("session_id", "unknown"),
                        "error": str(e)
                    })
            
            return {
                "sessions_found": len(sessions),
                "sessions_processed": sessions_processed,
                "total_sightings_created": total_sightings,
                "unique_species_detected": len(species_detected),
                "species_list": list(species_detected),
                "errors": errors
            }
            
        except Exception as e:
            logger.error(f"Error in sync_unprocessed_sessions: {e}")
            return {
                "sessions_found": 0,
                "sessions_processed": 0,
                "error": str(e)
            }
    
    async def sync_user_sessions(self, birdnet_user_id: str, winged_user_id: int, limit: int = 50, min_confidence: float = 0.7) -> Dict[str, Any]:
        """
        Sync sessions for a specific user
        
        Args:
            birdnet_user_id: BirdNet user ID
            winged_user_id: Corresponding Winged user ID
            limit: Maximum number of sessions to process
            min_confidence: Minimum confidence threshold
            
        Returns:
            Dictionary with sync results
        """
        
        try:
            # Get user's unprocessed sessions
            all_sessions = await self.db_client.get_user_sessions(birdnet_user_id, limit * 2)
            unprocessed_sessions = [s for s in all_sessions if not s.get("winged_processed", False)][:limit]
            
            if not unprocessed_sessions:
                return {
                    "birdnet_user_id": birdnet_user_id,
                    "winged_user_id": winged_user_id,
                    "sessions_processed": 0,
                    "total_sightings_created": 0,
                    "unique_species_detected": 0,
                    "message": "No unprocessed sessions found for user"
                }
            
            # Process sessions
            total_sightings = 0
            species_detected = set()
            sessions_processed = 0
            errors = []
            
            for session in unprocessed_sessions:
                try:
                    result = await self._process_single_session(session, min_confidence, winged_user_id)
                    
                    if result["success"]:
                        sessions_processed += 1
                        total_sightings += result["sightings_created"]
                        species_detected.update(result["species_detected"])
                        
                        # Mark as processed
                        await self.db_client.mark_session_processed(
                            session["session_id"],
                            {
                                "sightings_created": result["sightings_created"],
                                "species_detected": list(result["species_detected"]),
                                "winged_user_id": winged_user_id
                            }
                        )
                    else:
                        errors.append(result["error"])
                
                except Exception as e:
                    logger.error(f"Error processing user session: {e}")
                    errors.append(str(e))
            
            return {
                "birdnet_user_id": birdnet_user_id,
                "winged_user_id": winged_user_id,
                "sessions_processed": sessions_processed,
                "total_sightings_created": total_sightings,
                "unique_species_detected": len(species_detected),
                "species_list": list(species_detected),
                "errors": errors
            }
            
        except Exception as e:
            logger.error(f"Error syncing user {birdnet_user_id} sessions: {e}")
            return {
                "birdnet_user_id": birdnet_user_id,
                "winged_user_id": winged_user_id,
                "error": str(e)
            }
    
    async def _process_single_session(self, session: Dict[str, Any], min_confidence: float, default_user_id: Optional[int]) -> Dict[str, Any]:
        """Process a single session"""
        
        session_id = session.get("session_id")
        if not session_id:
            return {"success": False, "error": "No session_id"}
        
        # Get session detections
        session_data = await self.db_client.get_session_with_detections(session_id)
        
        if not session_data or not session_data.get("detections"):
            return {"success": False, "error": "No detections found"}
        
        detections = session_data["detections"]
        
        # Filter detections by confidence
        high_confidence_detections = [
            d for d in detections 
            if d.get("confidence", 0) >= min_confidence
        ]
        
        if not high_confidence_detections:
            return {"success": False, "error": "No high-confidence detections"}
        
        # Determine Winged user ID
        birdnet_user_id = session.get("user_id")
        winged_user_id = self._map_user_id(birdnet_user_id, default_user_id)
        
        if not winged_user_id:
            return {"success": False, "error": "Could not map user ID"}
        
        # Create sightings and process achievements
        sightings_created = 0
        species_detected = set()
        
        for detection in high_confidence_detections:
            species_code = detection.get("species_code")
            if not species_code:
                continue
            
            # Create sighting
            sighting_result = await self._create_sighting_from_detection(detection, winged_user_id, session)
            if sighting_result:
                sightings_created += 1
                species_detected.add(species_code)
                
                # Process achievement
                await self._process_achievement_for_detection(detection, winged_user_id, session)
        
        return {
            "success": True,
            "session_id": session_id,
            "winged_user_id": winged_user_id,
            "sightings_created": sightings_created,
            "species_detected": list(species_detected)
        }
    
    async def _create_sighting_from_detection(self, detection: Dict[str, Any], user_id: int, session: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a sighting from a detection"""
        
        species_code = detection.get("species_code")
        if not species_code:
            return None
        
        species_info = get_species_info(species_code)
        
        sighting_data = {
            "user_id": user_id,
            "species_code": species_code,
            "species_name": species_info.get("common_name", detection.get("species_name", "Unknown")),
            "confidence": detection.get("confidence", 0.0),
            "latitude": detection.get("latitude") or session.get("latitude"),
            "longitude": detection.get("longitude") or session.get("longitude"),
            "recorded_at": detection.get("recorded_at") or session.get("created_at", datetime.utcnow().isoformat()),
            "detection_metadata": {
                "birdnet_session_id": session.get("session_id"),
                "start_time": detection.get("start_time"),
                "end_time": detection.get("end_time"),
                "scientific_name": species_info.get("scientific_name"),
                "family": species_info.get("family"),
                "source": "birdnet_database"
            }
        }
        
        return await self.sightings_client.create_sighting(sighting_data)
    
    async def _process_achievement_for_detection(self, detection: Dict[str, Any], user_id: int, session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process achievements for a detection"""
        
        species_code = detection.get("species_code")
        if not species_code:
            return []
        
        species_info = get_species_info(species_code)
        
        achievement_data = {
            "user_id": user_id,
            "species_detected": species_code,
            "confidence": detection.get("confidence", 0.0),
            "location": {
                "latitude": detection.get("latitude") or session.get("latitude"),
                "longitude": detection.get("longitude") or session.get("longitude")
            } if (detection.get("latitude") or session.get("latitude")) else None,
            "detection_metadata": {
                "family": species_info.get("family"),
                "conservation_status": species_info.get("conservation_status"),
                "endemic_to_colombia": species_info.get("endemic_to_colombia", False),
                "migration": species_info.get("migration"),
                "source": "birdnet_database",
                "session_id": session.get("session_id")
            }
        }
        
        return await self.achievements_client.process_species_detection(achievement_data)
    
    def _map_user_id(self, birdnet_user_id: Optional[str], default_user_id: Optional[int]) -> Optional[int]:
        """Map BirdNet user ID to Winged user ID"""
        
        # In production, this would involve a proper user mapping service
        if default_user_id:
            return default_user_id
        
        if birdnet_user_id:
            try:
                return int(birdnet_user_id)
            except ValueError:
                # Use hash-based mapping
                return hash(birdnet_user_id) % 10000 + 1
        
        return None
    
    async def get_species_statistics(self, days_back: int = 7) -> Dict[str, Any]:
        """
        Get species detection statistics from the database
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            Dictionary with species statistics
        """
        
        if not self.db_client.detections_collection:
            return {"error": "Database not connected"}
        
        try:
            cutoff_time = datetime.utcnow() - timedelta(days=days_back)
            
            # Aggregation pipeline for species statistics
            pipeline = [
                {
                    "$match": {
                        "recorded_at": {"$gte": cutoff_time}
                    }
                },
                {
                    "$group": {
                        "_id": "$species_code",
                        "detection_count": {"$sum": 1},
                        "avg_confidence": {"$avg": "$confidence"},
                        "max_confidence": {"$max": "$confidence"},
                        "session_count": {"$addToSet": "$session_id"}
                    }
                },
                {
                    "$project": {
                        "species_code": "$_id",
                        "detection_count": 1,
                        "avg_confidence": {"$round": ["$avg_confidence", 3]},
                        "max_confidence": {"$round": ["$max_confidence", 3]},
                        "session_count": {"$size": "$session_count"},
                        "_id": 0
                    }
                },
                {
                    "$sort": {"detection_count": -1}
                }
            ]
            
            species_stats = await self.db_client.detections_collection.aggregate(pipeline).to_list(None)
            
            # Add species names
            for stat in species_stats:
                species_code = stat["species_code"]
                species_info = get_species_info(species_code)
                stat["species_name"] = species_info.get("common_name", f"Unknown ({species_code})")
                stat["family"] = species_info.get("family", "Unknown")
            
            return {
                "period_days": days_back,
                "total_species": len(species_stats),
                "species_stats": species_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting species statistics: {e}")
            return {"error": str(e)}