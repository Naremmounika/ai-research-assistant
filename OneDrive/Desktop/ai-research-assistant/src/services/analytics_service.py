from sqlalchemy.orm import Session

from src.database.models import Document


class AnalyticsService:

    def get_analytics(self, db: Session):

        documents = db.query(Document).all()

        total_documents = len(documents)

        processed_documents = len(
            [
                d for d in documents
                if d.processing_status == "PROCESSED"
            ]
        )

        total_chunks = sum(
            d.total_chunks or 0
            for d in documents
        )

        return {
            "total_documents": total_documents,
            "processed_documents": processed_documents,
            "total_chunks": total_chunks,
            "total_embeddings": total_chunks,
            "total_questions_answered": 0
        }