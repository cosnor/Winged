# 🚀 ML Worker Setup and Testing Guide

## Quick Start

### 1. Start Services
```bash
# Start all services
docker-compose up -d

# Check services are running
docker-compose ps
```

### 2. Verify ML Worker Health
```bash
curl http://localhost:8003/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ml_worker", 
  "version": "1.0.0",
  "dependencies": {
    "achievements": "healthy",
    "sightings": "healthy",
    "birdnet_api": "not_configured",
    "birdnet_database": "not_configured"
  }
}
```

### 3. Test Bird Identification
```bash
# Create test audio file (or use real audio)
echo "test audio data" > test_bird.wav

# Test identification
curl -X POST http://localhost:8003/identify-bird \
  -F "audio=@test_bird.wav" \
  -F "user_id=1" \
  -F "latitude=10.4595" \
  -F "longitude=-75.5118"
```

### 4. Check Achievements Created
```bash
curl http://localhost:8006/users/1/achievements
```

## Integration Testing

### Test Achievement Triggering
```bash
# Test with different species (mock ML will randomly select)
for i in {1..5}; do
  echo "test audio $i" > test_$i.wav
  curl -X POST http://localhost:8003/identify-bird \
    -F "audio=@test_$i.wav" \
    -F "user_id=$i"
  sleep 1
done
```

### Test BirdNet API Integration (if available)
```bash
# Test API health
curl http://localhost:8003/birdnet/health

# Process session (if BirdNet API is configured)
curl -X POST http://localhost:8003/birdnet/process-session \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test_session", "user_id": 1}'
```

### Test Database Integration (if MongoDB configured)
```bash
# Check database health
curl http://localhost:8003/database/health

# Get statistics
curl http://localhost:8003/database/statistics

# Test sync (if data available)
curl -X POST http://localhost:8003/database/sync-unprocessed \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "min_confidence": 0.7}'
```

## Configuration for Production

### MongoDB Setup (Optional)
```bash
# Add to docker-compose.yml environment
- BIRDNET_MONGODB_URL=mongodb://username:password@mongodb:27017/birdnet
- BIRDNET_DATABASE_NAME=birdnet_production  
- BIRDNET_SESSIONS_COLLECTION=sessions
- BIRDNET_DETECTIONS_COLLECTION=detections
```

### External BirdNet API (Optional)  
```bash
# Add to docker-compose.yml environment
- BIRDNET_API_URL=http://your-birdnet-api:8000
```

## Troubleshooting

### Common Issues

1. **Service not starting**
   ```bash
   docker-compose logs ml_worker
   ```

2. **Dependencies unavailable**
   ```bash
   # Check other services
   curl http://localhost:8006/health  # achievements
   curl http://localhost:8005/health  # sightings
   ```

3. **Import errors**
   ```bash
   # Rebuild with latest requirements
   docker-compose build ml_worker
   docker-compose up -d ml_worker
   ```

### Success Indicators
- ✅ ML Worker health check returns "healthy"
- ✅ Bird identification returns species and confidence
- ✅ Achievements are created for test users
- ✅ Sightings appear in database
- ✅ All service dependencies show as "healthy"

## Next Steps

1. **Configure MongoDB** for database integration (optional)
2. **Set up BirdNet API** connection (optional)  
3. **Test with real audio files** for actual species identification
4. **Monitor achievement creation** and user engagement
5. **Scale services** as needed for production load

## API Documentation

Once services are running, visit:
- ML Worker API: http://localhost:8003/docs
- Achievements API: http://localhost:8006/docs

---

**Your ML Worker ↔ Achievements integration is ready! 🎯**