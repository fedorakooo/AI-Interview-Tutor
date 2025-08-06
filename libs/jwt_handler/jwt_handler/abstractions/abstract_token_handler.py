from abc import ABC, abstractmethod

from jwt_handler.value_objects import AccessTokenPayload, RefreshTokenPayload


class AbstractTokenHandler(ABC):
    """Abstract class for handling token operations."""

    @abstractmethod
    def encode_jwt(
        self,
        payload: AccessTokenPayload | RefreshTokenPayload,
        expire_minutes: float,
    ) -> str:
        """Encodes the given payload into a JWT token."""
        pass

    @abstractmethod
    def decode_jwt(
        self,
        token: str | bytes,
    ) -> AccessTokenPayload | RefreshTokenPayload:
        """Decodes the given JWT and returns its payload."""
        pass
