from jwt_handler.dtos import TokenInfoDTO
from jwt_handler.value_objects import AuthType
from pydantic import BaseModel


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
