from src.database.database import Base
from src.database.database import engine
from src.api.document import router as document_router
import src.database.models
from fastapi import FastAPI
from src.api.health import router as health_router

app = FastAPI(
    title="AI Research & Knowledge Assistant",
    version="1.0.0",
    description="Backend APIs for Document Intelligence using RAG"
)
Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(document_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Research & Knowledge Assistant"
    }