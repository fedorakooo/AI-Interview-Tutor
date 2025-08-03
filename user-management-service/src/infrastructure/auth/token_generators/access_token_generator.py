from src.domain.abstractions.auth.token_generators.access_token_generator import (
    AbstractAccessTokenGenerator,
)
from src.domain.abstractions.auth.token_handler import AbstractTokenHandler
from src.domain.entities.user import User
from src.domain.value_objects.auth_type import TokenType
from src.domain.value_objects.token_payload import AccessTokenPayload


class AccessTokenGenerator(AbstractAccessTokenGenerator):
    def __init__(
        self,
        token_handler: AbstractTokenHandler,
        expire_minutes: float,
    ):
        self.token_handler = token_handler
        self.expire_minutes = expire_minutes

    def generate_access_token(self, user: User) -> str:
        payload = self._get_access_token_payload(user)
        return self.token_handler.encode_jwt(
            payload=dict(payload),
            expire_minutes=self.expire_minutes,
        )

    def _get_access_token_payload(self, user: User) -> AccessTokenPayload:
        return AccessTokenPayload(
            id=str(user.id),
            username=user.username,
            role=user.role,
            is_blocked=user.is_blocked,
            type=TokenType.ACCESS,
        )
