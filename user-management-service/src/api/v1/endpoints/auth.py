from typing import Annotated

from fastapi import APIRouter, Depends, status
from src.api.dependencies.use_cases import get_user_registration_use_case
from src.api.v1.models.user import UserCreateRequest, UserResponse
from src.application.use_cases.user_registration_use_case import UserRegistrationUseCase

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
