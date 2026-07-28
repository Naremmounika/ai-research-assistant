import fitz  # PyMuPDF


class PDFProcessor:

    def extract_text(self, pdf_path: str):
        """
        Extract text from every page while preserving page numbers.
        """

        document = fitz.open(pdf_path)

        pages = []

        for page_number in range(len(document)):

            page = document.load_page(page_number)

            text = page.get_text()

            pages.append({
                "page_number": page_number + 1,
                "text": text.strip()
            })

        document.close()

        return pages