from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.abstractions.database.repositories.user_repository import (
    AbstractUserRepository,
)
from src.domain.abstractions.database.uow import AbstractUnitOfWork


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """SQLAlchemy implementation of the UnitOfWork pattern."""

    def __init__(
        self,
        session: AsyncSession,
        user_repository: AbstractUserRepository,
    ):
        self._session = session
        self._user_repository = user_repository

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self._session.close()

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except Exception:
            await self.rollback()
            raise

    async def rollback(self) -> None:
        await self._session.rollback()

    @property
    def user_repository(self) -> AbstractUserRepository:
        return self._user_repository
