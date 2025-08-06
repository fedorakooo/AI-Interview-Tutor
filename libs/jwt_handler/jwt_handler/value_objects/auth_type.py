from enum import StrEnum


class AuthType(StrEnum):
    BEARER = "BEARER"


class TokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
