from google import genai

from src.core.config import settings
from src.vector_store.chroma_store import ChromaVectorStore


class SummaryService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

        self.vector_store = ChromaVectorStore()

    def summarize(self, document_id: str, summary_type: str):

        results = self.vector_store.get_document_chunks(document_id)

        if not results["documents"]:
            return {
                "error": "Document not found."
            }

        context = "\n\n".join(results["documents"])

        prompt = f"""
You are an AI Research Assistant.

Below is a document.

----------------------
{context}
----------------------

Generate a {summary_type}.

Rules:

1. If Executive Summary:
   Give a concise overview.

2. If Technical Summary:
   Explain the technical aspects.

3. If Bullet Summary:
   Return bullet points only.

4. If Key Takeaways:
   Return the important insights.

Return ONLY the summary.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "document_id": document_id,
            "summary_type": summary_type,
            "summary": response.text
        }