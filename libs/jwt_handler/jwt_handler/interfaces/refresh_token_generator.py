from abc import ABC, abstractmethod


class IRefreshTokenGenerator(ABC):
    """Abstract class for generating a refresh token."""

    @abstractmethod
    def generate_refresh_token(self, user_id: str, username: str) -> str:
        """Generate a new refresh token."""
        pass
