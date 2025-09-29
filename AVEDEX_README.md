# Avedex Microservice - Bird Species Album

## Overview
Avedex is a gamified bird species identification and collection microservice that provides:
- **Species Management**: CRUD operations for bird species data
- **User Collections**: Personal bird discovery tracking
- **Gamification**: Achievement system with points and progress tracking
- **BirdNet Integration**: AI-powered bird identification from audio
- **Collections System**: Curated species collections (Endemic Birds, Garden Birds, etc.)

## Features Implemented

### ✅ Core Functionality
- **Species Database**: 9 Caribbean bird species with complete metadata
- **User Collections**: Track discovered species with location, confidence, and notes
- **Achievement System**: 15 achievements across 6 categories (Discovery, Streak, Rarity, etc.)
- **Progress Tracking**: Collection completion percentages and user statistics
- **Search & Filter**: Find species by name, rarity level, or other criteria
- **BirdNet Integration**: Ready for audio-based bird identification

### 🎮 Gamification Elements
- **Rarity Points**: 10-200 points based on species rarity (Common → Legendary)
- **Achievement Tiers**: Bronze, Silver, Gold with progressive requirements
- **Collection Progress**: Track completion of curated species collections
- **Statistics**: Accuracy rates, verification rates, discovery counts

### 🏗️ Architecture
- **Clean Architecture**: Domain-driven design with clear separation of concerns
- **Async Database**: SQLite with aiosqlite for development, PostgreSQL for production
- **FastAPI**: Modern async Python web framework
- **Type Safety**: Comprehensive Pydantic schemas and type hints

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Species Management
- `GET /api/v1/species/` - List all species
- `GET /api/v1/species/{id}` - Get specific species
- `GET /api/v1/species/search?query={term}` - Search species
- `GET /api/v1/species/rarity/{level}` - Filter by rarity level

### User Collections
- `POST /api/v1/species/users/{user_id}/collection` - Add species to user collection
- `GET /api/v1/species/users/{user_id}/collection` - Get user's discovered species
- `GET /api/v1/species/users/{user_id}/stats` - User statistics

### Collections System
- `GET /api/v1/species/collections/` - List all collections
- `GET /api/v1/species/collections/{id}` - Get collection with species
- `GET /api/v1/species/users/{user_id}/collections/{id}/progress` - Collection progress

### Achievements
- `GET /api/v1/achievements/` - List all achievements

### BirdNet Integration
- `POST /api/v1/species/users/{user_id}/identify` - Identify bird from audio

## Deployment

### Using Docker Compose (Recommended)
```bash
# Extract the archive
tar -xzf avedex-microservice.tar.gz

# Start the services
docker-compose up -d avedex db

# The service will be available at http://localhost:8007
```

### Standalone Development
```bash
# Navigate to the service directory
cd services/avedex

# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Variables

### Production (PostgreSQL)
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
ML_WORKER_URL=http://ml-worker:8003
ENVIRONMENT=production
```

### Development (SQLite)
```env
DATABASE_URL=sqlite+aiosqlite:///./avedex.db
ML_WORKER_URL=http://localhost:8003
ENVIRONMENT=development
```

## Database Schema

### Core Tables
- **species**: Bird species with metadata (scientific name, rarity, points, etc.)
- **user_species**: User's discovered species with location and confidence
- **collections**: Curated species collections
- **collection_species**: Many-to-many relationship between collections and species
- **achievements**: Achievement definitions with requirements
- **user_achievements**: User's earned achievements
- **user_progress**: Progress tracking for various metrics

## Sample Data

The service comes pre-seeded with:
- **9 Caribbean Bird Species**: From common (American Robin) to legendary (Black-capped Petrel)
- **5 System Collections**: Endemic Birds, Garden Birds, Endangered Species, Forest Dwellers, Seabirds
- **15 Achievements**: Covering discovery, streaks, rarity finds, collections, expertise, and locations

## Testing

### API Testing Examples
```bash
# Health check
curl http://localhost:8007/health

# List all species
curl http://localhost:8007/api/v1/species/

# Add species to user collection
curl -X POST http://localhost:8007/api/v1/species/users/test_user/collection \
  -H "Content-Type: application/json" \
  -d '{
    "species_id": 1,
    "location_lat": 18.2208,
    "location_lng": -66.5901,
    "location_name": "San Juan, Puerto Rico",
    "confidence_score": 0.95,
    "notes": "Beautiful robin spotted in the park"
  }'

# Check collection progress
curl http://localhost:8007/api/v1/species/users/test_user/collections/1/progress
```

## Known Issues

1. **Statistics Endpoint**: Temporarily commented out due to circular import issues
2. **BirdNet Integration**: Requires actual ML Worker service for audio processing

## Future Enhancements

- [ ] Fix circular import issues for statistics endpoint
- [ ] Implement photo upload and storage
- [ ] Add social features (sharing discoveries)
- [ ] Implement user-created collections
- [ ] Add more achievement types
- [ ] Implement leaderboards
- [ ] Add push notifications for achievements

## Technical Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0+ with async support
- **Validation**: Pydantic v2
- **Testing**: pytest with async support
- **Containerization**: Docker with multi-stage builds
- **Database**: PostgreSQL (production) / SQLite (development)

## Support

For issues or questions, please refer to the main Winged project repository.