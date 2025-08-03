from typing import Annotated

from fastapi import Depends
from src.api.dependencies.auth import get_password_handler
from src.api.dependencies.database import get_unit_of_work
from src.application.use_cases.user_registration_use_case import UserRegistrationUseCase
from src.domain.abstractions.auth.password_handler import AbstractPasswordHandler
from src.domain.abstractions.database.uow import AbstractUnitOfWork


def get_user_registration_use_case(
    password_handler: Annotated[AbstractPasswordHandler, Depends(get_password_handler)],
    uow: Annotated[AbstractUnitOfWork, Depends(get_unit_of_work)],
) -> UserRegistrationUseCase:
    return UserRegistrationUseCase(
        password_handler=password_handler,
        uow=uow,
    )
