from dataclasses import dataclass

from src.domain.value_objects.auth_type import AuthType


@dataclass
class TokenInfoDTO:
    access_token: str
    refresh_token: str
    auth_type: AuthType
