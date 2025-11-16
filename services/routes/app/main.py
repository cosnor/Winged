from fastapi import FastAPI

app = FastAPI(title="Routes Service")

@app.get("/")
def read_root():
    return {"message": "Routes service is running"}