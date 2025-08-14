from typing import Annotated

from fastapi import Depends
from jwt_handler.abstractions import (
    AbstractAccessTokenGenerator,
    AbstractRefreshTokenGenerator,
    AbstractTokenHandler,
)
from jwt_handler.generators import AccessTokenGenerator, RefreshTokenGenerator
from jwt_handler.handlers import JWTTokenHandler

from src.config import settings
from src.domain.abstractions.auth.password_handler import AbstractPasswordHandler
from src.infrastructure.auth.password_handler import PasswordHandler


def get_password_handler() -> AbstractPasswordHandler:
    return PasswordHandler()


def get_token_handler() -> AbstractTokenHandler:
    return JWTTokenHandler(
        public_key=settings.jwt_settings.PUBLIC_KEY,
        private_key=settings.jwt_settings.PRIVATE_KEY,
    )


def get_access_token_generator(
    token_handler: Annotated[AbstractTokenHandler, Depends(get_token_handler)],
) -> AbstractAccessTokenGenerator:
    return AccessTokenGenerator(
        token_handler=token_handler,
    )


def get_refresh_token_generator(
    token_handler: Annotated[AbstractTokenHandler, Depends(get_token_handler)],
) -> AbstractRefreshTokenGenerator:
    return RefreshTokenGenerator(
        token_handler=token_handler,
    )
