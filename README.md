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


## 🔑 Main Endpoints (Backend API - example)
- `GET /predict` → Returns bird species probabilities by location/time.  
- `GET /heatmap` → Returns a grid-based heatmap of probable species in a polygon.  
- `GET /optimal_route` → Suggests a walking route optimized for birdwatching.  
- `POST /sightings` → Register a user’s bird sighting.  

---

## ⚙️ Running the Backend (Local)

### Clone repository
```
git clone https://github.com/yourusername/winged.git
cd winged/backend
```
### Create virtual environment
```
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```
### Install dependencies
```
pip install -r requirements.txt
```

### Start FastAPI server
```
uvicorn app.main:app --reload
```
### Running the Mobile App (Expo)
```
cd winged/mobile
npm install
npx expo start
```
Then you can run the app:

On Android Emulator
On iOS Simulator
Or directly on your device using the Expo Go app