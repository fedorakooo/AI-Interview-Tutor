from src.application.dtos.token import TokenInfoDTO
from src.domain.abstractions.auth.password_handler import AbstractPasswordHandler
from src.domain.abstractions.auth.token_generators.access_token_generator import AbstractAccessTokenGenerator
from src.domain.abstractions.auth.token_generators.refresh_token_generator import AbstractRefreshTokenGenerator
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.domain.exceptions.login_errors import (
    InvalidPasswordError,
    InvalidUsernameError,
)
from src.domain.exceptions.user_errors import UserBlockedError
from src.domain.value_objects.auth_type import AuthType


class LoginUserUseCase:
    """UseCase to handle user authentication."""

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        access_token_generator: AbstractAccessTokenGenerator,
        refresh_token_generator: AbstractRefreshTokenGenerator,
        password_handler: AbstractPasswordHandler,
    ):
        self.uow = uow
        self.access_token_generator = access_token_generator
        self.refresh_token_generator = refresh_token_generator
        self.password_handler = password_handler

    async def __call__(self, username: str, password: str) -> TokenInfoDTO:
        """Checks user credentials and returns access token"""

        async with self.uow:
            user = await self.uow.user_repository.get_by_username(username)
        if user is None:
            raise InvalidUsernameError(username)

        is_password_correct = self.password_handler.validate_password(
            password=password,
            hashed_password=user.hashed_password,
        )

        if not is_password_correct:
            raise InvalidPasswordError()

        if user.is_blocked:
            raise UserBlockedError(username)

        access_token = self.access_token_generator.generate_access_token(user=user)
        refresh_token = self.refresh_token_generator.generate_refresh_token(user=user)

        return TokenInfoDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            auth_type=AuthType.BEARER,
        )
