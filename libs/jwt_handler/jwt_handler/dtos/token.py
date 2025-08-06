from dataclasses import dataclass

from jwt_handler.value_objects import AuthType


@dataclass
class TokenInfoDTO:
    access_token: str
    refresh_token: str
    auth_type: AuthType
