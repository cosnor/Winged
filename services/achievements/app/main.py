from fastapi import FastAPI

app = FastAPI(title="Achievements Service")

@app.get("/")
def read_root():
    return {"message": "Achievements service is running"}
