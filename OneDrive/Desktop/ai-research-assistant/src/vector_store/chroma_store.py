import chromadb
from sentence_transformers import SentenceTransformer


class ChromaVectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/vector_db")

        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )
    
    def add_chunks(self, document_id, chunks):

        documents = []
        ids = []
        metadatas = []

        for chunk in chunks:

            documents.append(chunk["text"])

            ids.append(f"{document_id}_{chunk['chunk_id']}")

            metadatas.append({
                "document_id": document_id,
                "page_number": chunk["page_number"]
            })

        embeddings = self.embedding_model.encode(documents).tolist()

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query, top_k=5):

        embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )

        return results
    def get_document_chunks(self, document_id: str):

        results = self.collection.get(
            where={"document_id": document_id}
        )

        return results