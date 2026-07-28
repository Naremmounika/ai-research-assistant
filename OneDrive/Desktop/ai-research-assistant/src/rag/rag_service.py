from google import genai

from src.core.config import settings
from src.vector_store.chroma_store import ChromaVectorStore



class RAGService:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.vector_store = ChromaVectorStore()

    def ask(self, session_id: str, question: str):

        # Retrieve relevant chunks
        results = self.vector_store.search(
            query=question,
            top_k=5
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n\n".join(documents)

        # Conversation history
        
        history = memory.load_memory_variables({})

        history_text = ""

        if "chat_history" in history:
            for msg in history["chat_history"]:
                history_text += f"{msg.type}: {msg.content}\n"

        prompt = f"""
You are an AI Research Assistant.

Use ONLY the retrieved context to answer.

If the answer is not available, say:

"I could not find the answer in the uploaded documents."

Conversation History:
{history_text}

Retrieved Context:
{context}

Current Question:
{question}

Return:

1. Answer
2. Mention page numbers whenever possible.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # Save conversation
        memory.chat_memory.add_user_message(question)
        memory.chat_memory.add_ai_message(response.text)

        pages = sorted(
            list(
                {
                    meta["page_number"]
                    for meta in metadatas
                }
            )
        )

        return {
            "question": question,
            "answer": response.text,
            "source_pages": pages
        }