from google import genai

from src.core.config import settings
from src.vector_store.chroma_store import ChromaVectorStore


class ComparisonService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

        self.vector_store = ChromaVectorStore()

    def compare(
        self,
        document_id_1: str,
        document_id_2: str,
        comparison_type: str
    ):

        doc1 = self.vector_store.get_document_chunks(document_id_1)
        doc2 = self.vector_store.get_document_chunks(document_id_2)

        if not doc1["documents"]:
            return {
                "error": "First document not found."
            }

        if not doc2["documents"]:
            return {
                "error": "Second document not found."
            }

        context1 = "\n\n".join(doc1["documents"])
        context2 = "\n\n".join(doc2["documents"])

        prompt = f"""
You are an AI Research Assistant.

Compare the following two documents.

Comparison Type:
{comparison_type}

Document 1:
{context1}

Document 2:
{context2}

Generate the comparison in this format:

## Similarities

...

## Differences

...

## Conclusion

...
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "document_1": document_id_1,
            "document_2": document_id_2,
            "comparison_type": comparison_type,
            "comparison": response.text
        }