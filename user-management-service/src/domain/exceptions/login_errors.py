class LoginError(Exception):
    """Base exception for login errors."""

    pass


class InvalidUsernameError(LoginError):
    """Exception raised when the provided username is invalid."""

    def __init__(self, username: str):
        super().__init__(f"Invalid username [{username}]")


class InvalidPasswordError(LoginError):
    """Exception raised when the provided password is invalid."""

    def __init__(self):
        super().__init__("Invalid password")
