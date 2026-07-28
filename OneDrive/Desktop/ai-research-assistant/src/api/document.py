import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from src.schemas.comparison import ComparisonRequest
from src.rag.comparison_service import ComparisonService

from src.schemas.chat import ChatRequest
from src.rag.rag_service import RAGService

from src.services.analytics_service import AnalyticsService
from src.schemas.analytics import AnalyticsResponse

from src.schemas.summary import SummaryRequest
from src.rag.summary_service import SummaryService

from src.schemas.search import SearchRequest

from src.database.dependencies import get_db
from src.database.models import Document
from src.schemas.document import DocumentResponse

from src.document_processing.pdf_processor import PDFProcessor
from src.document_processing.chunker import DocumentChunker
from src.vector_store.chroma_store import ChromaVectorStore

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = "data/raw_documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
# Upload PDF
# -----------------------------
@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    document_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}.pdf"
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    document = Document(
        id=document_id,
        filename=file.filename,
        processing_status="UPLOADED"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


# -----------------------------
# Process PDF
# -----------------------------
@router.post("/process/{document_id}")
def process_document(
    document_id: str,
    db: Session = Depends(get_db)
):

    pdf_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}.pdf"
    )

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # Extract text
    processor = PDFProcessor()
    pages = processor.extract_text(pdf_path)

    # Chunk text
    chunker = DocumentChunker()
    chunks = chunker.create_chunks(pages)

    # Store embeddings in ChromaDB
    vector_store = ChromaVectorStore()
    vector_store.add_chunks(
        document_id=document_id,
        chunks=chunks
    )

    # Update database metadata
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if document:
        document.total_pages = len(pages)
        document.total_chunks = len(chunks)
        document.processing_status = "PROCESSED"

        db.commit()

    return {
        "message": "Document processed successfully",
        "document_id": document_id,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "status": "PROCESSED"
    }
@router.post("/search")
def semantic_search(request: SearchRequest):

    vector_store = ChromaVectorStore()

    results = vector_store.search(
        query=request.query,
        top_k=request.top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    response = []

    for doc, meta, distance in zip(documents, metadatas, distances):

        response.append({

            "document_id": meta["document_id"],

            "page_number": meta["page_number"],

            "distance": round(distance, 4),

            "text": doc

        })

    return {
        "query": request.query,
        "results": response
    }
@router.post("/chat")
def chat(request: ChatRequest):

    rag = RAGService()

    return rag.ask(
        session_id=request.session_id,
        question=request.question
    )
@router.post("/summary")
def summarize(request: SummaryRequest):

    service = SummaryService()

    return service.summarize(
        request.document_id,
        request.summary_type
    )
@router.post("/compare")
def compare_documents(request: ComparisonRequest):

    service = ComparisonService()

    return service.compare(
        request.document_id_1,
        request.document_id_2,
        request.comparison_type
    )
@router.get("/analytics", response_model=AnalyticsResponse)
def analytics(
    db: Session = Depends(get_db)
):

    service = AnalyticsService()

    return service.get_analytics(db)