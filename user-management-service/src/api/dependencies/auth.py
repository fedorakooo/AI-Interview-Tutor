from src.config import settings
from src.domain.abstractions.auth.password_handler import AbstractPasswordHandler
from src.domain.abstractions.auth.token_handler import AbstractTokenHandler
from src.infrastructure.auth.password_handler import PasswordHandler
from src.infrastructure.auth.token_handler import JWTTokenHandler


def get_password_handler() -> AbstractPasswordHandler:
    return PasswordHandler()


def get_token_handler() -> AbstractTokenHandler:
    return JWTTokenHandler(
        public_key=settings.jwt_settings.PUBLIC_KEY,
        private_key=settings.jwt_settings.PRIVATE_KEY,
        algorithm=settings.jwt_settings.algorithm,
    )
