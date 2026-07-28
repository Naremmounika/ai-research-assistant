from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=1000,

            chunk_overlap=150,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def create_chunks(self, pages):

        chunks = []

        chunk_id = 1

        for page in pages:

            page_chunks = self.splitter.split_text(page["text"])

            for chunk in page_chunks:

                chunks.append({

                    "chunk_id": chunk_id,

                    "page_number": page["page_number"],

                    "text": chunk

                })

                chunk_id += 1

        return chunks