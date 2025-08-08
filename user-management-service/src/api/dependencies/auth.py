from typing import Annotated

from fastapi import Depends
from jwt_handler.generators import AccessTokenGenerator, RefreshTokenGenerator
from jwt_handler.handlers import JWTTokenHandler
from jwt_handler.interfaces import (
    IAccessTokenGenerator,
    IRefreshTokenGenerator,
    ITokenHandler,
)

from src.config import settings
from src.domain.interfaces.auth.password_handler import IPasswordHandler
from src.infrastructure.auth.password_handler import PasswordHandler


def get_password_handler() -> IPasswordHandler:
    return PasswordHandler()


def get_token_handler() -> ITokenHandler:
    return JWTTokenHandler(
        public_key=settings.jwt_settings.PUBLIC_KEY,
        private_key=settings.jwt_settings.PRIVATE_KEY,
    )


def get_access_token_generator(
    token_handler: Annotated[ITokenHandler, Depends(get_token_handler)],
) -> IAccessTokenGenerator:
    return AccessTokenGenerator(
        token_handler=token_handler,
    )


def get_refresh_token_generator(
    token_handler: Annotated[ITokenHandler, Depends(get_token_handler)],
) -> IRefreshTokenGenerator:
    return RefreshTokenGenerator(
        token_handler=token_handler,
    )
