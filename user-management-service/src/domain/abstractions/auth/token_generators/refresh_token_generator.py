from abc import ABC, abstractmethod

from src.domain.entities.user import User


class AbstractRefreshTokenGenerator(ABC):
    """Abstract class for generating a refresh token."""

    @abstractmethod
    def generate_refresh_token(self, user: User) -> str:
        """Generate a new refresh token."""
        pass
