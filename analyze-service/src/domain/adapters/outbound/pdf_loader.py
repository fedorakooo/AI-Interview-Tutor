from abc import ABC, abstractmethod
from io import BytesIO


class IPDFLoader(ABC):
    """Interface defining the interface for loading PDF documents."""

    @abstractmethod
    def load(self, pdf_bytes: BytesIO) -> str:
        """Loads PDF content from a BytesIO object and returns all text."""
        pass
