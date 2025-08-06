from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from pydantic import SecretStr
from src.api.dependencies.use_cases import (
    get_login_user_use_case,
    get_refresh_token_use_case,
    get_user_registration_use_case,
)
from src.api.v1.models.tokens import TokenResponse
from src.api.v1.models.user import UserCreateRequest, UserResponse
from src.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from src.application.use_cases.auth.user_login_use_case import LoginUserUseCase
from src.application.use_cases.auth.user_registration_use_case import UserRegistrationUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Unique constraint violation"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Unexpected server error"},
    },
)
async def signup(
    user_create_request: UserCreateRequest,
    user_registration_use_case: Annotated[UserRegistrationUseCase, Depends(get_user_registration_use_case)],
) -> UserResponse:
    user_create = user_create_request.to_dto()
    created_user = await user_registration_use_case(user_create)
    return UserResponse.from_dto(created_user)


@router.post(
    "/token",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid password or login"},
        status.HTTP_403_FORBIDDEN: {"description": "User is blocked"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Unexpected server error"},
    },
)
async def token(
    login_user_use_case: Annotated[LoginUserUseCase, Depends(get_login_user_use_case)],
    username: str = Form(...),
    password: SecretStr = Form(...),
) -> TokenResponse:
    token_info = await login_user_use_case(
        username=username,
        password=password.get_secret_value(),
    )
    return TokenResponse.from_dto(token_info)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid or expired refresh token"},
        status.HTTP_403_FORBIDDEN: {"description": "User is blocked"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Unexpected server error"},
    },
)
async def auth_refresh(
    refresh_token_use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)],
    refresh_token: str = Form(...),
) -> TokenResponse:
    token_info = await refresh_token_use_case(refresh_token)
    return TokenResponse.from_dto(token_info)
