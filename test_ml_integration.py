#!/usr/bin/env python3
"""
Test script for ML Worker ↔ Achievements integration
Run this after starting the services with docker-compose up
"""

import requests
import json
from datetime import datetime, timezone

# Service URLs
ML_WORKER_URL = "http://localhost:8003"
ACHIEVEMENTS_URL = "http://localhost:8006"

def test_ml_worker_health():
    """Test ML Worker service health"""
    try:
        response = requests.get(f"{ML_WORKER_URL}/health")
        print(f"✅ ML Worker Health: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ ML Worker Health Error: {e}")
        return False

def test_achievements_health():
    """Test Achievements service health"""
    try:
        response = requests.get(f"{ACHIEVEMENTS_URL}/health")
        print(f"✅ Achievements Health: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Achievements Health Error: {e}")
        return False

def test_species_detection():
    """Test species detection endpoint"""
    try:
        detection_data = {
            "user_id": 1,
            "species_name": "Colibrí Coliazul",
            "confidence": 0.95,
            "location": {
                "latitude": 10.4036,
                "longitude": -75.5144,
                "address": "Cartagena, Colombia"
            },
            "detection_time": datetime.now(timezone.utc).isoformat()
        }
        
        response = requests.post(
            f"{ACHIEVEMENTS_URL}/species/detect",
            json=detection_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Species Detection: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Triggered Achievements: {len(result.get('triggered_achievements', []))}")
            print(f"   Species: {result.get('species_detected', {}).get('name')}")
        else:
            print(f"   Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Species Detection Error: {e}")
        return False

def test_batch_detection():
    """Test batch species detection endpoint"""
    try:
        batch_data = {
            "detections": [
                {
                    "user_id": 1,
                    "species_name": "Pelícano Pardo",
                    "confidence": 0.89,
                    "location": {
                        "latitude": 10.4036,
                        "longitude": -75.5144,
                        "address": "Cartagena Bay"
                    },
                    "detection_time": datetime.now(timezone.utc).isoformat()
                },
                {
                    "user_id": 1,
                    "species_name": "Gaviota Real",
                    "confidence": 0.92,
                    "location": {
                        "latitude": 10.4036,
                        "longitude": -75.5144,
                        "address": "Cartagena Beach"
                    },
                    "detection_time": datetime.now(timezone.utc).isoformat()
                }
            ]
        }
        
        response = requests.post(
            f"{ACHIEVEMENTS_URL}/species/detect/batch",
            json=batch_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Batch Detection: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Total Processed: {result.get('total_processed', 0)}")
            print(f"   Total Achievements: {result.get('total_achievements_triggered', 0)}")
        else:
            print(f"   Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Batch Detection Error: {e}")
        return False

def test_ml_worker_endpoints():
    """Test ML Worker specific endpoints"""
    try:
        # Test bird identification
        response = requests.get(f"{ML_WORKER_URL}/identify/test")
        print(f"✅ ML Worker Identify: {response.status_code}")
        
        # Test BirdNet integration endpoints
        response = requests.get(f"{ML_WORKER_URL}/birdnet/status")
        print(f"✅ BirdNet Status: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ ML Worker Endpoints Error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🧪 Testing ML Worker ↔ Achievements Integration")
    print("=" * 50)
    
    # Test basic health
    ml_healthy = test_ml_worker_health()
    achievements_healthy = test_achievements_health()
    
    if not (ml_healthy and achievements_healthy):
        print("❌ Services not healthy - make sure to run 'docker-compose up' first")
        return
    
    print("\n🔬 Testing Integration Endpoints")
    print("-" * 30)
    
    # Test ML Worker endpoints
    test_ml_worker_endpoints()
    
    # Test species detection
    test_species_detection()
    
    # Test batch detection
    test_batch_detection()
    
    print("\n✅ Integration tests completed!")
    print("Check the logs for detailed results.")

if __name__ == "__main__":
    main()