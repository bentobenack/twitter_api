# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from api.v1.users.schemas.user import UserOut


class BaseJWTAccessToken(BaseModel):
    access_token: str = Field(
        ...,
        min_length=8,
        example='access_token',
        description='Access token'
    )


class JWTAccessToken(BaseJWTAccessToken):
    access_token_expiration: int = Field(
        ...,
        gt=0,
        example=60,
        description='Access token expiration in seconds'
    )


class BaseJWTRefreshToken(BaseModel):
    refresh_token: str = Field(
        ...,
        min_length=8,
        example='refresh_token',
        description='Refresh token'
    )


class JWTRefreshToken(BaseJWTRefreshToken):

    refresh_token_expiration: int = Field(
        ...,
        gt=0,
        example=60,
        description='Refresh token expiration in seconds'
    )


class JWTCredentials(JWTRefreshToken, JWTAccessToken):
    pass


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        example="benack@email.com"
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        example='H4rdP455w0rd',
    )


class LoginReponse(JWTCredentials):

    user: UserOut