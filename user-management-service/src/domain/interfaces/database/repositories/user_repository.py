from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.user import User


class IUserRepository(ABC):
    """Interface defining the interface for user repository operations."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Returns one user by ID or None."""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """Returns one user by username or None."""
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Creates a new user and returns the created user."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Updates a user and returns the updated user."""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Deletes a user by its ID."""
        pass
