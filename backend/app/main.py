from fastapi import FastAPI

from app.routers import subgenres

app = FastAPI(title="I Was Feeling Epic")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(subgenres.router)