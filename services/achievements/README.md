# Achievements Service

The Achievements Service is a microservice that manages user achievements, bird collections, and gamification features for the Winged birdwatching application.

## Features

### 🏆 Achievement System
- **Automatic Achievement Unlocking**: Achievements are automatically unlocked when users meet specific criteria
- **Progress Tracking**: Track user progress towards achievements with percentage completion
- **XP and Leveling**: Users earn experience points (XP) and level up based on achievements
- **Multiple Achievement Categories**:
  - First bird identification
  - Species count milestones (5, 25, 50, 100 species)
  - Sighting count milestones
  - Consecutive day streaks
  - Rare species identification

### 🐦 Bird Collection Management
- **Species Tracking**: Track unique bird species identified by each user
- **Sighting Statistics**: Count total sightings per species
- **Location Data**: Store first and last sighting locations
- **Confidence Scores**: Track identification confidence levels

### 📊 User Statistics
- Total sightings count
- Unique species count
- Total XP earned
- Current level
- Achievement count
- Longest and current streaks
- First and last sighting dates

### 🏅 Leaderboards
- **Species Leaderboard**: Rank users by unique species count
- **XP Leaderboard**: Rank users by total experience points
- Configurable result limits

## API Endpoints

### User Collection & Stats
- `GET /users/{user_id}/collection` - Get user's bird collection with stats and recent achievements
- `GET /users/{user_id}/stats` - Get user statistics
- `GET /users/{user_id}/achievements` - Get user's unlocked achievements
- `GET /users/{user_id}/achievements/progress` - Get progress on all achievements

### Sighting Processing
- `POST /sightings/process` - Process a new sighting and unlock achievements

### Achievement Management
- `GET /achievements` - Get all available achievements
- `GET /achievements/{achievement_id}` - Get specific achievement details
- `POST /achievements` - Create new achievement (admin)

### Leaderboards
- `GET /leaderboard/species` - Get species count leaderboard
- `GET /leaderboard/xp` - Get XP leaderboard

### Utility
- `GET /` - Service status
- `GET /health` - Health check
- `GET /birds/species` - Get all sighted species
- `GET /birds/species/{species_name}/users` - Get users who sighted a species

## Data Models

### Achievement
- Name, description, category
- Criteria (JSON configuration)
- XP reward, icon
- Active status

### UserAchievement
- User ID, achievement ID
- Progress percentage
- Unlock timestamp

### BirdCollection
- User ID, species information
- Sighting count and timestamps
- Location and confidence data

### UserStats
- Comprehensive user statistics
- XP, level, streaks
- Achievement counts

## Default Achievements

The service comes with 8 default achievements:

1. **First Flight** (100 XP) - Identify your first bird species
2. **Novice Birder** (250 XP) - Identify 5 different species
3. **Experienced Birder** (500 XP) - Identify 25 different species
4. **Expert Birder** (1000 XP) - Identify 50 different species
5. **Master Birder** (2000 XP) - Identify 100 different species
6. **Active Observer** (300 XP) - Record 50 bird sightings
7. **Dedicated Watcher** (400 XP) - Record sightings for 7 consecutive days
8. **Committed Birder** (1000 XP) - Record sightings for 30 consecutive days

## Integration

### With Sightings Service
The sightings service automatically calls the achievements service when new birds are identified:

```python
# In sightings service
response = await client.post(
    f"{ACHIEVEMENTS_URL}/sightings/process",
    json=sighting_data
)
```

### With Backend Gateway
All achievements endpoints are proxied through the main backend BFF service for unified API access.

## Configuration

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `ACHIEVEMENTS_URL` - Service URL for inter-service communication

### Database
- Uses PostgreSQL with SQLAlchemy ORM
- Automatic table creation on startup
- Default achievements seeded on first run

## Development

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set database URL
export DATABASE_URL="postgresql://user:pass@localhost/winged"

# Run service
python -m app.main
```

### Running with Docker
```bash
docker build -t achievements-service .
docker run -p 8006:8006 -e DATABASE_URL="..." achievements-service
```

### Testing
The service includes comprehensive error handling and graceful degradation when dependencies are unavailable.

## Architecture

The service follows clean architecture principles:
- **Models**: SQLAlchemy database models
- **Schemas**: Pydantic request/response models
- **Services**: Business logic layer
- **Main**: FastAPI application and routes

## Gamification Features

### Level System
Users level up based on total XP earned:
- Level = √(XP / 100) + 1
- Provides continuous progression incentive

### Streak Tracking
- Tracks consecutive days with bird sightings
- Encourages daily engagement
- Separate tracking for current and longest streaks

### Achievement Categories
- **Milestone-based**: Species count, sighting count
- **Behavior-based**: Daily streaks, consistency
- **Discovery-based**: First sighting, rare species
- **Extensible**: Easy to add new achievement types

This service provides a comprehensive gamification layer that encourages user engagement and creates a rewarding experience for birdwatchers of all levels.