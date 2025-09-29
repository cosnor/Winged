# Avedex - Species Album Service

Avedex is a microservice for storing, visualizing, and gamifying bird species identified through BirdNet in the Winged birdwatching app. It provides a comprehensive species album system with gamification features to encourage bird discovery and identification.

## Features

### 🦜 Species Management
- **Species Database**: Comprehensive database of Caribbean bird species with detailed information
- **User Collections**: Personal species albums for each user
- **Discovery Tracking**: Track when and where species were discovered
- **Rarity System**: Species categorized by rarity levels (Common, Uncommon, Rare, Very Rare, Legendary)

### 🎮 Gamification
- **Achievement System**: Unlock achievements for various milestones
- **Progress Tracking**: Monitor user progress and statistics
- **Leaderboards**: Compete with other birdwatchers
- **Streak System**: Maintain daily discovery streaks
- **Points System**: Earn points based on species rarity and achievements

### 🔗 BirdNet Integration
- **Automatic Identification**: Identify species from audio recordings using BirdNet
- **Confidence Scoring**: Track identification confidence levels
- **Location-based Filtering**: Improve accuracy with location data

### 📊 Collections & Visualization
- **Themed Collections**: System-defined collections (Endemic Birds, Endangered Species, etc.)
- **Progress Tracking**: Monitor completion of collections
- **Statistics**: Comprehensive user statistics and analytics

## Architecture

The service follows Clean Architecture principles with clear separation of concerns:

```
app/
├── domain/                 # Business logic and entities
│   ├── entities/          # Domain entities (Species, Achievement, etc.)
│   ├── repositories/      # Repository interfaces
│   └── services/          # Domain services
├── application/           # Application layer
│   ├── dtos/             # Data Transfer Objects
│   └── use_cases/        # Application use cases
├── infrastructure/        # External concerns
│   ├── database/         # Database models and repositories
│   └── external/         # External service integrations
└── presentation/          # API layer
    ├── api/              # FastAPI routers
    └── schemas/          # Pydantic schemas
```

## API Endpoints

### Species Management
- `GET /api/v1/species/` - Get all species
- `GET /api/v1/species/search` - Search species
- `GET /api/v1/species/{species_id}` - Get species details
- `POST /api/v1/species/users/{user_id}/collection` - Add species to user collection
- `GET /api/v1/species/users/{user_id}/collection` - Get user's collection
- `POST /api/v1/species/users/{user_id}/identify` - Identify species using BirdNet

### Collections
- `GET /api/v1/species/collections/` - Get all collections
- `GET /api/v1/species/collections/{collection_id}` - Get collection details
- `GET /api/v1/species/users/{user_id}/collections/{collection_id}/progress` - Get user's collection progress

### Achievements & Gamification
- `GET /api/v1/achievements/` - Get available achievements
- `GET /api/v1/achievements/users/{user_id}` - Get user achievements
- `GET /api/v1/achievements/users/{user_id}/progress` - Get achievement progress
- `GET /api/v1/achievements/users/{user_id}/statistics` - Get user statistics
- `GET /api/v1/achievements/leaderboard/` - Get leaderboard

## Database Schema

### Core Tables
- **species**: Bird species information
- **user_species**: User's discovered species
- **collections**: Themed species collections
- **achievements**: Available achievements
- **user_achievements**: User's unlocked achievements
- **user_progress**: User's overall progress and statistics

## Setup & Development

### Prerequisites
- Python 3.11+
- PostgreSQL with PostGIS extension
- Docker & Docker Compose

### Environment Variables
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/winged_avedex
ML_WORKER_URL=http://ml_worker:8003
ENVIRONMENT=development
```

### Running with Docker
```bash
# From the root Winged directory
docker-compose up avedex
```

### Local Development
```bash
cd services/avedex

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage_db.py create

# Run the service
python -m app.main
```

### Database Management
```bash
# Create tables and seed data
python manage_db.py create

# Reset database (drop and recreate)
python manage_db.py reset

# Seed data only
python manage_db.py seed
```

## Sample Data

The service includes seed data with:
- **9 Caribbean bird species** across all rarity levels
- **5 themed collections** (Endemic Birds, Common Garden Birds, etc.)
- **15 achievements** covering discovery, streaks, rarity, collections, and expertise

### Featured Species
- **Common**: American Robin, Greater Antillean Grackle, Bananaquit
- **Uncommon**: Puerto Rican Tody, Puerto Rican Spindalis
- **Rare**: Puerto Rican Parrot, Puerto Rican Tanager
- **Very Rare**: Clapper Rail
- **Legendary**: Black-capped Petrel

## Gamification System

### Achievement Types
- **Discovery**: First species, milestone discoveries
- **Streak**: Daily/weekly discovery streaks
- **Rarity**: Discovering rare species
- **Collection**: Completing themed collections
- **Expertise**: High-confidence identifications
- **Location**: Geographic exploration

### Point System
- Common species: 10 points
- Uncommon species: 25 points
- Rare species: 50 points
- Very rare species: 100 points
- Legendary species: 200 points
- Achievement bonuses based on tier (Bronze to Diamond)

## Integration with Other Services

### BirdNet ML Worker
- Automatic species identification from audio
- Confidence scoring and multiple predictions
- Location-based filtering for improved accuracy

### Future Integrations
- User service for authentication
- Sightings service for location data
- Maps service for geographic visualization

## Contributing

1. Follow Clean Architecture principles
2. Write comprehensive tests
3. Use type hints and proper documentation
4. Follow the existing code style and patterns

## License

Part of the Winged birdwatching application ecosystem.