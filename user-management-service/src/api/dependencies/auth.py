from typing import Annotated

from fastapi import Depends
from src.config import settings
from src.domain.abstractions.auth.password_handler import AbstractPasswordHandler
from src.domain.abstractions.auth.token_generators.access_token_generator import AbstractAccessTokenGenerator
from src.domain.abstractions.auth.token_generators.refresh_token_generator import AbstractRefreshTokenGenerator
from src.domain.abstractions.auth.token_handler import AbstractTokenHandler
from src.infrastructure.auth.password_handler import PasswordHandler
from src.infrastructure.auth.token_generators.access_token_generator import AccessTokenGenerator
from src.infrastructure.auth.token_generators.refresh_token_generator import RefreshTokenGenerator
from src.infrastructure.auth.token_handler import JWTTokenHandler


def get_password_handler() -> AbstractPasswordHandler:
    return PasswordHandler()


def get_token_handler() -> AbstractTokenHandler:
    return JWTTokenHandler(
        public_key=settings.jwt_settings.PUBLIC_KEY,
        private_key=settings.jwt_settings.PRIVATE_KEY,
        algorithm=settings.jwt_settings.algorithm,
    )


def get_access_token_generator(
    token_handler: Annotated[AbstractTokenHandler, Depends(get_token_handler)],
) -> AbstractAccessTokenGenerator:
    return AccessTokenGenerator(
        token_handler=token_handler,
        expire_minutes=settings.jwt_settings.access_token_expire_minutes,
    )


def get_refresh_token_generator(
    token_handler: Annotated[AbstractTokenHandler, Depends(get_token_handler)],
) -> AbstractRefreshTokenGenerator:
    return RefreshTokenGenerator(
        token_handler=token_handler,
        expire_minutes=settings.jwt_settings.refresh_token_expire_minutes,
    )
