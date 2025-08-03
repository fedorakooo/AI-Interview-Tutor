from datetime import datetime

from src.application.dtos.token import TokenInfoDTO
from src.domain.abstractions.auth.token_generators.access_token_generator import (
    AbstractAccessTokenGenerator,
)
from src.domain.abstractions.auth.token_generators.refresh_token_generator import (
    AbstractRefreshTokenGenerator,
)
from src.domain.abstractions.auth.token_handler import AbstractTokenHandler
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.domain.abstractions.redis.redis_client import AbstractRedisClient
from src.domain.exceptions.token_errors import InvalidTokenError
from src.domain.exceptions.user_errors import UserBlockedError
from src.domain.value_objects.auth_type import AuthType, TokenType


class RefreshTokenUseCase:
    """UseCase to refresh access and refresh tokens."""

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        redis_client: AbstractRedisClient,
        token_handler: AbstractTokenHandler,
        access_token_generator: AbstractAccessTokenGenerator,
        refresh_token_generator: AbstractRefreshTokenGenerator,
    ):
        self.uow = uow
        self.redis_client = redis_client
        self.token_handler = token_handler
        self.access_token_generator = access_token_generator
        self.refresh_token_generator = refresh_token_generator

    async def __call__(self, refresh_token: str) -> TokenInfoDTO:
        """Refreshes access and refresh tokens using a valid refresh token."""

        payload = self.token_handler.decode_jwt(refresh_token)

        if payload.get("type") != TokenType.REFRESH:
            raise InvalidTokenError()

        username = payload.get("username")
        if username is None:
            raise InvalidTokenError()

        async with self.uow:
            user = await self.uow.user_repository.get_by_username(username)

        if user is None:
            raise InvalidTokenError()
        if user.is_blocked:
            raise UserBlockedError(username)

        if await self.redis_client.exists(f"refresh-key:{refresh_token}"):
            raise InvalidTokenError()

        access_token = self.access_token_generator.generate_access_token(user=user)
        new_refresh_token = self.refresh_token_generator.generate_refresh_token(user=user)

        expiration_time = payload.get("exp")

        if expiration_time is None:
            raise InvalidTokenError()

        current_time = datetime.now().timestamp()
        ttl_seconds = int(expiration_time - current_time)

        await self.redis_client.setex(
            key=f"refresh-key:{refresh_token}",
            value=refresh_token,
            time=ttl_seconds,
        )

        return TokenInfoDTO(
            access_token=access_token,
            refresh_token=new_refresh_token,
            auth_type=AuthType.BEARER,
        )
