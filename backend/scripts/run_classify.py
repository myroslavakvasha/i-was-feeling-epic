from app.core.database import SessionLocal
from app.services import classifier
from app.services.ollama_client import OllamaClient

db = SessionLocal()
client = OllamaClient()
try:
    classifier.run(db, client)
finally:
    client.close()
    db.close()