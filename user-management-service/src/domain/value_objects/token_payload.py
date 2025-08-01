from typing import TypedDict

from src.domain.value_objects.auth_type import TokenType


class AccessTokenPayload(TypedDict):
    id: str
    username: str
    role: str
    is_blocked: bool
    type: TokenType


class RefreshTokenPayload(TypedDict):
    id: str
    username: str
    type: TokenType
