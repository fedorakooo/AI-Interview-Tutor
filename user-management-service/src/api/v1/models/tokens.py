from pydantic import BaseModel
from src.application.dtos.token import TokenInfoDTO
from src.domain.value_objects.auth_type import AuthType


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    auth_type: AuthType

    @classmethod
    def from_dto(cls, login_info: TokenInfoDTO) -> "TokenResponse":
        return TokenResponse(
            access_token=login_info.access_token,
            refresh_token=login_info.refresh_token,
            auth_type=login_info.auth_type,
        )
