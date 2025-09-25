import sys
import os
from pathlib import Path

# ← AGREGAR ESTAS LÍNEAS AL INICIO
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from fastapi import FastAPI
from datetime import datetime

# Import controllers - ahora debería funcionar
from presentation.controllers.user_controller import router as user_router

# Create FastAPI app
app = FastAPI(
    title="Users Microservice", 
    description="Microservicio de gestión de usuarios",
    version="1.0.0"
)


# Include routers
app.include_router(user_router)

# Health check para API Gateway
@app.get("/health")
def health_check():
    """Health check endpoint for API Gateway monitoring"""
    return {
        "status": "healthy",
        "service": "users-service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# Service info
@app.get("/")
def service_info():
    """Service information"""
    return {
        "service": "users-microservice",
        "version": "1.0.0",
        "status": "running"
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    
    # Puerto diferente para evitar conflicto con API Gateway
    port = int(os.getenv("PORT", "8001"))
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        reload=True  # Solo para desarrollo
    )