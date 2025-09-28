from io import BytesIO

from pypdf import PdfReader

from src.domain.adapters.outbound.pdf_loader import IPDFLoader


class PDFLoader(IPDFLoader):
    def load(self, pdf_bytes: BytesIO) -> str:
        reader = PdfReader(pdf_bytes)
        all_text = []
        for _i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            all_text.append(text)
        return "\n\n".join(all_text)
