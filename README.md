# 🐦 Winged  
### A gamified mobile app for birdwatching in the Colombian Caribbean  

## 📖 Description  
**Winged** is a **cross-platform mobile application** that brings together **gamification, citizen science, and spatial prediction** to foster youth engagement in birdwatching across the Colombian Caribbean Region.  

Users can:  
- Register bird sightings with geolocation and pictures.  
- Explore **heatmaps** of species probability (Pokédex-style album).  
- Receive **suggested routes optimized for birdwatching** in urban and natural areas.  
- Unlock achievements and rewards as they record new bird species.  

The app integrates a **backend in Azure (FastAPI + Python)**, a **PostgreSQL/PostGIS database**, and a **Machine Learning model retrained every 15 days** with updated bird sighting data.  

---

## 🚀 Architecture  

- **Frontend (Mobile):** Expo (React Native + TypeScript)  
- **Backend (API):** Python + FastAPI, deployed in Docker containers  
- **Database:** PostgreSQL + PostGIS extension for advanced geospatial queries  
- **Machine Learning:** scikit-learn / XGBoost for probabilistic species prediction  
- **GIS Tools:** OSMnx + GeoPandas + Shapely for grids, polygons, and pathfinding  
- **Maps & Visualization:** Mapbox SDK integrated in the mobile app  
- **Infrastructure:** Azure Cloud (Web App, PostgreSQL Database, Blob Storage, Azure Functions for ML retraining)  

---

## 🤖 BirdNET Integration

Winged integrates with BirdNET analyzer for real-time bird species identification from audio recordings.

### Prerequisites

#### 1. Clone BirdNET-Analyzer Repository
```bash
# Clone the BirdNET analyzer repository
git clone https://github.com/albertojs7/BirdNET-Analyzer.git
cd BirdNET-Analyzer
```

#### 2. Set Up BirdNET Microservice
```bash
# Navigate to microservice directory
cd microservice/

# Start BirdNET microservice with MongoDB
./start.sh

# Alternative: Start without MongoDB (if you have external MongoDB)
./start.sh --no-mongodb

# Rebuild from scratch (if needed)
./start.sh --build
```

#### 3. Verify BirdNET Services
The BirdNET microservice provides the following endpoints:
- **BirdNET API**: http://localhost:8000
- **BirdNET WebSocket**: ws://localhost:8000/ws  
- **MongoDB**: mongodb://localhost:27017
- **Mongo Express UI**: http://localhost:8081 (admin/birdnet123)

Test the setup:
```bash
# Health check
curl http://localhost:8000/health

# Recent sessions
curl http://localhost:8000/sessions/recent

# Test WebSocket (from BirdNET directory)
python simple_real_time_client.py
```

### Integration Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   BirdNET       │    │   Winged        │    │   Mobile App    │
│   Microservice  │◄──►│   ML Worker     │◄──►│   (Expo)        │
│                 │    │                 │    │                 │
│ • Audio Analysis│    │ • Integration   │    │ • Audio Capture │
│ • Real-time WS  │    │ • Achievement   │    │ • Real-time UI  │
│ • MongoDB       │    │ • Data Sync     │    │ • Notifications │
│ • REST API      │    │ • User Mapping  │    │ • Species Info  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🔑 Main Endpoints (Backend API - example)
- `GET /predict` → Returns bird species probabilities by location/time.  
- `GET /heatmap` → Returns a grid-based heatmap of probable species in a polygon.  
- `GET /optimal_route` → Suggests a walking route optimized for birdwatching.  
- `POST /sightings` → Register a user’s bird sighting.  

---

## 🚀 Complete Setup Guide

### Step 1: Clone Repositories

#### Clone Winged Platform
```bash
git clone https://github.com/cosnor/Winged.git
cd Winged
```

#### Clone BirdNET Analyzer (Required for ML Integration)
```bash
# In a separate directory
cd ..
git clone https://github.com/kahst/BirdNET-Analyzer.git
```

### Step 2: Start BirdNET Microservice

```bash
cd BirdNET-Analyzer/microservice/
./start.sh
```

This will start:
- **BirdNET API**: http://localhost:8000
- **MongoDB**: mongodb://localhost:27017  
- **Mongo Express**: http://localhost:8081

Verify it's running:
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","analyzer_available":true}
```

### Step 3: Start Winged Platform

```bash
cd Winged/
docker-compose up -d
```

This will start:
- **Backend (BFF)**: http://localhost:8007
- **Users Service**: http://localhost:8001
- **Achievements**: http://localhost:8006
- **Sightings**: http://localhost:8002
- **ML Worker**: http://localhost:8003 (integrates with BirdNET)
- **Maps**: http://localhost:8004
- **Routes**: http://localhost:8005
- **Mobile App**: http://localhost:8082
- **PostgreSQL**: localhost:5432

Verify integration:
```bash
curl http://localhost:8007/health
# Expected: {"api_gateway":"healthy","services":{"users":"healthy"}}

curl http://localhost:8003/birdnet/health  
# Expected: {"status":"healthy","api_url":"http://host.docker.internal:8000"}
```

### Step 4: Test Integration

#### Test Audio Processing
```bash
# Sync BirdNET detections with Winged achievements
curl -X POST "http://localhost:8003/birdnet/sync-user-detections/1?hours_back=24&min_confidence=0.7"
```

#### Test User Registration
```bash
curl -X POST "http://localhost:8007/users/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "TestPass123"}'
```

### Step 5: Mobile App Development

```bash
cd Winged/mobile/
npm install
npx expo start
```

The mobile app can connect to:
- **Winged Backend**: http://localhost:8007 (user management, achievements)
- **BirdNET WebSocket**: ws://localhost:8000/ws (real-time audio analysis)

## 📋 Port Reference

### BirdNET Microservice
| Service | Port | URL | Description |
|---------|------|-----|-------------|
| BirdNET API | 8000 | http://localhost:8000 | Audio analysis REST API |
| MongoDB | 27017 | mongodb://localhost:27017 | BirdNET sessions/detections |
| Mongo Express | 8081 | http://localhost:8081 | MongoDB web UI (admin/birdnet123) |

### Winged Platform  
| Service | Port | URL | Description |
|---------|------|-----|-------------|
| Backend (BFF) | 8007 | http://localhost:8007 | API Gateway |
| Users | 8001 | http://localhost:8001 | Authentication & profiles |
| Sightings | 8002 | http://localhost:8002 | Bird sighting records |
| ML Worker | 8003 | http://localhost:8003 | BirdNET integration |
| Maps | 8004 | http://localhost:8004 | Geospatial services |
| Routes | 8005 | http://localhost:8005 | Route optimization |
| Achievements | 8006 | http://localhost:8006 | Gamification system |
| Mobile App | 8082 | http://localhost:8082 | Expo development server |
| PostgreSQL | 5432 | localhost:5432 | Main database |

## 🔧 Troubleshooting

### Port Conflicts
If you get "port already allocated" errors:
```bash
# Check what's using the port
netstat -tulpn | grep :8000

# Stop conflicting services
docker-compose down
# Or kill specific processes
```

### BirdNET Not Connecting
```bash
# Verify BirdNET is running
curl http://localhost:8000/health

# Check ML Worker integration  
curl http://localhost:8003/birdnet/health

# View logs
docker logs birdnet-microservice --tail=50
docker-compose logs ml_worker --tail=20
```

### Database Issues
```bash
# Check database connection
docker-compose logs db --tail=20

# Reset database (if needed)
docker-compose down -v
docker-compose up -d
```

### Password Requirements
User passwords must contain:
- At least one capital letter
- Minimum length requirements  
- Example: `"TestPass123"` ✅, `"testpass123"` ❌

## 📚 Documentation

- **BirdNET Integration**: `services/ml_worker/BIRDNET_INTEGRATION.md`
- **Integration Status**: `INTEGRATION_STATUS_REPORT.md`
- **Port Resolution**: `PORT_RESOLUTION_REPORT.md`
- **Users Service**: `USERS_SERVICE_FIX_REPORT.md`
