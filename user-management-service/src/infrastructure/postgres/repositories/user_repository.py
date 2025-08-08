from uuid import UUID

import sqlalchemy
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.interfaces.database.repositories.user_repository import IUserRepository
from src.infrastructure.postgres.exceptions.database_errors import (
    DatabaseError,
    DatabaseUniqueViolationError,
)
from src.infrastructure.postgres.schemas.user import UserORM


class UserPostgresRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(UserORM).where(UserORM.id == user_id)
        result = await self._session.execute(query)
        user_orm = result.scalar_one_or_none()
        return user_orm.to_entity() if user_orm else None

    async def get_by_username(self, username: str) -> User | None:
        query = select(UserORM).where(UserORM.username == username)
        result = await self._session.execute(query)
        user_orm = result.scalar_one_or_none()
        return user_orm.to_entity() if user_orm else None

    async def create(self, user: User) -> User:
        user_orm = UserORM.from_entity(user)
        self._session.add(user_orm)
        try:
            await self._session.flush()
            await self._session.refresh(user_orm)
        except sqlalchemy.exc.IntegrityError as exc:
            self._handle_integrity_error(exc)
        return user_orm.to_entity()

    async def update(self, user: User) -> User:
        user_orm = UserORM.from_entity(user)
        updated_user = await self._session.merge(user_orm)
        try:
            await self._session.flush()
            await self._session.refresh(updated_user)
        except sqlalchemy.exc.IntegrityError as exc:
            self._handle_integrity_error(exc)
        return updated_user.to_entity()

    async def delete(self, user_id: UUID) -> bool:
        query = delete(UserORM).where(UserORM.id == user_id)
        result = await self._session.execute(query)
        await self._session.flush()
        return result.rowcount == 1

    def _handle_integrity_error(self, exc: sqlalchemy.exc.IntegrityError) -> None:
        """Handles SQLAlchemy IntegrityError exceptions raised during database operations."""
        message = str(exc.orig).lower()
        if "duplicate key" in message:
            raise DatabaseUniqueViolationError() from exc
        raise DatabaseError(message) from exc
