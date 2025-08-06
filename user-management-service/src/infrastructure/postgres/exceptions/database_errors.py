class DatabaseError(Exception):
    """Base exception for database errors."""

    def __init__(self, message: str = "Database error") -> None:
        self.message = message
        super().__init__(self.message)


class DatabaseUniqueViolationError(DatabaseError):
    """Exception raised when an operation violates unique constraint."""

    def __init__(self, field=None):
        self.message = "Unique constraint violation"
        super().__init__(self.message)
