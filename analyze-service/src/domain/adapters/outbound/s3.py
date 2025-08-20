from abc import ABC, abstractmethod
from io import BytesIO


class IS3Client(ABC):
    """Interface defining the interface for an S3-compatible client."""

    @abstractmethod
    async def get_file(self, key: str) -> BytesIO:
        """Gets a file from the storage by its key."""
        pass
