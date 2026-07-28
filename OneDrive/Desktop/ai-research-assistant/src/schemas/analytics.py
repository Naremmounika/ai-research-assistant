from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    total_documents: int
    processed_documents: int
    total_chunks: int
    total_embeddings: int
    total_questions_answered: int