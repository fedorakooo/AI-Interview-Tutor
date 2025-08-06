from jwt_handler.abstractions import AbstractTokenHandler
from jwt_handler.abstractions.abstract_refresh_token_generator import AbstractRefreshTokenGenerator
from jwt_handler.config import jwt_settings
from jwt_handler.value_objects import RefreshTokenPayload, TokenType


class RefreshTokenGenerator(AbstractRefreshTokenGenerator):
    def __init__(
        self,
        token_handler: AbstractTokenHandler,
    ):
        self.token_handler = token_handler
        self.expire_minutes = jwt_settings.REFRESH_TOKEN_EXPIRE_MINUTES

    def generate_refresh_token(self, user_id: str, username: str) -> str:
        payload = RefreshTokenPayload(
            id=user_id,
            username=username,
            type=TokenType.REFRESH,
        )
        return self.token_handler.encode_jwt(
            payload=payload,
            expire_minutes=self.expire_minutes,
        )
