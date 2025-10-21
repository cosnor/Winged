#!/usr/bin/env python3
"""
BirdNET Integration Test Script
Test connectivity and data flow between BirdNET microservice and Winged ML Worker
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, List, Any

class BirdNetIntegrationTester:
    def __init__(self):
        self.birdnet_url = "http://localhost:8010"
        self.ml_worker_url = "http://localhost:8003"
        self.winged_services = {
            "achievements": "http://localhost:8006",
            "sightings": "http://localhost:8002"
        }
    
    async def test_birdnet_connectivity(self) -> Dict[str, Any]:
        """Test BirdNET microservice connectivity"""
        print("🔍 Testing BirdNET microservice connectivity...")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                # Test health endpoint
                health_response = await client.get(f"{self.birdnet_url}/health")
                health_data = health_response.json() if health_response.status_code == 200 else None
                
                # Test recent sessions
                sessions_response = await client.get(f"{self.birdnet_url}/sessions/recent?limit=5")
                sessions_data = sessions_response.json() if sessions_response.status_code == 200 else None
                
                return {
                    "health": {
                        "status_code": health_response.status_code,
                        "data": health_data
                    },
                    "sessions": {
                        "status_code": sessions_response.status_code,
                        "data": sessions_data
                    }
                }
            except Exception as e:
                return {"error": str(e)}
    
    async def test_ml_worker_connectivity(self) -> Dict[str, Any]:
        """Test ML Worker service connectivity"""
        print("🔍 Testing ML Worker service connectivity...")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                # Test health endpoint
                health_response = await client.get(f"{self.ml_worker_url}/health")
                health_data = health_response.json() if health_response.status_code == 200 else None
                
                # Test BirdNET integration health
                birdnet_health_response = await client.get(f"{self.ml_worker_url}/birdnet/health")
                birdnet_health_data = birdnet_health_response.json() if birdnet_health_response.status_code == 200 else None
                
                return {
                    "health": {
                        "status_code": health_response.status_code,
                        "data": health_data
                    },
                    "birdnet_integration": {
                        "status_code": birdnet_health_response.status_code,
                        "data": birdnet_health_data
                    }
                }
            except Exception as e:
                return {"error": str(e)}
    
    async def test_winged_services_connectivity(self) -> Dict[str, Any]:
        """Test Winged services connectivity"""
        print("🔍 Testing Winged services connectivity...")
        
        results = {}
        async with httpx.AsyncClient(timeout=10.0) as client:
            for service_name, url in self.winged_services.items():
                try:
                    response = await client.get(f"{url}/health")
                    results[service_name] = {
                        "status_code": response.status_code,
                        "data": response.json() if response.status_code == 200 else None
                    }
                except Exception as e:
                    results[service_name] = {"error": str(e)}
        
        return results
    
    async def test_integration_flow(self, test_user_id: int = 1) -> Dict[str, Any]:
        """Test the full integration flow"""
        print(f"🔄 Testing integration flow for user {test_user_id}...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                # Test syncing user detections
                sync_response = await client.post(
                    f"{self.ml_worker_url}/birdnet/sync-user-detections/{test_user_id}",
                    params={"hours_back": 24, "min_confidence": 0.5}
                )
                
                return {
                    "sync_detections": {
                        "status_code": sync_response.status_code,
                        "data": sync_response.json() if sync_response.status_code == 200 else sync_response.text
                    }
                }
            except Exception as e:
                return {"error": str(e)}
    
    def print_results(self, results: Dict[str, Any], title: str):
        """Print test results in a formatted way"""
        print(f"\n{'='*60}")
        print(f"📊 {title}")
        print(f"{'='*60}")
        print(json.dumps(results, indent=2, default=str))
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting BirdNET Integration Tests")
        print("="*60)
        
        # Test BirdNET microservice
        birdnet_results = await self.test_birdnet_connectivity()
        self.print_results(birdnet_results, "BirdNET Microservice Connectivity")
        
        # Test ML Worker
        ml_worker_results = await self.test_ml_worker_connectivity()
        self.print_results(ml_worker_results, "ML Worker Service Connectivity")
        
        # Test Winged services
        winged_results = await self.test_winged_services_connectivity()
        self.print_results(winged_results, "Winged Services Connectivity")
        
        # Test integration flow
        integration_results = await self.test_integration_flow()
        self.print_results(integration_results, "Integration Flow Test")
        
        # Summary
        print(f"\n{'='*60}")
        print("📋 TEST SUMMARY")
        print(f"{'='*60}")
        
        birdnet_healthy = birdnet_results.get('health', {}).get('status_code') == 200
        ml_worker_healthy = ml_worker_results.get('health', {}).get('status_code') == 200
        achievements_healthy = winged_results.get('achievements', {}).get('status_code') == 200
        
        print(f"✅ BirdNET Microservice: {'HEALTHY' if birdnet_healthy else '❌ FAILED'}")
        print(f"✅ ML Worker Service: {'HEALTHY' if ml_worker_healthy else '❌ FAILED'}")
        print(f"✅ Achievements Service: {'HEALTHY' if achievements_healthy else '❌ FAILED'}")
        
        if all([birdnet_healthy, ml_worker_healthy, achievements_healthy]):
            print("\n🎉 All services are healthy and ready for integration!")
        else:
            print("\n⚠️ Some services need attention before full integration.")
        
        return {
            "birdnet": birdnet_results,
            "ml_worker": ml_worker_results,
            "winged_services": winged_results,
            "integration": integration_results
        }

async def main():
    """Main function to run the integration tests"""
    tester = BirdNetIntegrationTester()
    results = await tester.run_all_tests()
    return results

if __name__ == "__main__":
    asyncio.run(main())