class TokenError(Exception):
    """Base exception for token errors."""

    pass


class InvalidTokenError(TokenError):
    """Exception raised when a token is invalid."""

    def __init__(self, message: str = "Token is invalid"):
        super().__init__(message)


class ExpiredSignatureError(TokenError):
    """Exception raised when a token is expired."""

    def __init__(self, message: str = "Token has expired"):
        super().__init__(message)
