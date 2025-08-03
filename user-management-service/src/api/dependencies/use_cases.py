from typing import Annotated

from fastapi import Depends
from src.api.dependencies.auth import get_access_token_generator, get_password_handler, get_refresh_token_generator
from src.api.dependencies.database import get_unit_of_work
from src.application.use_cases.auth.user_login_use_case import LoginUserUseCase
from src.application.use_cases.auth.user_registration_use_case import UserRegistrationUseCase
from src.domain.abstractions.auth.password_handler import AbstractPasswordHandler
from src.domain.abstractions.auth.token_generators.access_token_generator import AbstractAccessTokenGenerator
from src.domain.abstractions.auth.token_generators.refresh_token_generator import AbstractRefreshTokenGenerator
from src.domain.abstractions.database.uow import AbstractUnitOfWork


def get_user_registration_use_case(
    password_handler: Annotated[AbstractPasswordHandler, Depends(get_password_handler)],
    uow: Annotated[AbstractUnitOfWork, Depends(get_unit_of_work)],
) -> UserRegistrationUseCase:
    return UserRegistrationUseCase(
        password_handler=password_handler,
        uow=uow,
    )


def get_login_user_use_case(
    uow: Annotated[AbstractUnitOfWork, Depends(get_unit_of_work)],
    access_token_generator: Annotated[AbstractAccessTokenGenerator, Depends(get_access_token_generator)],
    refresh_token_generator: Annotated[AbstractRefreshTokenGenerator, Depends(get_refresh_token_generator)],
    password_handler: Annotated[AbstractPasswordHandler, Depends(get_password_handler)],
) -> LoginUserUseCase:
    return LoginUserUseCase(
        access_token_generator=access_token_generator,
        refresh_token_generator=refresh_token_generator,
        password_handler=password_handler,
        uow=uow,
    )
