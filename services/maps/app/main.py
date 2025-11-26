from fastapi import FastAPI
from app.api.routes import router as api_router


app = FastAPI(title="Maps Service")

# Incluir las rutas de la API
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Maps service is running"}