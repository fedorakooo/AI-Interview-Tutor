import bcrypt
from src.domain.abstractions.auth.password_handler import AbstractPasswordHandler


class PasswordHandler(AbstractPasswordHandler):
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode("utf-8")

    def validate_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
