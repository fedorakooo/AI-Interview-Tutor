class UserBlockedError(Exception):
    """Exception raised when a user is blocked and cannot perform the action."""

    def __init__(self, username: str):
        super().__init__(f"User with username [{username}] is blocked")
