from abc import ABC, abstractmethod

from src.domain.entities.user import User


class AbstractAccessTokenGenerator(ABC):
    """Abstract class for generating an access tokens."""

    @abstractmethod
    def generate_access_token(self, user: User) -> str:
        """Generate a new access token."""
        pass
