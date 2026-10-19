from fastapi import FastAPI

app = FastAPI(title="I Was Feeling Epic")

@app.get("/health")
def health():
    return {"status": "ok"}